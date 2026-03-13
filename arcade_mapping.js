(function () {
    // Vertaling van Hyperspin/MAME naar MakeCode Arcade
    const keyMap = {
        'Control': 'z',      // Knop 1 -> A
        'Alt': 'x',      // Knop 2 -> B
        ' ': 'z',      // Spatie -> A
        'Shift': 'x',      // Knop 3 -> B
        '1': 'Enter',  // Start 1 -> Menu
        'Escape': 'Escape'  // Knop 6 -> Terug naar menu
    };

    const injectKey = (targetKey) => {
        const iframe = document.querySelector('iframe');
        if (iframe && iframe.contentWindow) {
            ['keydown', 'keyup'].forEach(type => {
                const event = new KeyboardEvent(type, {
                    key: targetKey,
                    keyCode: targetKey.toUpperCase().charCodeAt(0),
                    code: 'Key' + targetKey.toUpperCase(),
                    bubbles: true,
                    composed: true
                });
                // We sturen het event direct naar de content van het iframe
                iframe.contentWindow.dispatchEvent(event);
            });
        }
    };

    // Luister naar toetsen op de 'parent' pagina
    window.addEventListener('keydown', function (e) {
        if (keyMap[e.key]) {
            console.log("MATCH! Ik vertaal " + e.key + " naar " + keyMap[e.key]); // Voeg dit toe
            e.preventDefault();
            injectKey(keyMap[e.key]);
        } else {
            console.log("Geen match voor: " + e.key); // Handig om te zien wat je IPAC uitstuurt
        }
    }, true);

    // Forceer focus zodra een iframe verschijnt
    const observer = new MutationObserver((mutations) => {
        mutations.forEach((mutation) => {
            mutation.addedNodes.forEach((node) => {
                if (node.tagName === 'IFRAME') {
                    node.focus();
                    // Extra check: zorg dat het spel de focus houdt bij clicks
                    node.addEventListener('load', () => node.focus());
                }
            });
        });
    });

    observer.observe(document.body, { childList: true, subtree: true });
})();