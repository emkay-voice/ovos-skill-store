"""Skill stores: read their lists, and search them.

A store is a URL to a JSON list of skills. Two formats are read, told apart
by their records:

- the Emkay store's (https://store.emkay.ai/data/skills.json): texts per
  language (name, description, examples), and whether the skill was found
  working in Emkay ("status")
- ovos-klondike-mercantile's (https://andlo.github.io/ovos-klondike-mercantile/skills.json):
  every OVOS skill found on GitHub, in English

Both become the same `Skill` record. Search matches the words of a question
against each skill's name, description, examples and category, in the
question's language and in English, with the language's own search words
(locale/<lang>/search_words.json) turning "vejret" into "weather".
"""
import json
import re
import time
from dataclasses import dataclass, field

import requests

CACHE_SECONDS = 6 * 3600


@dataclass
class Skill:
    package: str                 # what pip installs
    texts: dict                  # {lang: {"name", "description", "examples"}}, "en-us" at least
    icon: str = None
    category: str = ""
    source: str = ""
    works: bool = None           # found working where it is used (None: not tested)
    store: str = ""              # the store's name, for "found in …"
    tags: list = field(default_factory=list)

    def text(self, lang: str) -> dict:
        """name, description and examples in `lang`, else English."""
        lang = lang.lower()
        for key in (lang, lang.split("-")[0]):
            for k, v in self.texts.items():
                if k.lower() == key or k.lower().split("-")[0] == key:
                    if v.get("name") or v.get("examples"):
                        base = self.texts.get("en-us", {})
                        return {"name": v.get("name") or base.get("name") or self.package,
                                "description": v.get("description") or base.get("description", ""),
                                "examples": v.get("examples") or base.get("examples", [])}
        base = self.texts.get("en-us") or next(iter(self.texts.values()), {})
        return {"name": base.get("name") or self.package, "description": base.get("description", ""),
                "examples": base.get("examples", [])}


def _from_emkay(r: dict, store: str):
    if r.get("kind") != "skill" or r.get("status") not in ("works", "untested"):
        return None              # plugins, what ships already, what does not work
    return Skill(package=r["package"], texts=r.get("texts") or {}, icon=r.get("icon"),
                 category=r.get("category", ""), source=r.get("source", ""),
                 works=True if r.get("status") == "works" else None, store=store)


def _from_klondike(r: dict, store: str):
    if r.get("component_type") != "Skill" or r.get("archived") or not r.get("on_pypi"):
        return None
    texts = {"en-us": {"name": r.get("name") or r["package_name"], "description": r.get("description", ""),
                       "examples": r.get("examples") or []}}
    return Skill(package=r["package_name"], texts=texts, icon=r.get("icon"),
                 category=(r.get("category") or "").lower(), source=r.get("source", ""),
                 store=store, tags=r.get("tags") or [])


def parse(records: list, store: str) -> list:
    """The skills in a store's list, whichever of the two formats it is."""
    out = []
    for r in records if isinstance(records, list) else []:
        if not isinstance(r, dict):
            continue
        if "texts" in r and "package" in r:
            s = _from_emkay(r, store)
        elif "package_name" in r:
            s = _from_klondike(r, store)
        else:
            s = None
        if s:
            out.append(s)
    return out


class Stores:
    """The skills of every configured store, fetched when needed and kept
    CACHE_SECONDS. The first store's record wins for a package in several."""

    def __init__(self, stores: list):
        self.stores = stores          # [{"name": ..., "url": ...}]
        self._skills = None
        self._at = 0

    def skills(self) -> list:
        if self._skills is None or time.time() - self._at > CACHE_SECONDS:
            seen, out = set(), []
            for store in self.stores:
                try:
                    r = requests.get(store["url"], timeout=20)
                    r.raise_for_status()
                    found = parse(r.json(), store.get("name") or store["url"])
                except Exception:
                    continue             # a store that is down leaves the others
                for s in found:
                    if s.package not in seen:
                        seen.add(s.package)
                        out.append(s)
            if out or self._skills is None:
                self._skills, self._at = out, time.time()
        return self._skills

    def find(self, package_or_name: str, lang: str):
        """The skill whose package or name is closest to what was said."""
        want = _norm(package_or_name)
        best, best_score = None, 0.0
        for s in self.skills():
            for cand in (s.package, s.text(lang)["name"], s.text("en-us")["name"]):
                c = _norm(cand).replace("ovos skill ", "").replace(" skill", "")
                score = _overlap(want.replace(" skill", ""), c)
                if score > best_score:
                    best, best_score = s, score
        return best if best_score >= 0.6 else None


WORD = re.compile(r"\w+", re.UNICODE)


def _norm(text: str) -> str:
    return " ".join(WORD.findall((text or "").lower().replace("-", " ").replace("_", " ")))


def _overlap(a: str, b: str) -> float:
    """How much of `a`'s words are in `b` (by their first five letters)."""
    aw = [w[:5] for w in a.split() if len(w) > 1]
    bw = {w[:5] for w in b.split()}
    return sum(w in bw for w in aw) / len(aw) if aw else 0.0


def search(skills: list, query: str, lang: str, words: dict, top: int = 4) -> list:
    """The skills that best match `query`: [(score, skill)], best first.

    `words` is the language's search words: {"vejret": "weather", ...}; a
    query word found there also searches for its English word."""
    terms = []
    for w in WORD.findall(query.lower()):
        if len(w) < 3:
            continue
        terms.append(w[:5])
        for k, v in words.items():
            if w.startswith(k[:5]) or k.startswith(w[:5]):
                terms.extend(x[:5] for x in WORD.findall(v.lower()))
    terms = list(dict.fromkeys(terms))
    if not terms:
        return []
    scored = []
    for s in skills:
        local, en = s.text(lang), s.text("en-us")
        name = {w[:5] for w in WORD.findall(f"{local['name']} {en['name']} {s.package}".lower())}
        tags = {w[:5] for w in WORD.findall(f"{s.category} {' '.join(s.tags)}".lower())}
        body = {w[:5] for w in WORD.findall(" ".join(
            [local["description"], en["description"], *local["examples"], *en["examples"]]).lower())}
        score = sum(3 * (t in name) + 2 * (t in tags) + (t in body) for t in terms)
        if score:
            scored.append((score + (0.5 if s.works else 0), s))
    scored.sort(key=lambda x: -x[0])
    return scored[:top]


def load_words(path) -> dict:
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}
