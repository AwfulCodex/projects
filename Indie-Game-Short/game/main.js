import { Chess } from 'https://cdn.jsdelivr.net/npm/chess.js@0.13.4/chess.min.js';

// ── Piece image URLs (Wikimedia Commons, public domain) ───────────────────────

function pieceUrl(color, type) {
  const c = color === 'w' ? 'l' : 'd';
  return `https://commons.wikimedia.org/wiki/Special:FilePath/Chess_${type}${c}t45.svg`;
}

// ── State ─────────────────────────────────────────────────────────────────────

let game        = null;
let gameMode    = 'self';   // 'self' | 'ai'
let selectedSq  = null;     // e.g. 'e2'
let legalMoves  = [];       // verbose move objects for selected square
let aiThinking  = false;
let aiGeneration = 0;       // bumped to invalidate in-flight AI requests on new game / menu
let pendingPromo = null;    // { from, to } while promotion modal is open
let dragState   = null;     // { sq, ghost } during drag
let dragMoved   = false;    // true if mouse moved enough during drag to count as a drag (not a click)

// ── Boot ──────────────────────────────────────────────────────────────────────

document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('btn-play-yourself').addEventListener('click', () => startGame('self'));
  document.getElementById('btn-ai-mode').addEventListener('click', () => startGame('ai'));
  document.getElementById('btn-undo').addEventListener('click', handleUndo);
  document.getElementById('btn-new-game').addEventListener('click', returnToMenu);
  document.getElementById('btn-play-again').addEventListener('click', () => {
    hideOverlay();
    startGame(gameMode);
  });
  buildCoords();
});

// ── Screen helpers ────────────────────────────────────────────────────────────

function showScreen(id) {
  document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
  document.getElementById(id).classList.add('active');
}

function returnToMenu() {
  aiGeneration++; // cancel any in-flight AI request
  aiThinking = false;
  document.getElementById('ai-thinking').classList.add('hidden');
  showScreen('start-screen');
}

// ── Game init ─────────────────────────────────────────────────────────────────

function startGame(mode) {
  gameMode     = mode;
  game         = new Chess();
  selectedSq   = null;
  legalMoves   = [];
  aiThinking   = false;
  pendingPromo = null;
  dragState    = null;
  dragMoved    = false;

  aiGeneration++; // invalidate any AI request still pending from a previous game
  document.getElementById('ai-thinking').classList.add('hidden');
  document.getElementById('btn-undo').disabled = false;

  showScreen('game-screen');
  buildBoard();
  render();
  updateStatus();
  clearHistory();
}

// ── Board construction ────────────────────────────────────────────────────────

const FILES = 'abcdefgh';

function buildCoords() {
  const ranks = document.getElementById('coords-ranks');
  ranks.innerHTML = '87654321'.split('').map(r => `<span>${r}</span>`).join('');

  const files = document.getElementById('coords-files');
  files.innerHTML = 'abcdefgh'.split('').map(f => `<span>${f}</span>`).join('');
}

function buildBoard() {
  const boardEl = document.getElementById('board');
  boardEl.innerHTML = '';

  // Render from rank 8 down to rank 1 (white's perspective)
  for (let row = 0; row < 8; row++) {
    for (let col = 0; col < 8; col++) {
      const sq = sqFromRowCol(row, col);
      const isLight = (row + col) % 2 === 0;

      const div = document.createElement('div');
      div.className = 'square ' + (isLight ? 'light' : 'dark');
      div.id = 'sq-' + sq;
      div.addEventListener('click', () => onSquareClick(sq));
      div.addEventListener('dragover', e => e.preventDefault());
      div.addEventListener('drop', e => onDrop(e, sq));
      boardEl.appendChild(div);
    }
  }

  document.addEventListener('mousemove', onMouseMove);
  document.addEventListener('mouseup', onMouseUp);
}

function sqFromRowCol(row, col) {
  return FILES[col] + (8 - row);
}

// ── Rendering ─────────────────────────────────────────────────────────────────

