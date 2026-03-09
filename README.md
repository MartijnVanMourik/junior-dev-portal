# Arcade Studio Junior Dev Portal & Kiosk

Dit project bestaat uit twee gekoppelde hoofdcomponenten die samen een complete leer- en showcase-omgeving vormen voor het bouwen van retrogames met Microsoft MakeCode Arcade.

## 1. Arcade Studio Junior Dev Portal (`index.html`)
Een educatieve, stapsgewijze portal die is ontworpen als lesmateriaal voor leerlingen (Junior Devs).
 
- **Doel:** In 7 weken leren werken met Microsoft MakeCode Arcade en het van scratch af opbouwen van een eigen werkende game.
- **Opzet:** Het is een visuele en interactieve gids (course) die de theorie, stappenplannen en opdrachten hapklaar aan de leerlingen aanbiedt. 
- **Eindresultaat:** Aan het einde van de cyclus hebben de leerlingen een eigen retro-game geprogrammeerd en begrijpen ze de basisconcepten van game development.

## 2. Arcade Kiosk (`kiosk.html`)
Een stand-alone browser-gebaseerde "launcher", ontworpen om de eindresultaten van de leerlingen te presenteren op een fysieke arcadekast met Porteus Kiosk.

- **Seamless Game Embedding:** Laadt MakeCode Arcade spellen direct ("bezel-free") in fullscreen via de `---run` URL.
- **Carrousel Weergave:** Een strakke horizontale weergavelijst waardoor de aangeboden games overzichtelijk worden gepresenteerd en makkelijk met the joystick kunnen worden gekozen.
- **Hardware Controller Ready:** Ingebouwde Gamepad API polling om fysieke arcade-joysticks en knoppen te ondersteunen (waarmee spellen direct zonder muis/toetsenbord kunnen worden gestart en gesloten).
- **Kiosk Modus:** Bevat geen externe weblinks (Kiosk-trap), waardoor leerlingen niet onbedoeld de veilige afspeelomgeving op de fysieke kast kunnen verlaten.
- **Dynamische Spellenlijst:** Spellen kunnen eenvoudig worden toegevoegd via Share ID's in het `assets/games.json` bestand.
## 3. Spellen Inleveren en Archiveren (De Workflow)
De games van leerlingen worden volledig automatisch aan de Arcadekast toegevoegd via een CSV-bestand.

### Halverwege/Aan het einde van de cursus:
1. Laat leerlingen hun game-titel, naam en MakeCode Share-link inleveren. 
2. Je kunt hiervoor bijvoorbeeld deze **[Gedeelde Excel-lijst op SharePoint](https://trinitascollege-my.sharepoint.com/:x:/g/personal/m_vanmourik_trinitascollege_nl/IQBeWO164CdNSpKi7DTAPTDzAYAK2oH0uf5I2N3Ed6Z-QbE?e=ahEkN5)** gebruiken (zorg dat leerlingen bewerkrechten hebben).
3. Download de antwoorden uit Excel als **CSV (Kommagescheiden waarden)**. Zorg dat de kolommen `Titel`, `Leerling` en `Link` heten.
4. Upload en overschrijf het bestand `datasources/ingeleverde_games.csv` in deze GitHub repository met de nieuwe data.
5. GitHub Actions draait nu automatisch op de achtergrond. Het Python-script leest de CSV uit, genereert de afbeeldingen en plaatst alle data in `datasources/[huidig_jaar]/games.json`. De kast is direct geüpdatet!

### Een nieuw schooljaar starten (Archiveren):
Aan het einde van het huidige jaar bereid je de omgeving als volgt voor op de nieuwe lichting:
1. Kopieer alle definitieve Share-links van het huidige jaar (uit de CSV of portal) en plak ze als platte tekst onder elkaar in `datasources/[huidig_jaar]/links.txt`. Dit bevriest de games van dit jaar als **Archief**.
2. Maak in de map `datasources/` een nieuwe (lege) map aan voor het komende jaar (bijv. `2026-2027`).
3. Maak het bestand `datasources/ingeleverde_games.csv` weer helemaal leeg (laat alleen de kolomkoppen `titel,leerling,link` staan).
4. Zodra je nieuwe games uploadt in de CSV, zal het script deze automatisch toewijzen aan de map van het *nieuwste* schooljaar.

## Lokaal Ontwikkelen en Testen
Vanwege de (JSON/Assets) fetch-opdrachten voor de Kiosk is een lokale HTTP-server vereist, anders werpt de browser 'CORS' foutmeldingen op:

```bash
# Starten via Python 3 (in de map van dit project)
python3 -m http.server 8000
```

- Bezoek `http://localhost:8000/index.html` om de educatieve portal te zien.
- Bezoek `http://localhost:8000/kiosk.html` om de arcadekast launcher in de browser te testen en je Joystick te calibreren.
