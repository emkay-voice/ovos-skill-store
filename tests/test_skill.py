"""The store skill reads both store formats, searches in English and Danish,
and installs through ovos-core's installer only after a yes."""
import sys
from pathlib import Path

import pytest
from ovos_bus_client.message import Message
from ovos_utils.fakebus import FakeBus

ROOT = Path(__file__).parent.parent / "ovos_skill_store"
sys.path.insert(0, str(ROOT.parent))
import ovos_skill_store as pkg  # noqa: E402
from ovos_skill_store import stores  # noqa: E402

EMKAY = [
    {"package": "ovos-skill-weather", "kind": "skill", "status": "works", "category": "information",
     "icon": "https://example.org/w.png", "source": "",
     "texts": {"en-us": {"name": "Weather", "description": "Weather forecasts",
                         "examples": ["What's the weather like?"]},
               "da-dk": {"name": "Vejr", "description": "Vejrudsigter", "examples": ["Hvordan er vejret?"]}}},
    {"package": "ovos-skill-joke", "kind": "skill", "status": "untested", "category": "fun",
     "texts": {"en-us": {"name": "Jokes", "description": "Tells jokes", "examples": ["Tell me a joke"]}}},
    {"package": "ovos-core", "kind": "pipeline", "status": "builtin", "texts": {"en-us": {"name": "Core"}}},
    {"package": "ovos-skill-broken", "kind": "skill", "status": "fails", "texts": {"en-us": {"name": "Broken"}}},
]
KLONDIKE = [
    {"package_name": "ovos-skill-laugh", "name": "Laugh", "description": "Laugh when asked",
     "examples": ["can you laugh"], "component_type": "Skill", "on_pypi": True, "archived": False,
     "category": "Entertainment", "tags": ["fun"]},
    {"package_name": "ovos-plugin-x", "component_type": "Plugin", "on_pypi": True},
]


def test_parse_both_formats():
    got = {s.package for s in stores.parse(EMKAY, "Emkay") + stores.parse(KLONDIKE, "Klondike")}
    assert got == {"ovos-skill-weather", "ovos-skill-joke", "ovos-skill-laugh"}


def test_text_in_the_language_else_english():
    w = stores.parse(EMKAY, "Emkay")[0]
    assert w.text("da-DK")["name"] == "Vejr"
    assert w.text("de-DE")["name"] == "Weather"


def test_search_english_and_danish():
    skills = stores.parse(EMKAY, "E") + stores.parse(KLONDIKE, "K")
    assert stores.search(skills, "the weather", "en-us", {})[0][1].package == "ovos-skill-weather"
    words = stores.load_words(ROOT / "locale/da-DK/search_words.json")
    assert stores.search(skills, "vittigheder", "da-dk", words)[0][1].package == "ovos-skill-joke"
    assert stores.search(skills, "vejret", "da-dk", words)[0][1].package == "ovos-skill-weather"


class FakeStores(stores.Stores):
    def skills(self):
        return stores.parse(EMKAY, "Emkay")


@pytest.fixture
def skill():
    bus = FakeBus()
    spoken = []
    bus.on("speak", lambda m: spoken.append(Message.deserialize(m) if isinstance(m, str) else m))
    s = pkg.StoreSkill(bus=bus, skill_id="ovos-skill-store.emkay-voice")
    s.stores = FakeStores([])
    s.spoken = spoken
    yield s
    s.shutdown()


def said(skill):
    return skill.spoken[-1].data["utterance"]


def test_search_names_what_it_found(skill):
    skill.handle_search(Message("x", {"query": "weather"}))
    assert "Weather" in said(skill)


def test_nothing_found(skill):
    skill.handle_search(Message("x", {"query": "submarines"}))
    assert "didn't find" in said(skill)


def test_install_after_yes(skill, monkeypatch):
    asked = []
    monkeypatch.setattr(skill, "ask_yesno", lambda d, data=None: asked.append(d) or "yes")
    sent = []

    def installer(message):
        m = Message.deserialize(message) if isinstance(message, str) else message
        sent.append(m.data["packages"])
        skill.bus.emit(m.reply("ovos.pip.install.complete"))

    skill.bus.on("ovos.pip.install", installer)
    skill.handle_install(Message("x", {"name": "jokes"}))
    assert asked == ["confirm_install"] and sent == [["ovos-skill-joke"]]
    assert "Tell me a joke" in said(skill)


def test_no_install_without_yes(skill, monkeypatch):
    monkeypatch.setattr(skill, "ask_yesno", lambda d, data=None: "no")
    sent = []
    skill.bus.on("ovos.pip.install", lambda m: sent.append(m))
    skill.handle_install(Message("x", {"name": "weather"}))
    assert not sent and "won't" in said(skill)


def test_stores_setting(skill):
    skill.settings["stores"] = "https://a.example/skills.json, https://b.example/skills.json"
    assert [s["url"] for s in skill.store_list()] == ["https://a.example/skills.json", "https://b.example/skills.json"]
    skill.settings["stores"] = []
    assert skill.store_list() == pkg.DEFAULT_STORES


LANGS = ["en-US", "da-DK", "de-DE", "nl-NL", "fr-FR", "es-ES", "it-IT",
         "pt-BR", "pt-PT", "ca-ES", "gl-ES", "eu-ES"]


@pytest.mark.parametrize("lang", LANGS)
def test_every_language_has_everything(lang):
    loc = ROOT / "locale" / lang
    for intent in ("search", "install", "recommend"):
        assert (loc / f"{intent}.intent").read_text(encoding="utf-8").strip(), intent
    for d in ("found", "nothing_found", "recommend", "recommend_title", "nothing_to_recommend", "not_found",
              "already_installed", "confirm_install", "not_installing", "installing", "install_failed",
              "installed", "installed_try", "badge_works", "badge_installed", "and"):
        assert (loc / f"{d}.dialog").read_text(encoding="utf-8").strip(), d
    assert isinstance(stores.load_words(loc / "search_words.json"), dict)