function render() {
  const board = game.board(); // board[0][0] = a8
  const history = game.history({ verbose: true });
  const lastMove = history.length > 0 ? history[history.length - 1] : null;
  const checkSq = game.in_check() ? findKing(game.turn()) : null;

  for (let row = 0; row < 8; row++) {
    for (let col = 0; col < 8; col++) {
      const sq = sqFromRowCol(row, col);
      const el = document.getElementById('sq-' + sq);

      // Reset highlight classes
      el.classList.remove('selected', 'legal-target', 'legal-capture', 'in-check', 'last-move');

      // Apply highlights
      if (lastMove && (sq === lastMove.from || sq === lastMove.to)) el.classList.add('last-move');
      if (sq === checkSq) el.classList.add('in-check');
      if (sq === selectedSq) el.classList.add('selected');

      // Remove existing piece img
      const existing = el.querySelector('img.piece');
      if (existing) el.removeChild(existing);

      // Render piece
      const piece = board[row][col];
      if (piece) {
        const img = createPieceImg(piece.color, piece.type, sq);
        el.appendChild(img);
      }
    }
  }

  // Legal move highlights
  legalMoves.forEach(m => {
    const el = document.getElementById('sq-' + m.to);
    const occupied = game.get(m.to);
    el.classList.add(occupied ? 'legal-capture' : 'legal-target');
  });

  // If a piece is being dragged, dim its origin square
  if (dragState) {
    const originEl = document.getElementById('sq-' + dragState.sq);
    const img = originEl && originEl.querySelector('img.piece');
    if (img) img.classList.add('dragging');
  }

  updateCaptured();
}

function createPieceImg(color, type, sq) {
  const img = document.createElement('img');
  img.src = pieceUrl(color, type);
  img.alt = color + type;
  img.className = 'piece';
  img.draggable = false; // we handle drag manually

  img.addEventListener('mousedown', e => onPieceMouseDown(e, sq));

  return img;
}

function findKing(color) {
  const board = game.board();
  for (let r = 0; r < 8; r++) {
    for (let c = 0; c < 8; c++) {
      const p = board[r][c];
      if (p && p.type === 'k' && p.color === color) return sqFromRowCol(r, c);
    }
  }
  return null;
}

function updateCaptured() {
  const history = game.history({ verbose: true });
  const whiteCaps = [], blackCaps = [];

  history.forEach(m => {
    if (m.captured) {
      if (m.color === 'w') whiteCaps.push(m.captured);
      else blackCaps.push(m.captured);
    }
  });

  renderCaptured('captured-white', 'b', blackCaps); // pieces captured BY white (black pieces)
  renderCaptured('captured-black', 'w', whiteCaps); // pieces captured BY black (white pieces)
}

function renderCaptured(elId, color, types) {
  const el = document.getElementById(elId);
  el.innerHTML = '';
  types.forEach(type => {
    const img = document.createElement('img');
    img.src = pieceUrl(color, type);
    img.className = 'cap-piece';
    el.appendChild(img);
  });
}

// ── Click to move ─────────────────────────────────────────────────────────────

function onSquareClick(sq) {
  if (aiThinking || pendingPromo) return;
  if (gameMode === 'ai' && game.turn() === 'b') return;
  if (dragMoved) { dragMoved = false; return; } // mousedown started a drag — ignore the synthetic click

  const piece = game.get(sq);
  const turn  = game.turn();

  if (selectedSq) {
    const target = legalMoves.find(m => m.to === sq);
    if (target) { attemptMove(selectedSq, sq); return; }

    if (piece && piece.color === turn) { selectSq(sq); return; }

    deselect();
    return;
  }

  if (piece && piece.color === turn) selectSq(sq);
}

function selectSq(sq) {
  selectedSq = sq;
  legalMoves = game.moves({ square: sq, verbose: true });
  render();
}

function deselect() {
  selectedSq = null;
  legalMoves = [];
  render();
}

// ── Drag to move ──────────────────────────────────────────────────────────────

let dragOrigin = null; // { x, y } of mousedown, to detect real drags vs clicks

function onPieceMouseDown(e, sq) {
  if (aiThinking || pendingPromo) return;
  if (gameMode === 'ai' && game.turn() === 'b') return;

  const piece = game.get(sq);
  if (!piece || piece.color !== game.turn()) return;

  e.preventDefault();
  dragOrigin = { x: e.clientX, y: e.clientY };
  dragMoved  = false;

  // Create floating ghost (hidden until mouse actually moves)
  const ghost = document.createElement('div');
  ghost.className = 'drag-ghost';
  ghost.innerHTML = `<img src="${pieceUrl(piece.color, piece.type)}" alt="">`;
  ghost.style.left = e.clientX + 'px';
  ghost.style.top  = e.clientY + 'px';
  ghost.style.display = 'none';
  document.body.appendChild(ghost);

  dragState = { sq, ghost };
  // Don't selectSq yet — wait to see if it's a drag or a click
}

