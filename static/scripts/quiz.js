// ═══════════════════════════════════════════
//  MIWS — Gesture Quiz  |  quiz.js
//  Hold finger for 1.5s to confirm answer.
// ═══════════════════════════════════════════

const detDot        = document.getElementById('detDot');
const detText       = document.getElementById('detText');
const questionNum   = document.getElementById('questionNum');
const progressFill  = document.getElementById('progressFill');
const scoreVal      = document.getElementById('scoreVal');
const qCategory     = document.getElementById('qCategory');
const qText         = document.getElementById('qText');
const opts          = [0,1,2,3].map(i => document.getElementById(`opt${i}`));
const optTexts      = [0,1,2,3].map(i => document.getElementById(`optText${i}`));
const hints         = [0,1,2,3,4].map(i => document.getElementById(`h${i}`));
const holdRings     = [0,1,2,3].map(i => document.getElementById(`ring${i}`));
const statusBar     = document.getElementById('statusBar');
const statusMsg     = document.getElementById('statusMsg');
const resultOverlay = document.getElementById('resultOverlay');
const finalScore    = document.getElementById('finalScore');
const finalTotal    = document.getElementById('finalTotal');
const resultEmoji   = document.getElementById('resultEmoji');
const resultTitle   = document.getElementById('resultTitle');
const resultMsg     = document.getElementById('resultMsg');

let phase     = 'selecting';
let score     = 0;
let total     = 10;
let pollTimer = null;


// ══════════════════════════════════════════
//  LOAD QUESTION
// ══════════════════════════════════════════
async function loadQuestion() {
  phase = 'selecting';
  clearOptions();
  setStatus('Hold a finger steady for 1.5s to confirm your answer.', '');

  try {
    const res  = await fetch('/quiz/question');
    const data = await res.json();

    if (data.done) { showResult(data.score, data.total); return; }

    total = data.total;
    score = data.score;

    qCategory.textContent    = data.category;
    qText.textContent        = data.question;
    optTexts.forEach((el, i) => el.textContent = data.options[i]);
    questionNum.textContent  = `${data.index + 1} / ${total}`;
    progressFill.style.width = `${(data.index / total) * 100}%`;
    scoreVal.textContent     = score;

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
    const f    = data.fingers;   // -1 = not confirmed yet, 1-4 = confirmed
    const h    = data.holding;   // -1 = no hand, 1-4 = finger currently held
    const prog = data.progress;  // 0-100

    updateDetectionUI(h, f, prog);

    if (phase === 'selecting') {
      // FIX: use h directly — this is what was missing
      if (h >= 1 && h <= 4 && prog > 0 && prog < 100) {
        highlightHolding(h - 1, prog);
      } else if (h === -1) {
        clearHoldBars();
      }

      // f >= 1 means fully confirmed
      if (f >= 1 && f <= 4) {
        confirmAnswer(f - 1);
      }
    }

    // After answer shown, next confirmed gesture = next question
    if (phase === 'confirmed' && f >= 1 && f <= 4) {
      phase = 'transitioning';
      setTimeout(loadQuestion, 400);
    }

  } catch { /* ignore */ }
}


// ══════════════════════════════════════════
//  CONFIRM ANSWER
// ══════════════════════════════════════════
async function confirmAnswer(idx) {
  if (phase !== 'selecting') return;
  phase = 'confirmed';
  clearHoldBars();

  try {
    const res  = await fetch('/quiz/answer', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ answer: idx })
    });
    const data = await res.json();

    score = data.score;
    scoreVal.textContent = score;
    // FIX: simple, correct progress formula
    progressFill.style.width = `${(data.index / data.total) * 100}%`;

    opts.forEach(o => o.classList.remove('holding', 'selected'));
    opts[data.correct].classList.add('correct');

    if (data.is_correct) {
      setStatus('✅ Correct! Hold any finger for next question.', 'correct');
    } else {
      opts[idx].classList.add('wrong');
      setStatus(`❌ Wrong! Correct: ${['A','B','C','D'][data.correct]}. Hold a finger to continue.`, 'wrong');
    }

    if (data.done) {
      phase = 'result';
      setTimeout(() => showResult(data.score, data.total), 1800);
    }

  } catch {
    setStatus('Error submitting answer.', '');
    phase = 'selecting';
  }
}


