# Arcade Kiosk Setup (Fossapup64)
Deze repository bevat de configuratie en scripts om van een Fossapup64 (Puppy Linux) installatie een robuuste Arcadekast te maken. De setup maakt gebruik van een Chromium-gebaseerde Kiosk-omgeving met een automatische focus-fix voor MakeCode Arcade iframes.

## 📂 Bestandsstructuur
Plaats de bestanden op de volgende locaties in je Puppy Linux systeem:

- `/root/.Xmodmap` - De toetsenbord-mapping voor de arcade-encoder.
- `/root/Startup/start_arcade.sh` - Het hoofdscript (start automatisch bij inloggen).
- `/root/Startup/stop_arcade.sh` - Het afsluitscript (te koppelen aan een JWM-sneltoets).
- `/root/Startup/arcade_clicker.sh` - De achtergrond-service voor de muis-focus fix.

## 🎹 1. Toetsenbord Mapping (`/root/.Xmodmap`)
Dit bestand vertaalt de rauwe keycodes van de USB-arcade-encoder naar logische toetsen die MakeCode begrijpt.

```text
! Player 1
keycode 111 = Up
keycode 116 = Down
keycode 113 = Left
keycode 114 = Right
keycode 44 = z
keycode 55 = x

! Player 2
keycode 27 = i
keycode 42 = l
keycode 41 = k
keycode 40 = j

! Player 2 Actie knoppen
keycode 38 = u
keycode 39 = o

! Menu & Reset
keycode 9 = Return
keycode 14 = F5
```

## 🚀 2. De Scripts
Zorg dat alle scripts uitvoerbaar zijn met: `chmod +x /root/Startup/*.sh`

### `start_arcade.sh`
Dit script start de omgeving op. Het bevat een Singleton-check om te voorkomen dat er meerdere vensters openen.

```bash
#!/bin/bash
export DISPLAY=:0.0

# Singleton check tegen dubbele windows
LOCKFILE="/tmp/arcade_startup.lock"
if [ -f "$LOCKFILE" ]; then
    exit 0
fi
touch "$LOCKFILE"
trap "rm -f $LOCKFILE" EXIT

# 1. Opschonen en Mapping laden
/root/Startup/stop_arcade.sh > /dev/null 2>&1
sleep 1
[ -f /root/.Xmodmap ] && xmodmap /root/.Xmodmap

# 2. Achtergrond processen
/root/Startup/arcade_clicker.sh &

# 3. Start Chromium (Kiosk Mode)
run-as-spot chromium \
  --kiosk \
  --incognito \
  --bwsi \
  --no-first-run \
  --disable-infobars \
  --disable-session-crashed-bubble \
  --autoplay-policy=no-user-gesture-required \
  "https://martijnvanmourik.github.io/junior-dev-portal/kiosk.html" &

# 4. Fullscreen force (F11)
sleep 6
xdotool key F11

wait
```

### `stop_arcade.sh`
Sluit alles netjes af en herstelt het systeem naar de us indeling.

```bash
#!/bin/bash
export DISPLAY=:0.0

pkill -9 chromium 2>/dev/null
ps aux | grep 'arcade_clicker.sh' | grep -v 'grep' | awk '{print $2}' | xargs kill -9 2>/dev/null
pkill -9 -f arcade_clicker.sh 2>/dev/null

# Herstel naar standaard US keyboard layout
setxkbmap us

rm -f /tmp/arcade_startup.lock
rm -f /tmp/arcade_clicker.pid

echo "Systeem hersteld."
```

### `arcade_clicker.sh`
De "Bliksem-Clicker" die luistert naar `TRIGGER_FOCUS` in de venstertitel om het iframe te activeren.

```bash
#!/bin/bash
export DISPLAY=:0.0

eval $(xdotool getdisplaygeometry --shell)
CENTER_X=$((WIDTH / 2))
CENTER_Y=$((HEIGHT / 2))
PARK_X=$((WIDTH - 1))
PARK_Y=$((HEIGHT - 1))

xdotool mousemove $PARK_X $PARK_Y

while true; do
    WID=$(xdotool search --name "TRIGGER_FOCUS" | head -n 1)
    if [ -n "$WID" ]; then
        xdotool windowactivate --sync $WID \
                mousemove $CENTER_X $CENTER_Y \
                click 1 \
                mousemove $PARK_X $PARK_Y
        sleep 2.5
    fi
    sleep 0.2
done
```

## 🌐 3. Web Interface (`kiosk.html`)
Om de automatische focus te laten werken, moet de web-app de venstertitel wijzigen zodra een game geladen is:

```javascript
// In de startGame() functie van je JS:
iframe.onload = () => {
    setTimeout(() => {
        document.title = "TRIGGER_FOCUS";
        setTimeout(() => { document.title = "Arcade Portal"; }, 2000);
    }, 1000);
};
```

## 🛠 4. Installatie op Fossapup64
1. Kopieer de bestanden naar de juiste mappen.
2. Maak de scripts uitvoerbaar.
3. Voeg een sneltoets toe aan `/root/.jwmrc` om `stop_arcade.sh` aan te roepen (bijv. `Control+Alt+X`).
4. Start de computer opnieuw op.
