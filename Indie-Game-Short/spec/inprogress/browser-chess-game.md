# Browser Chess Game

**Created**: 2026-06-06
**Status**: In Progress
**Scope**: Full browser-based chess application

---

## Overview

A fully playable chess game running in the browser with two modes: **Play Yourself** (local two-player on one screen, hot-seat style) and **AI Mode** (single player vs. a chess engine). The visual style is a dark, luxurious aesthetic — deep walnut board, cream and charcoal pieces, gold highlights — designed to feel premium without being cluttered.

---

## Core Mechanics

### Board & Pieces
- Standard 8×8 chessboard rendered in HTML/CSS or Canvas
- All 32 pieces represented with SVG icons (no raster images — scalable, crisp at any size)
- Pieces snap to squares on drop or click-to-move
- Highlighted legal moves shown on piece selection (soft glow on valid target squares)

### Play Yourself Mode
- Both White and Black are controlled by the human player
- Turn alternates normally after each valid move
- No clock — purely for analysis, study, or casual play
- Full legal move enforcement (no illegal moves accepted)

### AI Mode
- Human plays as White; AI plays as Black (color selection stretch goal)
- AI powered by **Stockfish.js** (WebAssembly build) running in a Web Worker
- AI strength: **Elo ~1500** (configurable via skill level 1–20 on the Stockfish UCI scale, defaulting to ~10)
- AI "thinks" asynchronously — board is locked during AI turn, spinner shown
- AI move plays automatically after a short simulated delay (300–800ms) to feel natural

### Move Handling
- Click-to-move: click piece → valid squares highlight → click target
- Drag-to-move: drag piece onto target square
- Illegal move attempts: piece snaps back, no state change
- Move history tracked in algebraic notation (PGN-compatible)
- Undo button: steps back one full move (both sides) — Play Yourself only
- In AI mode, undo steps back the human's last move + AI response

### Special Moves
- Castling (kingside and queenside) — both legal conditions enforced
- En passant — enforced correctly with capture of passed pawn
- Pawn promotion — modal appears on reaching back rank; player selects Queen, Rook, Bishop, or Knight
- AI auto-promotes to Queen

### Game State Detection
- Check: king square highlighted red, status bar shows "Check"
- Checkmate: game ends, overlay shows winner, Play Again button
- Stalemate: game ends, overlay shows draw
- Insufficient material draw: detected and declared
- Threefold repetition: tracked, draw claimable (button appears)
- 50-move rule: tracked, draw claimable

---

## Requirements

- Runs entirely in the browser — no server, no backend, no login
- Works on Chrome, Firefox, and Edge (latest two versions each)
- Mobile-responsive: playable on tablets (768px+); phones (360px+) degrade gracefully
- Stockfish.js loaded from a CDN or bundled — no install required
- No external dependencies beyond Stockfish.js and one SVG piece set
- Page load under 3 seconds on a standard connection (Stockfish lazy-loaded after first move)

---

## Acceptance Criteria

- [ ] All legal chess moves are accepted; all illegal moves are rejected
- [ ] En passant, castling, and pawn promotion work correctly in both modes
- [ ] Check, checkmate, stalemate, and draw conditions are detected and displayed
- [ ] AI responds within 5 seconds at default skill level on a mid-range laptop
- [ ] Undo reverts board state and move history correctly
- [ ] Play Yourself and AI Mode are selectable from a start screen
- [ ] New Game resets board and history completely
- [ ] Board renders correctly at 360px, 768px, and 1440px viewport widths
- [ ] Move history panel updates in real time with algebraic notation
- [ ] Pawn promotion modal appears and applies the chosen piece

---

## Technical Considerations

