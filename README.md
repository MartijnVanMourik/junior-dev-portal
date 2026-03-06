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
## Lokaal Ontwikkelen en Testen
Vanwege de (JSON/Assets) fetch-opdrachten voor de Kiosk is een lokale HTTP-server vereist, anders werpt de browser 'CORS' foutmeldingen op:

```bash
# Starten via Python 3 (in de map van dit project)
python3 -m http.server 8000
```

- Bezoek `http://localhost:8000/index.html` om de educatieve portal te zien.
- Bezoek `http://localhost:8000/kiosk.html` om de arcadekast launcher in de browser te testen en je Joystick te calibreren.
