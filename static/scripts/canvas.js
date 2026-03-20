// ── Air Canvas Launch ──
// Calls Flask /launch-canvas → Flask runs AI_VirtualPainter.py as subprocess
// The cv2 window opens separately. Browser just shows this launch page.

const launchBtn  = document.getElementById('launchBtn');
const statusDot  = document.getElementById('statusDot');
const statusText = document.getElementById('statusText');

function launchCanvas() {
  launchBtn.disabled = true;
  statusText.textContent = 'Launching...';

  fetch('/launch-canvas')
    .then(r => r.json())
    .then(data => {
      if (data.status === 'launched') {
        statusDot.classList.add('live');
        statusText.textContent = 'Painter is running — check your screen! Press Q to quit.';
        launchBtn.textContent  = 'Painter Running';
      } else {
        statusDot.classList.add('error');
        statusText.textContent = 'Error: ' + (data.message || 'Could not launch painter.');
        launchBtn.disabled = false;
      }
    })
    .catch(() => {
      statusDot.classList.add('error');
      statusText.textContent = 'Could not reach server. Is Flask running?';
      launchBtn.disabled = false;
    });
}