### Stack
- **Vanilla HTML/CSS/JS** — no framework needed; keeps bundle small and load fast
- **Stockfish.js (WASM)** — run in a `Worker` thread to avoid blocking the UI
- **SVG piece set** — recommend [cburnett](https://github.com/nicholasstephan/chess-pieces) or [Lichess piece sets](https://lichess.org/) (open license)
- **Chess logic** — implement from scratch or use [chess.js](https://github.com/jhlywa/chess.js) (MIT) for move validation and game state

### Architecture
```
index.html
├── style.css          — board, pieces, UI chrome
├── main.js            — game loop, UI events, mode switching
├── chess-logic.js     — move validation, game state (or chess.js)
├── ai-worker.js       — Stockfish Web Worker wrapper
└── stockfish.wasm     — bundled or CDN
```

### Board Rendering
- CSS grid or absolute positioning for squares
- SVG pieces positioned as `<img>` or inline SVG inside square divs
- Board can be flipped for Play Yourself mode (stretch goal)

### AI Communication
```
main.js  →  postMessage("position fen ... moves ...")  →  ai-worker.js
         ←  postMessage("bestmove e2e4")               ←
```

### Styling — Dark Luxe Theme
- **Board light squares**: `#e8d5b0` (warm cream)
- **Board dark squares**: `#5c3d1e` (deep walnut)
- **Background**: `#1a1a1a` (near-black)
- **Accent / highlights**: `#c9a84c` (antique gold)
- **UI text**: `#f0e6d3` (off-white parchment)
- **Font**: `Cinzel` (Google Fonts) for headings; `Inter` for UI chrome
- Pieces: cream/white for White, charcoal/near-black for Black

### Performance
- Stockfish loaded lazily on first AI move request
- Board updates via DOM diffing (no full re-render on each move)
- Debounce resize handler for responsive recalculation

---

## Edge Cases

- **Promotion on AI move**: AI always promotes to Queen; no modal shown
- **Undo during AI thinking**: disable undo button while AI Worker is running
- **Drag off board**: piece returns to origin square
- **Double-click a piece**: deselect and reselect
- **Click opponent's piece on your turn**: deselect current piece, do not move
- **Threefold repetition / 50-move**: only claimable by active player; don't auto-draw
- **Browser tab loses focus during AI turn**: Worker continues, move applies on return
- **Stockfish WASM not supported**: graceful fallback message, disable AI mode
- **Rapid clicking during move animation**: queue or debounce to prevent state corruption

---

## Dependencies

- [chess.js](https://github.com/jhlywa/chess.js) — move validation, FEN/PGN, game state (MIT license)
- [Stockfish.js](https://github.com/nmrugg/stockfish.js) — WASM chess engine (GPL-3.0; acceptable for non-commercial use)
- SVG piece set — cburnett or similar (open license)
- Google Fonts: Cinzel, Inter (loaded via `<link>`)

---

## Implementation Notes

### Recommended Build Order
1. Render static board with piece placement from FEN
2. Wire click-to-move with chess.js validation
3. Add drag-to-move
4. Implement game state detection (check/checkmate/draw overlays)
5. Add move history panel
6. Add Play Yourself mode with undo
7. Integrate Stockfish Worker for AI mode
8. Add pawn promotion modal
9. Polish UI, responsive layout, animations

### Animations
- Piece move: CSS `transition: transform 150ms ease` — fast enough to feel snappy
- Check flash: brief red pulse on king square
- Capture: captured piece fades out (opacity 0, 100ms) before attacker moves in

### Stockfish UCI Setup
```
uci
setoption name Skill Level value 10
isready
position fen <current FEN>
go movetime 1000
```
Parse `bestmove <from><to>[promotion]` from Worker response.

### PGN Export (stretch goal)
- Button to copy PGN to clipboard for game review in external tools

---

## Stretch Goals

- Color selection before AI game (play as Black)
- Board flip button in Play Yourself mode
- Adjustable AI difficulty slider (1–20)
- Move sound effects (move, capture, check)
- PGN export / import
- Highlight last move with subtle gold tint
- Game clock (optional, Play Yourself only)
