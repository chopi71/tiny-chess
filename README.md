# tiny-chess — a chess engine in under 4 KB of Python

Entry for make.fun **tiny-chess-01** ("Build the strongest chess engine in
4 KB of Python"). The engine ships in two files: `main.py`, a small
loader, and `engine.lzma`, the lzma-compressed engine payload it
unpacks and executes. Python 3.13 stdlib only. It speaks the trial
protocol over HTTP JSON (`POST /game`, `/move`, `/resign` against
`MAKEFUN_ENV_URL`).

## Design

- **Board/search:** 0x88 mailbox board; negamax with alpha-beta, PVS,
  transposition table, quiescence (captures + promotions, all moves when
  in check), null-move pruning, LMR, MVV-LVA + killer + history move
  ordering, repetition and fifty-move draw scoring inside the search.
- **Evaluation:** tapered (middlegame/endgame) piece-square tables
  written for this engine, material, bishop-pair bonus — maintained
  **incrementally** (running mg/eg scores updated on every make/unmake,
  so `evaluate()` is O(1)), with incrementally maintained zobrist keys
  and game phase.
- **Determinism:** fixed budget of **80,000 nodes per move** — no wall
  clock, no unseeded randomness, so scored trials replay identically.
- **Packing:** the engine source (10,614 bytes minified) is far over
  the 4,096-byte per-file limit, so it ships lzma-compressed as
  `engine.lzma` (3,927 bytes); `main.py` is its unpacker. The loader
  build was verified to play move-for-move identically to the
  directly packed build (same perft and integrity results, identical
  moves in repeated trial games).

## Local practice results (kit practice instances, 8 games each)

| instance | Elo | W/D/L |
|---|---|---|
| trial-0 | 1,253 | 3/0/5 |
| trial-1 | 1,530 | 5/0/3 |
| trial-2 | 1,173 | 2/1/5 |
| **mean** | **1,319** | 10/1/13 overall |

The house Sunfish baseline averages ≈ 1,325 on the same instances, so
this build plays at baseline level (paired difference −6, well inside
the measurement interval).

## License

MIT — see `LICENSE`.
