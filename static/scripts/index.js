// ── Scroll Reveal ──
const observer = new IntersectionObserver(
  entries => entries.forEach(e => {
    if (e.isIntersecting) e.target.classList.add('visible');
  }),
  { threshold: 0.12 }
);
document.querySelectorAll('.reveal').forEach(el => observer.observe(el));

// ── Smooth Anchor Scroll ──
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', e => {
    const target = document.querySelector(a.getAttribute('href'));
    if (target) { e.preventDefault(); target.scrollIntoView({ behavior: 'smooth' }); }
  });
});

// ── Air Canvas — launch painter ──
function launchCanvas(e) {
  e.preventDefault();
  showToast('🖐️ Launching Air Canvas...', 'Painter window opening on your screen.');

  fetch('/launch-canvas')
    .then(r => r.json())
    .then(data => {
      if (data.status === 'launched') {
        showToast('✅ Painter is running!', 'Press Q on the painter window to quit.');
      } else {
        showToast('❌ Launch failed', data.message || 'Something went wrong.');
      }
    })
    .catch(() => showToast('❌ Could not reach server', 'Make sure Flask is running.'));
}

// ── Snake Game Launcher— launch Game ──
function launchSnakeGame(e) {
  e.preventDefault();
  showToast('🐍 Launching Snake Game...', 'Game window opening on your screen.');

  fetch('/launch-game')
    .then(r => r.json())
    .then(data => {
      if (data.status === 'launched') {
        showToast('✅ Game is running!', 'Press Q on the Game window to quit.');
      } else {
        showToast('❌ Launch failed', data.message || 'Something went wrong.');
      }
    })
    .catch(() => showToast('❌ Could not reach server', 'Make sure Flask is running.'));
}

// ── Quiz Game — launch Quiz Game ──
function launchQuiz(e) {
  e.preventDefault();
  showToast('🖐️ Launching Quiz Game...', 'Quiz window opening on your screen.');

  fetch('/launch-quiz')
    .then(r => r.json())
    .then(data => {
      if (data.status === 'launched') {
        showToast('✅ Quiz is running!', 'Press Q on the Quiz window to quit.');
      } else {
        showToast('❌ Launch failed', data.message || 'Something went wrong.');
      }
    })
    .catch(() => showToast('❌ Could not reach server', 'Make sure Flask is running.'));
}

// ── Toast notification ──
function showToast(title, subtitle) {
  document.querySelector('.toast')?.remove();

  const toast = document.createElement('div');
  toast.className = 'toast';
  toast.innerHTML = `<strong>${title}</strong><span>${subtitle}</span>`;
  document.body.appendChild(toast);

  requestAnimationFrame(() => toast.classList.add('toast-show'));

  setTimeout(() => {
    toast.classList.remove('toast-show');
    setTimeout(() => toast.remove(), 400);
  }, 4000);
}