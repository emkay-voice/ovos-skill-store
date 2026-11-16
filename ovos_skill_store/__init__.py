"""Skill store: find and install skills by voice.

"Find a skill for the weather" searches the configured stores and names the
best matches; the screen shows each as a card with its icon and a few of the
things you can say to it, as speech bubbles. "Install the joke skill" asks
first, then installs it the way the control panel does (ovos-core's own
installer, `ovos.pip.install`), and says what to try once it is in.

Generic: the stores are a setting, one or more, read in either the Emkay
store's format or ovos-klondike-mercantile's (stores.py).

Settings:
    stores   a list of {"name": ..., "url": ...}, or a comma-separated
             string of URLs (default: the Emkay store)
"""
import html
import importlib.metadata
import random
import threading
from os.path import dirname, isdir, join
from os import listdir

from ovos_bus_client.message import Message
from ovos_utils import classproperty
from ovos_utils.process_utils import RuntimeRequirements
from ovos_workshop.decorators import intent_handler
from ovos_workshop.skills import OVOSSkill

from .stores import Stores, load_words, search

DEFAULT_STORES = [{"name": "Emkay", "url": "https://store.emkay.ai/data/skills.json"}]
#: how long an install may take before we stop waiting (a browser is slow)
INSTALL_TIMEOUT = 900


def installed(package: str) -> bool:
    try:
        importlib.metadata.distribution(package)
        return True
    except importlib.metadata.PackageNotFoundError:
        return False


