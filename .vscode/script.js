// Configuration de l'effet Matrix
const canvas = document.getElementById('matrix-bg');
const ctx = canvas.getContext('2d');

// Ajuster la taille du canvas
function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}

// Initialiser le canvas
resizeCanvas();
window.addEventListener('resize', resizeCanvas);

// Caractères binaires uniquement
const chars = '01';
const charArray = chars.split('');

// Configuration des colonnes
const fontSize = 14;
const columns = canvas.width / fontSize;
const drops = [];

// Initialiser les positions de départ
for (let i = 0; i < columns; i++) {
    drops[i] = Math.floor(Math.random() * canvas.height/fontSize);
}

// Fonction de dessin principale
function draw() {
    // Fond semi-transparent pour créer l'effet de fade
    ctx.fillStyle = 'rgba(10, 25, 47, 0.05)';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Style des caractères
    ctx.fillStyle = '#64ffda'; // Couleur d'accent
    ctx.font = fontSize + 'px monospace';

    // Dessiner les caractères
    for (let i = 0; i < drops.length; i++) {
        // Caractère aléatoire binaire
        const char = charArray[Math.floor(Math.random() * charArray.length)];
        
        // Position du caractère
        const x = i * fontSize;
        const y = drops[i] * fontSize;

        // Dessiner avec effet de luminosité
        ctx.shadowBlur = 5;
        ctx.shadowColor = '#64ffda';
        ctx.fillText(char, x, y);
        ctx.shadowBlur = 0;

        // Réinitialiser la position ou faire descendre
        if (y > canvas.height && Math.random() > 0.975) {
            drops[i] = 0;
        }
        drops[i]++;
    }
}

// Animer
function animate() {
    draw();
    requestAnimationFrame(animate);
}

// Démarrer l'animation
animate(); 
