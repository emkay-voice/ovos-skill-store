# <img src='res/icon.png' width='50' height='50' style='vertical-align:bottom'/> Skill store

An [OpenVoiceOS](https://openvoiceos.org) skill to find and install skills
by voice, from one or more skill stores. The screen shows each skill it
finds as a card: its icon, what it does, and a few of the things you can
say to it, as speech bubbles.

Made for [Emkay](https://github.com/emkay-voice/emkay), OpenVoiceOS in the
browser, whose store (https://store.emkay.ai) only lists what works there.
It is generic: the stores are a setting.

## Usage

```
"Find a skill for the weather"     "Find en skill til vejret"
"Is there a skill for jokes?"      "Er der en skill til vittigheder?"
"Install the joke skill"           "Installer vittigheds-skillen"
"Recommend some skills"            "Anbefal nogle skills"
```

- **Search** matches your words against each skill's name, description,
  examples and category, in your language and in English. Each language has
  a few search words of its own (`locale/<lang>/search_words.json`), so
  "vejret" also finds "weather" when a skill is only described in English.
  Skills found working in Emkay come first.
- **Install** asks before it installs ("Shall I install Jokes?"), then
  installs the way the control panel does, through ovos-core's own installer
  (`ovos.pip.install`), and says what to try once it is in.
- **Recommend** picks a few tested skills you don't have yet.

In all twelve languages Emkay ships; the translations other than English and
Danish are in [`tools/translations.py`](tools/translations.py).

## Stores

`stores` in the skill's settings: a list of `{"name": ..., "url": ...}`, or
a comma-separated string of URLs. Default: the Emkay store. Two list formats
are read, told apart by their records:

| store | URL | format |
|---|---|---|
| Emkay | `https://store.emkay.ai/data/skills.json` | texts per language, and whether each skill works in Emkay |
| ovos-klondike-mercantile | `https://andlo.github.io/ovos-klondike-mercantile/skills.json` | every OVOS skill found on GitHub, in English |

```json
{"stores": [
  {"name": "Emkay", "url": "https://store.emkay.ai/data/skills.json"},
  {"name": "Klondike", "url": "https://andlo.github.io/ovos-klondike-mercantile/skills.json"}
]}
```

Stores are read in that order; a skill in more than one keeps the first
store's record. A store that cannot be reached leaves the others.

Installing needs ovos-core's installer with pip allowed
(`skills.installer.allow_pip`), as for the control panel.

The setting has a form on the Skills page of the [control panel](https://github.com/OpenVoiceOS/ovos-control-panel), in the languages the
skill speaks (`settingsmeta.json`, with its texts in `locale/<lang>/controlpanel.json`).

## License

Apache-2.0
