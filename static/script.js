// ── Scroll reveal ──
const observer = new IntersectionObserver(
    entries => entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible'); }),
    { threshold: 0.12 }
  );
  document.querySelectorAll('.reveal').forEach(el => observer.observe(el));

  // ── Smooth anchor scroll ──
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', e => {
      e.preventDefault();
      document.querySelector(a.getAttribute('href'))?.scrollIntoView({ behavior: 'smooth' });
    });
  });

  // ── Launch Air Canvas (opens OpenCV window via Flask) ──
  function launchCanvas(e) {
    e.preventDefault();
    showToast('🖐️ Launching Air Canvas...', 'Painter window opening on your screen.');

    fetch('/launch-canvas')
      .then(r => r.json())
      .then(data => {
        if (data.status === 'launched') {
          showToast('✅ Air Canvas is running!', 'Check your screen — press Q to quit.');
        } else {
          showToast('❌ Launch failed', data.message || 'Something went wrong.');
        }
      })
      .catch(() => showToast('❌ Could not reach server', 'Make sure Flask is running.'));
  }

  // ── Toast notification ──
  function showToast(title, subtitle) {
    // Remove existing toast
    document.querySelector('.toast')?.remove();

    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.innerHTML = `<strong>${title}</strong><span>${subtitle}</span>`;
    document.body.appendChild(toast);

    // Animate in
    requestAnimationFrame(() => toast.classList.add('toast-show'));

    // Auto-dismiss after 4s
    setTimeout(() => {
      toast.classList.remove('toast-show');
      setTimeout(() => toast.remove(), 400);
    }, 4000);
  }
