"""Writes the intents, dialogs and search words for the languages Emkay ships
besides English and Danish (those are in ovos_skill_store/locale/ by hand),
so they can be reviewed and corrected in one place. From the repository root:

    python tools/translations.py
"""
import json
from pathlib import Path

KEYS = ("found", "nothing_found", "recommend", "recommend_title", "nothing_to_recommend", "not_found",
        "already_installed", "confirm_install", "not_installing", "installing", "install_failed",
        "installed", "installed_try", "badge_works", "badge_installed", "and")

T = {
"de-DE": dict(
 search=["finde einen skill (für|zum|über) {query}", "gibt es einen skill (für|zum|über) {query}", "suche im [skill] store nach {query}", "welche skills gibt es für {query}"],
 install=["installiere den {name} skill", "installiere den skill {name}", "füge den {name} skill hinzu", "installiere {name}"],
 recommend=["empfiehl [mir] (einen|ein paar) skills", "welche skills empfiehlst du", "was ist gut im [skill] store", "zeig mir ein paar skills"],
 d=["Ich habe {count} gefunden: {list}. Sag installieren und den Namen, um einen hinzuzufügen.", "Ich habe keinen Skill für {query} gefunden.",
    "Du könntest {list} ausprobieren. Sag installieren und den Namen, um einen hinzuzufügen.", "Einen Versuch wert", "Ich habe nichts Neues zu empfehlen; die getesteten hast du schon.",
    "Ich habe keinen Skill namens {name} im Store gefunden.", "{name} ist schon installiert.", "Soll ich {name} installieren?", "Gut, ich installiere {name} nicht.",
    "Ich installiere {name}. Das kann eine Minute dauern.", "Die Installation von {name} hat nicht geklappt. Das Protokoll in den Einstellungen sagt vielleicht warum.",
    "{name} ist installiert.", "{name} ist installiert. Sag zum Beispiel: {example}", "läuft hier", "installiert", "und"],
 words={"wetter": "weather forecast", "nachrichten": "news", "musik": "music", "radio": "radio", "licht": "light lights", "lampe": "lamp light", "timer": "timer", "wecker": "alarm", "erinnerung": "reminder", "witz": "joke", "witze": "jokes", "spiel": "game", "quiz": "quiz trivia", "geschichte": "story stories", "märchen": "fairy tale", "buch": "book", "lernen": "learn", "mathe": "math", "rechnen": "calculator", "übersetzen": "translate", "kalender": "calendar", "einkauf": "shopping list", "uhrzeit": "time clock", "datum": "date", "wissen": "knowledge wikipedia", "rezept": "recipe cooking"},
 name="Skill-Store", desc="Skills per Stimme finden und installieren, aus einem oder mehreren Skill-Stores; der Bildschirm zeigt jeden mit Symbol und was man zu ihm sagen kann.",
 ex=["Finde einen Skill für das Wetter", "Installiere den Witz-Skill", "Empfiehl mir ein paar Skills"]),
"nl-NL": dict(
 search=["zoek een skill (voor|om|over) {query}", "is er een skill (voor|om|over) {query}", "zoek in de [skill] winkel naar {query}", "welke skills zijn er voor {query}"],
 install=["installeer de {name} skill", "installeer de skill {name}", "voeg de {name} skill toe", "installeer {name}"],
 recommend=["(raad|beveel) [me] (een|wat) skills aan", "welke skills raad je aan", "wat is goed in de [skill] winkel", "laat me wat skills zien"],
 d=["Ik heb er {count} gevonden: {list}. Zeg installeer en de naam om er een toe te voegen.", "Ik heb geen skill voor {query} gevonden.",
    "Je kunt {list} proberen. Zeg installeer en de naam om er een toe te voegen.", "Het proberen waard", "Ik heb niets nieuws aan te raden; de geteste heb je al.",
    "Ik kon geen skill met de naam {name} in de winkel vinden.", "{name} is al geïnstalleerd.", "Zal ik {name} installeren?", "Goed, ik installeer {name} niet.",
    "Ik installeer {name}. Dat kan een minuut duren.", "Het installeren van {name} is niet gelukt. Het logboek in de instellingen zegt misschien waarom.",
    "{name} is geïnstalleerd.", "{name} is geïnstalleerd. Zeg bijvoorbeeld: {example}", "werkt hier", "geïnstalleerd", "en"],
 words={"weer": "weather forecast", "nieuws": "news", "muziek": "music", "radio": "radio", "licht": "light lights", "lamp": "lamp light", "timer": "timer", "wekker": "alarm", "herinnering": "reminder", "grap": "joke", "grappen": "jokes", "spel": "game", "quiz": "quiz trivia", "verhaal": "story stories", "sprookje": "fairy tale", "boek": "book", "leren": "learn", "rekenen": "calculator math", "vertalen": "translate", "agenda": "calendar", "boodschappen": "shopping list", "tijd": "time clock", "datum": "date", "kennis": "knowledge wikipedia", "recept": "recipe cooking"},
 name="Skillwinkel", desc="Skills zoeken en installeren met je stem, uit een of meer skillwinkels; het scherm toont elke met icoon en wat je ertegen kunt zeggen.",
 ex=["Zoek een skill voor het weer", "Installeer de grappen-skill", "Raad me wat skills aan"]),
"fr-FR": dict(
 search=["trouve une skill (pour|sur) {query}", "y a-t-il une skill (pour|sur) {query}", "cherche dans la boutique [de skills] {query}", "quelles skills y a-t-il pour {query}"],
 install=["installe la skill {name}", "installe {name}", "ajoute la skill {name}"],
 recommend=["(recommande|suggère)[-moi] (une|des) skills", "quelles skills recommandes-tu", "qu'y a-t-il de bien dans la boutique", "montre-moi des skills"],
 d=["J'en ai trouvé {count} : {list}. Dis installe et le nom pour en ajouter une.", "Je n'ai pas trouvé de skill pour {query}.",
    "Tu pourrais essayer {list}. Dis installe et le nom pour en ajouter une.", "À essayer", "Je n'ai rien de nouveau à recommander ; tu as déjà celles qui sont testées.",
    "Je n'ai pas trouvé de skill appelée {name} dans la boutique.", "{name} est déjà installée.", "J'installe {name} ?", "D'accord, je n'installe pas {name}.",
    "J'installe {name}. Ça peut prendre une minute.", "L'installation de {name} n'a pas marché. Le journal des réglages dira peut-être pourquoi.",
    "{name} est installée.", "{name} est installée. Essaie de dire : {example}", "marche ici", "installée", "et"],
 words={"météo": "weather forecast", "temps": "weather", "actualités": "news", "infos": "news", "musique": "music", "radio": "radio", "lumière": "light lights", "lampe": "lamp light", "minuteur": "timer", "réveil": "alarm", "rappel": "reminder", "blague": "joke", "blagues": "jokes", "jeu": "game", "quiz": "quiz trivia", "histoire": "story stories", "conte": "fairy tale", "livre": "book", "apprendre": "learn", "calcul": "calculator math", "traduire": "translate", "agenda": "calendar", "courses": "shopping list", "heure": "time clock", "date": "date", "recette": "recipe cooking"},
 name="Boutique de skills", desc="Trouver et installer des skills à la voix, depuis une ou plusieurs boutiques ; l'écran montre chacune avec son icône et ce qu'on peut lui dire.",
 ex=["Trouve une skill pour la météo", "Installe la skill des blagues", "Recommande-moi des skills"]),
"es-ES": dict(
 search=["busca una skill (para|de|sobre) {query}", "hay alguna skill (para|de|sobre) {query}", "busca en la tienda [de skills] {query}", "qué skills hay para {query}"],
 install=["instala la skill {name}", "instala {name}", "añade la skill {name}"],
 recommend=["(recomiéndame|sugiéreme) (una|unas) skills", "qué skills recomiendas", "qué hay de bueno en la tienda", "enséñame unas skills"],
 d=["He encontrado {count}: {list}. Di instala y el nombre para añadir una.", "No he encontrado ninguna skill para {query}.",
    "Podrías probar {list}. Di instala y el nombre para añadir una.", "Vale la pena probar", "No tengo nada nuevo que recomendar; ya tienes las probadas.",
    "No he encontrado ninguna skill llamada {name} en la tienda.", "{name} ya está instalada.", "¿Instalo {name}?", "Vale, no instalo {name}.",
    "Instalando {name}. Puede tardar un minuto.", "No se ha podido instalar {name}. El registro de los ajustes puede decir por qué.",
    "{name} está instalada.", "{name} está instalada. Prueba a decir: {example}", "funciona aquí", "instalada", "y"],
 words={"tiempo": "weather forecast", "clima": "weather", "noticias": "news", "música": "music", "radio": "radio", "luz": "light lights", "lámpara": "lamp light", "temporizador": "timer", "alarma": "alarm", "recordatorio": "reminder", "chiste": "joke", "chistes": "jokes", "juego": "game", "trivial": "quiz trivia", "cuento": "story fairy tale", "historia": "story", "libro": "book", "aprender": "learn", "calcular": "calculator math", "traducir": "translate", "calendario": "calendar", "compra": "shopping list", "hora": "time clock", "fecha": "date", "receta": "recipe cooking"},
 name="Tienda de skills", desc="Busca e instala skills con la voz, desde una o varias tiendas; la pantalla muestra cada una con su icono y lo que le puedes decir.",
 ex=["Busca una skill para el tiempo", "Instala la skill de chistes", "Recomiéndame unas skills"]),
"it-IT": dict(
 search=["trova una skill (per|su) {query}", "c'è una skill (per|su) {query}", "cerca nel negozio [di skill] {query}", "che skill ci sono per {query}"],
 install=["installa la skill {name}", "installa {name}", "aggiungi la skill {name}"],
 recommend=["(consigliami|suggeriscimi) (una|qualche) skill", "che skill mi consigli", "cosa c'è di bello nel negozio", "fammi vedere qualche skill"],
 d=["Ne ho trovate {count}: {list}. Di' installa e il nome per aggiungerne una.", "Non ho trovato skill per {query}.",
    "Potresti provare {list}. Di' installa e il nome per aggiungerne una.", "Da provare", "Non ho niente di nuovo da consigliare; quelle provate le hai già.",
    "Non ho trovato una skill chiamata {name} nel negozio.", "{name} è già installata.", "Installo {name}?", "Va bene, non installo {name}.",
    "Installo {name}. Può volerci un minuto.", "L'installazione di {name} non è riuscita. Il registro delle impostazioni forse dice perché.",
    "{name} è installata.", "{name} è installata. Prova a dire: {example}", "funziona qui", "installata", "e"],
 words={"meteo": "weather forecast", "tempo": "weather", "notizie": "news", "musica": "music", "radio": "radio", "luce": "light lights", "lampada": "lamp light", "timer": "timer", "sveglia": "alarm", "promemoria": "reminder", "barzelletta": "joke", "barzellette": "jokes", "gioco": "game", "quiz": "quiz trivia", "storia": "story stories", "fiaba": "fairy tale", "libro": "book", "imparare": "learn", "calcolare": "calculator math", "tradurre": "translate", "calendario": "calendar", "spesa": "shopping list", "ora": "time clock", "data": "date", "ricetta": "recipe cooking"},
 name="Negozio di skill", desc="Trova e installa skill con la voce, da uno o più negozi; lo schermo mostra ognuna con la sua icona e cosa le puoi dire.",
 ex=["Trova una skill per il meteo", "Installa la skill delle barzellette", "Consigliami qualche skill"]),
"pt-BR": dict(
 search=["encontre uma skill (para|de|sobre) {query}", "tem alguma skill (para|de|sobre) {query}", "procure na loja [de skills] {query}", "que skills existem para {query}"],
 install=["instale a skill {name}", "instale {name}", "adicione a skill {name}"],
 recommend=["(recomende|sugira)[-me] (uma|algumas) skills", "que skills você recomenda", "o que tem de bom na loja", "mostre algumas skills"],
 d=["Encontrei {count}: {list}. Diga instale e o nome para adicionar uma.", "Não encontrei nenhuma skill para {query}.",
    "Você pode experimentar {list}. Diga instale e o nome para adicionar uma.", "Vale a pena experimentar", "Não tenho nada novo para recomendar; você já tem as testadas.",
    "Não encontrei uma skill chamada {name} na loja.", "{name} já está instalada.", "Instalo {name}?", "Tudo bem, não vou instalar {name}.",
    "Instalando {name}. Pode levar um minuto.", "Não foi possível instalar {name}. O registro das configurações pode dizer por quê.",
    "{name} está instalada.", "{name} está instalada. Experimente dizer: {example}", "funciona aqui", "instalada", "e"],
 words={"tempo": "weather forecast", "clima": "weather", "notícias": "news", "música": "music", "rádio": "radio", "luz": "light lights", "lâmpada": "lamp light", "timer": "timer", "alarme": "alarm", "lembrete": "reminder", "piada": "joke", "piadas": "jokes", "jogo": "game", "quiz": "quiz trivia", "história": "story stories", "conto": "fairy tale", "livro": "book", "aprender": "learn", "calcular": "calculator math", "traduzir": "translate", "calendário": "calendar", "compras": "shopping list", "hora": "time clock", "data": "date", "receita": "recipe cooking"},
 name="Loja de skills", desc="Encontre e instale skills com a voz, de uma ou mais lojas; a tela mostra cada uma com seu ícone e o que você pode dizer a ela.",
 ex=["Encontre uma skill para o tempo", "Instale a skill de piadas", "Recomende algumas skills"]),
"pt-PT": dict(
 search=["encontra uma skill (para|de|sobre) {query}", "há alguma skill (para|de|sobre) {query}", "procura na loja [de skills] {query}", "que skills há para {query}"],
 install=["instala a skill {name}", "instala {name}", "adiciona a skill {name}"],
 recommend=["(recomenda|sugere)-me (uma|algumas) skills", "que skills recomendas", "o que há de bom na loja", "mostra-me algumas skills"],
 d=["Encontrei {count}: {list}. Diz instala e o nome para adicionar uma.", "Não encontrei nenhuma skill para {query}.",
    "Podes experimentar {list}. Diz instala e o nome para adicionar uma.", "Vale a pena experimentar", "Não tenho nada de novo para recomendar; já tens as testadas.",
    "Não encontrei uma skill chamada {name} na loja.", "{name} já está instalada.", "Instalo {name}?", "Está bem, não instalo {name}.",
    "A instalar {name}. Pode demorar um minuto.", "Não foi possível instalar {name}. O registo das definições pode dizer porquê.",
    "{name} está instalada.", "{name} está instalada. Experimenta dizer: {example}", "funciona aqui", "instalada", "e"],
 words={"tempo": "weather forecast", "meteorologia": "weather", "notícias": "news", "música": "music", "rádio": "radio", "luz": "light lights", "candeeiro": "lamp light", "temporizador": "timer", "alarme": "alarm", "lembrete": "reminder", "anedota": "joke", "anedotas": "jokes", "jogo": "game", "quiz": "quiz trivia", "história": "story stories", "conto": "fairy tale", "livro": "book", "aprender": "learn", "calcular": "calculator math", "traduzir": "translate", "calendário": "calendar", "compras": "shopping list", "hora": "time clock", "data": "date", "receita": "recipe cooking"},
 name="Loja de skills", desc="Encontra e instala skills com a voz, a partir de uma ou mais lojas; o ecrã mostra cada uma com o seu ícone e o que lhe podes dizer.",
 ex=["Encontra uma skill para o tempo", "Instala a skill de anedotas", "Recomenda-me algumas skills"]),
"ca-ES": dict(
 search=["troba una skill (per|de|sobre) {query}", "hi ha alguna skill (per|de|sobre) {query}", "cerca a la botiga [de skills] {query}", "quines skills hi ha per {query}"],
 install=["instal·la la skill {name}", "instal·la {name}", "afegeix la skill {name}"],
 recommend=["(recomana'm|suggereix-me) (una|unes) skills", "quines skills recomanes", "què hi ha de bo a la botiga", "ensenya'm unes skills"],
 d=["N'he trobat {count}: {list}. Digues instal·la i el nom per afegir-ne una.", "No he trobat cap skill per {query}.",
    "Podries provar {list}. Digues instal·la i el nom per afegir-ne una.", "Val la pena provar", "No tinc res de nou per recomanar; ja tens les provades.",
    "No he trobat cap skill anomenada {name} a la botiga.", "{name} ja està instal·lada.", "Instal·lo {name}?", "D'acord, no instal·lo {name}.",
    "Instal·lant {name}. Pot trigar un minut.", "No s'ha pogut instal·lar {name}. El registre dels ajustos potser diu per què.",
    "{name} està instal·lada.", "{name} està instal·lada. Prova de dir: {example}", "funciona aquí", "instal·lada", "i"],
 words={"temps": "weather forecast", "notícies": "news", "música": "music", "ràdio": "radio", "llum": "light lights", "làmpada": "lamp light", "temporitzador": "timer", "alarma": "alarm", "recordatori": "reminder", "acudit": "joke", "acudits": "jokes", "joc": "game", "qüestionari": "quiz trivia", "conte": "story fairy tale", "història": "story", "llibre": "book", "aprendre": "learn", "calcular": "calculator math", "traduir": "translate", "calendari": "calendar", "compra": "shopping list", "hora": "time clock", "data": "date", "recepta": "recipe cooking"},
 name="Botiga de skills", desc="Troba i instal·la skills amb la veu, des d'una o més botigues; la pantalla mostra cadascuna amb la seva icona i què li pots dir.",
 ex=["Troba una skill per al temps", "Instal·la la skill d'acudits", "Recomana'm unes skills"]),
"gl-ES": dict(
 search=["atopa unha skill (para|de|sobre) {query}", "hai algunha skill (para|de|sobre) {query}", "busca na tenda [de skills] {query}", "que skills hai para {query}"],
 install=["instala a skill {name}", "instala {name}", "engade a skill {name}"],
 recommend=["(recoméndame|suxíreme) (unha|unhas) skills", "que skills recomendas", "que hai de bo na tenda", "amósame unhas skills"],
 d=["Atopei {count}: {list}. Di instala e o nome para engadir unha.", "Non atopei ningunha skill para {query}.",
    "Poderías probar {list}. Di instala e o nome para engadir unha.", "Paga a pena probar", "Non teño nada novo que recomendar; xa tes as probadas.",
    "Non atopei ningunha skill chamada {name} na tenda.", "{name} xa está instalada.", "Instalo {name}?", "Vale, non instalo {name}.",
    "Instalando {name}. Pode tardar un minuto.", "Non se puido instalar {name}. O rexistro dos axustes pode dicir por que.",
    "{name} está instalada.", "{name} está instalada. Proba a dicir: {example}", "funciona aquí", "instalada", "e"],
 words={"tempo": "weather forecast", "noticias": "news", "música": "music", "radio": "radio", "luz": "light lights", "lámpada": "lamp light", "temporizador": "timer", "alarma": "alarm", "recordatorio": "reminder", "chiste": "joke", "chistes": "jokes", "xogo": "game", "quiz": "quiz trivia", "conto": "story fairy tale", "historia": "story", "libro": "book", "aprender": "learn", "calcular": "calculator math", "traducir": "translate", "calendario": "calendar", "compra": "shopping list", "hora": "time clock", "data": "date", "receita": "recipe cooking"},
 name="Tenda de skills", desc="Atopa e instala skills coa voz, dende unha ou varias tendas; a pantalla amosa cada unha coa súa icona e o que lle podes dicir.",
 ex=["Atopa unha skill para o tempo", "Instala a skill de chistes", "Recoméndame unhas skills"]),
"eu-ES": dict(
 search=["bilatu skill bat {query}(rako|ri buruz)", "bilatu {query} skill bat", "ba al dago {query} skillik", "bilatu dendan {query}"],
 install=["instalatu {name} skill(a)", "instalatu {name}", "gehitu {name} skill(a)"],
 recommend=["gomendatu (skill bat|skill batzuk)", "zein skill gomendatzen dituzu", "zer dago ona dendan", "erakutsi skill batzuk"],
 d=["{count} aurkitu ditut: {list}. Esan instalatu eta izena bat gehitzeko.", "Ez dut {query} skillik aurkitu.",
    "{list} proba ditzakezu. Esan instalatu eta izena bat gehitzeko.", "Probatzeko modukoak", "Ez daukat ezer berririk gomendatzeko; probatuak badituzu.",
    "Ez dut {name} izeneko skillik aurkitu dendan.", "{name} instalatuta dago dagoeneko.", "{name} instalatu?", "Ados, ez dut {name} instalatuko.",
    "{name} instalatzen. Minutu bat beharko du.", "Ezin izan da {name} instalatu. Ezarpenen erregistroak esan dezake zergatik.",
    "{name} instalatuta dago.", "{name} instalatuta dago. Esan, adibidez: {example}", "hemen dabil", "instalatuta", "eta"],
 words={"eguraldia": "weather forecast", "albisteak": "news", "musika": "music", "irratia": "radio", "argia": "light lights", "lanpara": "lamp light", "tenporizadorea": "timer", "alarma": "alarm", "oroigarria": "reminder", "txistea": "joke", "txisteak": "jokes", "jokoa": "game", "galdetegia": "quiz trivia", "ipuina": "story fairy tale", "istorioa": "story", "liburua": "book", "ikasi": "learn", "kalkulatu": "calculator math", "itzuli": "translate", "egutegia": "calendar", "erosketak": "shopping list", "ordua": "time clock", "data": "date", "errezeta": "recipe cooking"},
 name="Skill denda", desc="Bilatu eta instalatu skillak ahotsez, denda batetik edo gehiagotatik; pantailak bakoitza bere ikonoarekin eta esan diezaiokezunarekin erakusten du.",
 ex=["Bilatu eguraldirako skill bat", "Instalatu txisteen skilla", "Gomendatu skill batzuk"]),
}

ROOT = Path(__file__).parent.parent / "ovos_skill_store" / "locale"
ICON = "https://raw.githubusercontent.com/emkay-voice/ovos-skill-store/main/res/icon.png"
for lang, t in T.items():
    loc = ROOT / lang
    loc.mkdir(parents=True, exist_ok=True)
    for name in ("search", "install", "recommend"):
        (loc / f"{name}.intent").write_text("\n".join(t[name]) + "\n", encoding="utf-8")
    for key, text in zip(KEYS, t["d"]):
        (loc / f"{key}.dialog").write_text(text + "\n", encoding="utf-8")
    (loc / "search_words.json").write_text(json.dumps(t["words"], ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    (loc / "skill.json").write_text(json.dumps({
        "skill_id": "ovos-skill-store.emkay-voice", "source": "https://github.com/emkay-voice/ovos-skill-store",
        "name": t["name"], "description": t["desc"], "examples": t["ex"], "icon": ICON,
        "tags": ["store", "skills", "install", "emkay"]}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(lang)
