const befehlContainer = document.getElementById('befehlContainer');
const neuerBefehlButton = document.getElementById('neuerBefehlButton');
const weiterButton = document.getElementById('weiterButton');

neuerBefehlButton.addEventListener('click', () => {
    const newBefehl = document.createElement('div');
    newBefehl.className = 'befehl';
    newBefehl.textContent = 'Neuer Befehl';
    newBefehl.draggable = true;

    // Event-Listener für das Ziehen des Befehls
    newBefehl.addEventListener('dragstart', (event) => {
        event.dataTransfer.setData('text/plain', event.target.id);
    });

    // Event-Listener für das Bearbeiten des Befehls
    newBefehl.addEventListener('dblclick', () => {
        const newName = prompt('Neuen Namen eingeben:', newBefehl.textContent);
        if (newName !== null) {
            newBefehl.textContent = newName;
        }
    });

    befehlContainer.appendChild(newBefehl);
});

befehlContainer.addEventListener('dragstart', (event) => {
    event.dataTransfer.setData('text/plain', event.target.id);
});

befehlContainer.addEventListener('dragover', (event) => {
    event.preventDefault();
});

befehlContainer.addEventListener('drop', (event) => {
    event.preventDefault();
    const befehlId = event.dataTransfer.getData('text/plain');
    const befehlElement = document.getElementById(befehlId);
    
    // Stellen Sie sicher, dass befehlElement ein gültiges Element ist
    if (befehlElement) {
        befehlContainer.insertBefore(befehlElement, event.target);
    }
});

weiterButton.addEventListener('click', () => {
    const befehle = document.querySelectorAll('.befehl');

    befehle.forEach((befehl, index) => {
        console.log("Führe Befehl aus: " + befehl.textContent);
        // Hier können Sie den Befehl ausführen oder andere Aktionen durchführen
    });
});
