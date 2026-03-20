// ═══════════════════════════════════════════
//  MIWS — Gesture Quiz  |  quiz.js
//  MediaPipe runs silently in background.
//  This file only handles browser UI.
// ═══════════════════════════════════════════

// ── DOM refs ──
const detDot       = document.getElementById('detDot');
const detText      = document.getElementById('detText');
const questionNum  = document.getElementById('questionNum');
const progressFill = document.getElementById('progressFill');
const scoreVal     = document.getElementById('scoreVal');
const qCategory    = document.getElementById('qCategory');
const qText        = document.getElementById('qText');
const opts         = [0,1,2,3].map(i => document.getElementById(`opt${i}`));
const optTexts     = [0,1,2,3].map(i => document.getElementById(`optText${i}`));
const hints        = [0,1,2,3,4].map(i => document.getElementById(`h${i}`));  // h0=fist, h1-h4=fingers
const statusBar    = document.getElementById('statusBar');
const statusMsg    = document.getElementById('statusMsg');
const resultOverlay= document.getElementById('resultOverlay');
const finalScore   = document.getElementById('finalScore');
const finalTotal   = document.getElementById('finalTotal');
const resultEmoji  = document.getElementById('resultEmoji');
const resultTitle  = document.getElementById('resultTitle');
const resultMsg    = document.getElementById('resultMsg');

// ── State ──
let selectedOption = null;   // 0-3
let phase          = 'selecting';  // 'selecting' | 'confirmed' | 'result'
let score          = 0;
let total          = 10;
let pollTimer      = null;


// ══════════════════════════════════════════
//  LOAD QUESTION
// ══════════════════════════════════════════
async function loadQuestion() {
  phase = 'selecting';
  selectedOption = null;
  clearOptions();
  setStatus('Show fingers to select · ✊ Fist to confirm', '');

  try {
    const res  = await fetch('/quiz/question');
    const data = await res.json();

    if (data.done) {
      showResult(data.score, data.total);
      return;
    }

    total = data.total;
    score = data.score;

    qCategory.textContent       = data.category;
    qText.textContent           = data.question;
    optTexts.forEach((el, i)    => el.textContent = data.options[i]);
    questionNum.textContent     = `${data.index + 1} / ${total}`;
    progressFill.style.width    = `${(data.index / total) * 100}%`;
    scoreVal.textContent        = score;

  } catch {
    setStatus('Could not load question — is Flask running?', '');
  }
}


// ══════════════════════════════════════════
//  POLL FLASK FOR GESTURE
// ══════════════════════════════════════════
async function pollGesture() {
  if (phase === 'result') return;

  try {
    const res  = await fetch('/quiz/gesture');
    const data = await res.json();
    const f    = data.fingers;   // -1=no hand, 0=fist, 1-4=fingers

    updateDetectionUI(f);

    if (phase === 'selecting') {
      if (f >= 1 && f <= 4) {
        const idx = f - 1;  // convert to 0-indexed
        if (idx !== selectedOption) {
          selectedOption = idx;
          highlightOption(idx);
        }
      } else if (f === 0 && selectedOption !== null) {
        // Fist = confirm
        confirmAnswer();
      }
    }

    // After answer shown, any finger = next question
    if (phase === 'confirmed' && f >= 1 && f <= 4) {
      phase = 'transitioning';
      setTimeout(loadQuestion, 400);
    }

  } catch { /* ignore poll errors silently */ }
}


// ══════════════════════════════════════════
//  CONFIRM ANSWER
// ══════════════════════════════════════════
async function confirmAnswer() {
  if (selectedOption === null || phase !== 'selecting') return;
  phase = 'confirmed';

  try {
    const res  = await fetch('/quiz/answer', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ answer: selectedOption })
    });
    const data = await res.json();

    score = data.score;
    scoreVal.textContent = score;
    progressFill.style.width = `${((data.done ? total : (total - data.total + data.index ?? 0)) / total) * 100}%`;

    // Clear selected state, show correct/wrong
    opts.forEach(o => o.classList.remove('selected'));
    opts[data.correct].classList.add('correct');

    if (data.is_correct) {
      setStatus('✅ Correct! Raise any finger for next question.', 'correct');
    } else {
      opts[selectedOption].classList.add('wrong');
      setStatus(`❌ Wrong! Correct: ${['A','B','C','D'][data.correct]}. Raise a finger to continue.`, 'wrong');
    }

    if (data.done) {
      phase = 'result';
      setTimeout(() => showResult(data.score, data.total), 1600);
    }

  } catch {
    setStatus('Error submitting answer.', '');
    phase = 'selecting';
  }
}


// ══════════════════════════════════════════
//  UI HELPERS
// ══════════════════════════════════════════
function highlightOption(idx) {
  opts.forEach(o => o.classList.remove('selected'));
  opts[idx].classList.add('selected');
}

function clearOptions() {
  opts.forEach(o => o.classList.remove('selected', 'correct', 'wrong'));
}

function setStatus(msg, state) {
  statusMsg.textContent = msg;
  statusBar.classList.remove('correct', 'wrong');
  if (state) statusBar.classList.add(state);
}

function updateDetectionUI(f) {
  // Update nav detection indicator
  if (f === -1) {
    detDot.classList.remove('active');
    detText.textContent = 'Waiting for hand...';
  } else {
    detDot.classList.add('active');
    detText.textContent = f === 0 ? '✊ Fist detected' : `${f} finger${f > 1 ? 's' : ''} up`;
  }

  // Highlight active hint pill
  hints.forEach(h => h.classList.remove('active'));
  if (f === 0)            hints[0].classList.add('active');  // fist
  else if (f >= 1 && f <= 4) hints[f].classList.add('active');  // h1-h4
}


// ══════════════════════════════════════════
//  RESULT SCREEN
// ══════════════════════════════════════════
function showResult(s, t) {
  phase = 'result';
  clearInterval(pollTimer);

  finalScore.textContent = s;
  finalTotal.textContent = `/ ${t}`;
  progressFill.style.width = '100%';
  questionNum.textContent = `${t} / ${t}`;

  const pct = s / t;
  if      (pct >= 0.9) { resultEmoji.textContent = '🏆'; resultTitle.textContent = 'Outstanding!';  resultMsg.textContent = 'Near perfect — you absolutely crushed it!'; }
  else if (pct >= 0.7) { resultEmoji.textContent = '🎉'; resultTitle.textContent = 'Great Job!';    resultMsg.textContent = 'Solid performance. Well done!'; }
  else if (pct >= 0.5) { resultEmoji.textContent = '👍'; resultTitle.textContent = 'Not Bad!';      resultMsg.textContent = 'More than half right. Keep it up!'; }
  else                 { resultEmoji.textContent = '📚'; resultTitle.textContent = 'Keep Studying'; resultMsg.textContent = 'Better luck next time!'; }

  setTimeout(() => resultOverlay.classList.add('show'), 400);
}

function restartQuiz() {
  resultOverlay.classList.remove('show');
  fetch('/quiz/restart', { method: 'POST' })
    .then(() => {
      score = 0;
      scoreVal.textContent = 0;
      progressFill.style.width = '0%';
      phase = 'selecting';
      loadQuestion();
      startPolling();
    });
}


// ══════════════════════════════════════════
//  POLLING
// ══════════════════════════════════════════
function startPolling() {
  if (pollTimer) clearInterval(pollTimer);
  pollTimer = setInterval(pollGesture, 150);
}

// ── INIT ──
loadQuestion();
startPolling();