// ══════════════════════════════════════════
//  STOP QUIZ — releases camera before leaving
// ══════════════════════════════════════════
function stopQuiz() {
  clearInterval(pollTimer);
  fetch('/quiz/stop').finally(() => { window.location.href = '/'; });
}

function stopAndGoHome() {
  stopQuiz();
}


// ══════════════════════════════════════════
//  UI HELPERS
// ══════════════════════════════════════════
function highlightHolding(idx, progress) {
  opts.forEach((o, i) => {
    o.classList.remove('holding');
    if (holdRings[i]) holdRings[i].style.width = '0%';
  });
  hints.forEach(h => h && h.classList.remove('active', 'holding'));

  opts[idx].classList.add('holding');
  if (holdRings[idx]) holdRings[idx].style.width = progress + '%';
  if (hints[idx + 1]) hints[idx + 1].classList.add('active');
}

function clearHoldBars() {
  opts.forEach((o, i) => {
    o.classList.remove('holding');
    if (holdRings[i]) holdRings[i].style.width = '0%';
  });
  hints.forEach(h => h && h.classList.remove('active', 'holding'));
}

function clearOptions() {
  opts.forEach((o, i) => {
    o.classList.remove('selected', 'correct', 'wrong', 'holding');
    if (holdRings[i]) holdRings[i].style.width = '0%';
  });
  hints.forEach(h => h && h.classList.remove('active', 'holding'));
}

function setStatus(msg, state) {
  statusMsg.textContent = msg;
  statusBar.classList.remove('correct', 'wrong');
  if (state) statusBar.classList.add(state);
}

function updateDetectionUI(h, f, prog) {
  if (f >= 1 && f <= 4) {
    detDot.classList.add('active');
    detText.textContent = `✅ ${f} finger${f > 1 ? 's' : ''} confirmed`;
  } else if (prog > 0 && h >= 1) {
    detDot.classList.add('active');
    detText.textContent = `Holding ${h} finger${h > 1 ? 's' : ''}... ${prog}%`;
  } else {
    detDot.classList.remove('active');
    detText.textContent = 'Waiting for hand...';
  }
}


// ══════════════════════════════════════════
//  RESULT SCREEN
// ══════════════════════════════════════════
function showResult(s, t) {
  phase = 'result';
  clearInterval(pollTimer);
  finalScore.textContent   = s;
  finalTotal.textContent   = `/ ${t}`;
  progressFill.style.width = '100%';
  questionNum.textContent  = `${t} / ${t}`;

  const pct = s / t;
  if      (pct >= 0.9) { resultEmoji.textContent = '🏆'; resultTitle.textContent = 'Outstanding!';  resultMsg.textContent = 'Near perfect — you crushed it!'; }
  else if (pct >= 0.7) { resultEmoji.textContent = '🎉'; resultTitle.textContent = 'Great Job!';    resultMsg.textContent = 'Solid performance. Well done!'; }
  else if (pct >= 0.5) { resultEmoji.textContent = '👍'; resultTitle.textContent = 'Not Bad!';      resultMsg.textContent = 'More than half right. Keep it up!'; }
  else                 { resultEmoji.textContent = '📚'; resultTitle.textContent = 'Keep Studying'; resultMsg.textContent = 'Better luck next time!'; }

  setTimeout(() => resultOverlay.classList.add('show'), 400);
}

function restartQuiz() {
  resultOverlay.classList.remove('show');
  fetch('/quiz/restart', { method: 'POST' }).then(() => {
    score = 0;
    scoreVal.textContent     = 0;
    progressFill.style.width = '0%';
    phase = 'selecting';
    loadQuestion();
    startPolling();
  });
}


// ══════════════════════════════════════════
//  POLLING + INIT
// ══════════════════════════════════════════
function startPolling() {
  if (pollTimer) clearInterval(pollTimer);
  pollTimer = setInterval(pollGesture, 100);
}

loadQuestion();
startPolling();