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

// Navigation mobile (bouton Menu + ouverture/fermeture)
(function setupMobileNav() {
    const sidebar = document.querySelector('.sidebar');
    if (!sidebar) return;

    const MOBILE_MAX_WIDTH = 768;
    const mq = window.matchMedia(`(max-width: ${MOBILE_MAX_WIDTH}px)`);

    function closeNav() {
        document.body.classList.remove('nav-open');
    }

    function openNav() {
        document.body.classList.add('nav-open');
    }

    function removeButtonIfExists() {
        const existing = document.getElementById('mobile-nav-toggle');
        if (existing) existing.remove();
    }

    function ensureButton() {
        if (document.getElementById('mobile-nav-toggle')) return;

        const btn = document.createElement('button');
        btn.id = 'mobile-nav-toggle';
        btn.type = 'button';
        btn.className = 'mobile-nav-toggle';
        btn.setAttribute('aria-label', 'Ouvrir le menu');
        btn.innerHTML = '<i class="fas fa-bars" aria-hidden="true"></i><span>Menu</span>';

        // On insère au début du body
        document.body.insertBefore(btn, document.body.firstChild);

        btn.addEventListener('click', () => {
            const isOpen = document.body.classList.contains('nav-open');
            if (isOpen) closeNav();
            else openNav();
        });

        // Ferme quand on clique sur un lien
        sidebar.querySelectorAll('a').forEach((a) => {
            a.addEventListener('click', () => closeNav());
        });

        // Ferme en cliquant en dehors
        document.addEventListener('click', (e) => {
            const isOpen = document.body.classList.contains('nav-open');
            if (!isOpen) return;
            const clickedInsideSidebar = e.target && e.target.closest && e.target.closest('.sidebar');
            const clickedToggle = e.target && e.target.closest && e.target.closest('#mobile-nav-toggle');
            if (!clickedInsideSidebar && !clickedToggle) closeNav();
        });
    }

    function sync() {
        if (mq.matches) {
            ensureButton();
            closeNav();
        } else {
            removeButtonIfExists();
            closeNav();
        }
    }

    // Sync initial
    sync();

    // Écoute changements de taille
    if (mq.addEventListener) mq.addEventListener('change', sync);
    else mq.addListener(sync);
})();

// Branchement interactif (parcours) - page À propos
(function setupCareerBranch() {
    const branches = document.querySelectorAll('.career-branch');
    if (!branches || branches.length === 0) return;

    function setActive(branchEl, step) {
        const nodes = branchEl.querySelectorAll('.career-node');
        const steps = branchEl.querySelectorAll('.career-panel-step');

        nodes.forEach((node) => {
            const isActive = node.getAttribute('data-step') === step;
            node.classList.toggle('is-active', isActive);
            node.setAttribute('aria-selected', isActive ? 'true' : 'false');
        });

        steps.forEach((panelStep) => {
            const isActive = panelStep.getAttribute('data-step') === step;
            panelStep.classList.toggle('is-active', isActive);
        });
    }

    branches.forEach((branchEl) => {
        const nodes = branchEl.querySelectorAll('.career-node');
        if (!nodes || nodes.length === 0) return;

        const initialNode = branchEl.querySelector('.career-node[aria-selected="true"]') || nodes[0];
        const initialStep = initialNode ? initialNode.getAttribute('data-step') : null;
        if (!initialStep) return;

        // Initialisation
        setActive(branchEl, initialStep);

        // Interaction
        nodes.forEach((node) => {
            node.addEventListener('click', () => {
                const step = node.getAttribute('data-step');
                if (!step) return;
                setActive(branchEl, step);
            });
        });
    });
})();
