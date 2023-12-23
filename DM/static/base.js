function afficherToutesLesDonnees() {
    const affichageTableau = document.getElementById('affichageTableau');
    const tableau = document.getElementById('tableau');

    fetch('/api/v1/resources/questions_reponses/all')
        .then(response => response.json())
        .then(data => {
            data.forEach(row => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${row.question}</td>
                    <td>${row.reponse}</td>
                    <td>${row.niveau}</td>
                `;
                tableau.appendChild(tr);
            });

            affichageTableau.style.display = 'block';
        })
}

function retournerPageAccueil() {
    const affichageTableau = document.getElementById('affichageTableau');
    const accueil = document.getElementById('accueil');

    affichageTableau.style.display = 'none';
    accueil.style.display = 'block';
}