class StoreSkill(OVOSSkill):

    @classproperty
    def runtime_requirements(self):
        return RuntimeRequirements(internet_before_load=False,
                                   network_before_load=False,
                                   gui_before_load=False,
                                   requires_internet=True,
                                   requires_network=True,
                                   requires_gui=False,
                                   no_internet_fallback=False,
                                   no_network_fallback=False,
                                   no_gui_fallback=True)

    def initialize(self):
        self.stores = Stores(self.store_list())
        self.settings_change_callback = self._on_settings

    def _on_settings(self):
        self.stores = Stores(self.store_list())

    def store_list(self) -> list:
        """The configured stores, as [{"name", "url"}]."""
        value = self.settings.get("stores")
        if isinstance(value, str):
            value = [{"name": u.strip(), "url": u.strip()} for u in value.split(",") if u.strip()]
        if isinstance(value, list):
            out = [s if isinstance(s, dict) else {"name": str(s), "url": str(s)} for s in value]
            out = [s for s in out if s.get("url")]
            if out:
                return out
        return list(DEFAULT_STORES)

    # -- words ---------------------------------------------------------------

    def search_words(self) -> dict:
        """This language's search words (locale/<lang>/search_words.json)."""
        base = join(dirname(__file__), "locale")
        want = self.lang.lower()
        for d in listdir(base) if isdir(base) else []:
            if d.lower() == want or d.lower().split("-")[0] == want.split("-")[0]:
                return load_words(join(base, d, "search_words.json"))
        return {}

    def join(self, items: list) -> str:
        if len(items) <= 1:
            return "".join(items)
        return f"{', '.join(items[:-1])} {self.dialog_renderer.render('and')} {items[-1]}"

    # -- the screen ----------------------------------------------------------

    def cards(self, skills: list, title: str):
        """Each skill as a card: icon, name, description and up to three of
        its example phrases as speech bubbles."""
        if not self.gui.connected:
            return
        works = self.dialog_renderer.render("badge_works")
        have = self.dialog_renderer.render("badge_installed")
        rows = []
        for s in skills:
            t = s.text(self.lang)
            icon = (f'<img src="{html.escape(s.icon)}" alt="">' if s.icon
                    else f'<div class="noicon">{html.escape(t["name"][:1].upper())}</div>')
            bubbles = "".join(f'<div class="bubble">“{html.escape(e)}”</div>' for e in t["examples"][:3])
            badge = have if installed(s.package) else works if s.works else ""
            rows.append(f'''<div class="card">{icon}<div class="body">
<div class="name">{html.escape(t["name"])}{f'<span class="badge">{html.escape(badge)}</span>' if badge else ""}</div>
<div class="desc">{html.escape(t["description"][:160])}</div>{bubbles}</div></div>''')
        page = f'''<!doctype html><meta charset="utf-8"><style>
body{{margin:0;padding:16px;background:#000;color:#eee;font:16px/1.35 system-ui,sans-serif}}
h1{{font-weight:300;letter-spacing:.15em;font-size:20px;margin:0 0 12px;text-align:center}}
.card{{display:flex;gap:14px;background:#141414;border-radius:16px;padding:14px;margin:0 0 12px}}
.card img,.noicon{{width:56px;height:56px;border-radius:12px;flex:none;object-fit:contain;background:#222}}
.noicon{{display:flex;align-items:center;justify-content:center;font-size:28px;color:#22a7f0}}
.name{{font-size:19px}}.desc{{color:#9ab;font-size:14px;margin:2px 0 6px}}
.badge{{font-size:12px;color:#7d7;margin-left:8px}}
.bubble{{display:inline-block;background:#22a7f0;color:#fff;border-radius:16px 16px 16px 4px;
padding:6px 12px;margin:4px 6px 0 0;font-size:14px}}
</style><h1>{html.escape(title)}</h1>{"".join(rows)}'''
        self.gui.show_html(page, override_idle=60)

    # -- search --------------------------------------------------------------

    @intent_handler("search.intent")
    def handle_search(self, message: Message):
        query = message.data.get("query") or message.data.get("utterance", "")
        found = [s for _, s in search(self.stores.skills(), query, self.lang, self.search_words())]
        if not found:
            return self.speak_dialog("nothing_found", {"query": query})
        self.cards(found, query)
        new = [s for s in found if not installed(s.package)]
        if not new:   # what matches is here already: say how to use it
            have = found[0].text(self.lang)
            if have["examples"]:
                return self.speak_dialog("already_have_try", {"name": have["name"], "example": have["examples"][0]})
            return self.speak_dialog("already_installed", {"name": have["name"]})
        names = [s.text(self.lang)["name"] for s in new]
        self.speak_dialog("found", {"count": len(new), "list": self.join(names)})

    @intent_handler("recommend.intent")
    def handle_recommend(self, message: Message):
        good = [s for s in self.stores.skills() if s.works and not installed(s.package)]
        if not good:
            return self.speak_dialog("nothing_to_recommend")
        pick = random.sample(good, min(3, len(good)))
        self.cards(pick, self.dialog_renderer.render("recommend_title"))
        self.speak_dialog("recommend", {"list": self.join([s.text(self.lang)["name"] for s in pick])})

    # -- install -------------------------------------------------------------

    @intent_handler("install.intent")
    def handle_install(self, message: Message):
        name = message.data.get("name", "")
        skill = self.stores.find(name, self.lang)
        if not skill:
            return self.speak_dialog("not_found", {"name": name})
        title = skill.text(self.lang)["name"]
        if installed(skill.package):
            return self.speak_dialog("already_installed", {"name": title})
        self.cards([skill], title)
        if self.ask_yesno("confirm_install", {"name": title}) != "yes":
            return self.speak_dialog("not_installing", {"name": title})
        self.speak_dialog("installing", {"name": title})
        ok, detail = self.pip_install(skill.package)
        if not ok:
            return self.speak_dialog("install_failed", {"name": title})
        examples = skill.text(self.lang)["examples"]
        if examples:
            self.speak_dialog("installed_try", {"name": title, "example": examples[0]})
        else:
            self.speak_dialog("installed", {"name": title})

    def pip_install(self, package: str):
        """Install through ovos-core's installer; (succeeded, detail)."""
        done = threading.Event()
        result = {}

        def answer(message):
            result["ok"] = message.msg_type.endswith(".complete")
            result["detail"] = (message.data or {}).get("error", "")
            done.set()

        self.bus.once("ovos.pip.install.complete", answer)
        self.bus.once("ovos.pip.install.failed", answer)
        self.bus.emit(Message("ovos.pip.install", {"packages": [package]},
                              {"source": self.skill_id, "destination": ["skills"]}))
        done.wait(INSTALL_TIMEOUT)
        return result.get("ok", False), result.get("detail", "")