const DRAG_THRESHOLD = 6; // pixels before we commit to a drag

function onMouseMove(e) {
  if (!dragState) return;

  if (!dragMoved && dragOrigin) {
    const dx = e.clientX - dragOrigin.x;
    const dy = e.clientY - dragOrigin.y;
    if (Math.sqrt(dx * dx + dy * dy) < DRAG_THRESHOLD) return;
    // Threshold crossed — commit to drag
    dragMoved = true;
    dragState.ghost.style.display = '';
    selectSq(dragState.sq);
  }

  dragState.ghost.style.left = e.clientX + 'px';
  dragState.ghost.style.top  = e.clientY + 'px';
}

function onMouseUp(e) {
  if (!dragState) return;

  const ghost  = dragState.ghost;
  const fromSq = dragState.sq;
  const wasDrag = dragMoved;

  dragState  = null;
  dragOrigin = null;
  ghost.remove();

  if (!wasDrag) {
    // Was just a click — let the click event handle it normally
    return;
  }

  // Find which square the mouse is released over
  const el = document.elementFromPoint(e.clientX, e.clientY);
  const sqEl = el && el.closest('[id^="sq-"]');
  const toSq = sqEl ? sqEl.id.replace('sq-', '') : null;

  if (toSq && toSq !== fromSq) {
    const isLegal = legalMoves.find(m => m.to === toSq);
    if (isLegal) { attemptMove(fromSq, toSq); return; }
  }

  deselect(); // snap back
}

function onDrop(e, sq) {
  e.preventDefault();
  // covered by mouseup handler
}

// ── Move execution ────────────────────────────────────────────────────────────

function attemptMove(from, to, promotion) {
  const piece = game.get(from);
  const isPromo = piece && piece.type === 'p' &&
    ((piece.color === 'w' && to[1] === '8') || (piece.color === 'b' && to[1] === '1'));

  if (isPromo && !promotion) {
    pendingPromo = { from, to };
    showPromotionModal(game.turn());
    return;
  }

  const result = game.move({ from, to, promotion: promotion || 'q' });
  if (!result) { deselect(); return; }

  selectedSq = null;
  legalMoves = [];

  render();
  updateStatus();
  appendMoveHistory(result);
  checkGameOver();

  if (!game.game_over() && gameMode === 'ai' && game.turn() === 'b') {
    setTimeout(triggerAI, 250);
  }
}

function handleUndo() {
  if (aiThinking || game.history().length === 0) return;

  game.undo();
  if (gameMode === 'ai' && game.history().length > 0) game.undo();

  selectedSq = null;
  legalMoves = [];
  hideOverlay();
  render();
  updateStatus();
  rebuildHistory();
}

// ── Promotion ─────────────────────────────────────────────────────────────────

function showPromotionModal(turn) {
  const container = document.getElementById('promotion-pieces');
  container.innerHTML = '';

  ['q', 'r', 'b', 'n'].forEach(type => {
    const btn = document.createElement('button');
    btn.className = 'promo-btn';
    btn.innerHTML = `<img src="${pieceUrl(turn, type)}" alt="${type}">`;
    btn.addEventListener('click', () => {
      document.getElementById('promotion-modal').classList.add('hidden');
      const { from, to } = pendingPromo;
      pendingPromo = null;
      attemptMove(from, to, type);
    });
    container.appendChild(btn);
  });

  document.getElementById('promotion-modal').classList.remove('hidden');
}

// ── Game state ────────────────────────────────────────────────────────────────

function updateStatus() {
  const el   = document.getElementById('status-bar');
  const turn = game.turn() === 'w' ? 'White' : 'Black';

  if (game.in_checkmate())        el.textContent = `${turn === 'White' ? 'Black' : 'White'} wins by checkmate`;
  else if (game.in_draw())        el.textContent = 'Draw';
  else if (game.in_check())       el.textContent = `${turn} to move  —  Check!`;
  else                            el.textContent = `${turn} to move`;
}

function checkGameOver() {
  if (game.in_checkmate())          showOverlay(game.turn() === 'w' ? 'Black Wins' : 'White Wins', 'by checkmate');
  else if (game.in_stalemate())     showOverlay('Draw', 'by stalemate');
  else if (game.insufficient_material()) showOverlay('Draw', 'insufficient material');
  else if (game.in_threefold_repetition()) showOverlay('Draw', 'threefold repetition');
  else if (game.in_draw())          showOverlay('Draw', 'fifty-move rule');
}

