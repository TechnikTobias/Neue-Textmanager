const befehlContainer = document.getElementById('befehlContainer');
const neuerBefehlButton = document.getElementById('neuerBefehlButton');
const weiterButton = document.getElementById('weiterButton');

neuerBefehlButton.addEventListener('click', () => {
    const newBefehl = document.createElement('div');
    newBefehl.className = 'befehl';
    newBefehl.innerHTML = `
        <span class="up-arrow">&#9650;</span>
        <span class="down-arrow">&#9660;</span>
        <span class="befehl-text">Neuer Befehl</span>
    `;

    befehlContainer.appendChild(newBefehl);

    // Event-Listener für das Ändern der Reihenfolge nach oben
    const upArrow = newBefehl.querySelector('.up-arrow');
    upArrow.addEventListener('click', () => {
        const previousSibling = newBefehl.previousElementSibling;
        if (previousSibling) {
            befehlContainer.insertBefore(newBefehl, previousSibling);
        }
    });

    // Event-Listener für das Ändern der Reihenfolge nach unten
    const downArrow = newBefehl.querySelector('.down-arrow');
    downArrow.addEventListener('click', () => {
        const nextSibling = newBefehl.nextElementSibling;
        if (nextSibling) {
            befehlContainer.insertBefore(nextSibling, newBefehl);
        }
    });
});

weiterButton.addEventListener('click', () => {
    const befehle = document.querySelectorAll('.befehl .befehl-text');

    befehle.forEach((befehl, index) => {
        console.log("Führe Befehl aus: " + befehl.textContent);
        // Hier können Sie den Befehl ausführen oder andere Aktionen durchführen
    });
});