function showOverlay(title, subtitle) {
  document.getElementById('gameover-title').textContent = title;
  document.getElementById('gameover-subtitle').textContent = subtitle;
  document.getElementById('gameover-overlay').classList.remove('hidden');
}

function hideOverlay() {
  document.getElementById('gameover-overlay').classList.add('hidden');
}

// ── Move history ──────────────────────────────────────────────────────────────

function clearHistory() {
  document.getElementById('move-history').innerHTML = '';
}

function appendMoveHistory(move) {
  const history = game.history();
  const el = document.getElementById('move-history');

  // Remove 'latest' class from all rows
  el.querySelectorAll('.move-row').forEach(r => r.classList.remove('latest'));

  const moveNum = history.length;
  const isWhiteMove = moveNum % 2 === 1;
  const pairNum = Math.ceil(moveNum / 2);

  if (isWhiteMove) {
    const row = document.createElement('div');
    row.className = 'move-row latest';
    row.id = 'mr-' + pairNum;
    row.innerHTML = `<span class="move-num">${pairNum}.</span><span class="move-san">${move.san}</span><span class="move-san"></span>`;
    el.appendChild(row);
  } else {
    const row = document.getElementById('mr-' + pairNum);
    if (row) {
      row.classList.add('latest');
      row.querySelector('span:last-child').textContent = move.san;
    }
  }

  el.scrollTop = el.scrollHeight;
}

function rebuildHistory() {
  clearHistory();
  game.history({ verbose: true }).forEach(m => appendMoveHistory(m));
}

// ── AI (remote chess engines) ───────────────────────────────────────────────
//
// Primary:  Lichess cloud-eval — deep, cached Stockfish analysis (free, no key).
//           Returns 404 for positions not in its cache.
// Fallback: chess-api.com — on-demand Stockfish that solves any position, so the
//           bot never stalls once play leaves Lichess's cached lines.

async function triggerAI() {
  if (game.game_over()) return;

  const myGen = aiGeneration;
  aiThinking = true;
  document.getElementById('ai-thinking').classList.remove('hidden');
  document.getElementById('btn-undo').disabled = true;

  const started = Date.now();
  let move = null;
  try {
    move = await getEngineMove(game.fen());
  } catch (err) {
    console.error('Engine request failed:', err);
  }

  // Hold the spinner briefly so moves never feel jarringly instant.
  const elapsed = Date.now() - started;
  if (elapsed < 350) await sleep(350 - elapsed);

  // Abandon if a new game started (or we returned to menu) while waiting.
  if (myGen !== aiGeneration) return;

  aiThinking = false;
  document.getElementById('ai-thinking').classList.add('hidden');
  document.getElementById('btn-undo').disabled = false;

  if (!move) {
    document.getElementById('status-bar').textContent = 'AI unavailable — check your connection';
    return;
  }
  if (game.game_over()) return;

  const result = game.move({ from: move.from, to: move.to, promotion: move.promotion || 'q' });
  if (!result) return;

  render();
  updateStatus();
  appendMoveHistory(result);
  checkGameOver();
}

// Returns { from, to, promotion } or null.
async function getEngineMove(fen) {
  const lichessMove = await getLichessMove(fen);
  if (lichessMove) return lichessMove;
  return await getChessApiMove(fen);
}

async function getLichessMove(fen) {
  try {
    const res = await fetch('https://lichess.org/api/cloud-eval?multiPv=1&fen=' + encodeURIComponent(fen));
    if (!res.ok) return null; // 404 = position not in Lichess's cache
    const data = await res.json();
    const pv = data.pvs && data.pvs[0];
    if (!pv || !pv.moves) return null;
    return parseUci(pv.moves.split(' ')[0]);
  } catch {
    return null;
  }
}

async function getChessApiMove(fen) {
  try {
    const res = await fetch('https://chess-api.com/v1', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ fen, depth: 12 })
    });
    if (!res.ok) return null;
    const data = await res.json();
    return parseUci(data.move);
  } catch {
    return null;
  }
}

function parseUci(uci) {
  if (!uci || uci.length < 4) return null;
  return {
    from: uci.slice(0, 2),
    to: uci.slice(2, 4),
    promotion: uci.length > 4 ? uci[4] : undefined
  };
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
