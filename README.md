# tiny-chess — a chess engine in 4,059 bytes of Python

Entry for make.fun **tiny-chess-01** ("Build the strongest chess engine in
4 KB of Python"). `main.py` is the whole engine: Python 3.13 stdlib only,
no other files read. It speaks the trial protocol over HTTP JSON
(`POST /game`, `/move`, `/resign` against `MAKEFUN_ENV_URL`).

## Design

- **Board/search:** 0x88 mailbox board; negamax with alpha-beta, PVS,
  transposition table, quiescence (captures + promotions, all moves when in
  check), null-move pruning, LMR, MVV-LVA + killer + history move ordering,
  repetition and fifty-move draw scoring inside the search.
- **Evaluation:** tapered (middlegame/endgame) piece-square tables written
  for this engine, material, bishop-pair bonus — maintained
  **incrementally** (running mg/eg scores updated on every make/unmake, so
  `evaluate()` is O(1)), with incrementally maintained zobrist keys and
  game phase.
- **Determinism:** fixed budget of **80,000 nodes per move** — no wall
  clock, no unseeded randomness (zobrist keys come from a fixed-seed PRNG),
  so scored trials replay byte-identically.
- **Packing:** the shipped `main.py` is an lzma-compressed payload
  (latin-1 string literal + `exec`) of a token-verified minified build;
  the decompressed engine is byte-for-byte the tested source.

## Local practice results (kit practice instances, 8 games each)

| instance | Elo | W/D/L |
|---|---|---|
| trial-0 | 1,253 | 3/0/5 |
| trial-1 | 1,530 | 5/0/3 |
| trial-2 | 1,173 | 2/1/5 |
| **mean** | **1,319** | 10/1/13 overall |

The house Sunfish baseline averages ≈ 1,325 on the same instances, so
this build plays at baseline level (paired difference −6, well inside
the measurement interval) and 97 points above this repository's first
graded build. Verified locally before submission: the perft suite
passes and 17,780 incremental-state integrity checks pass (running
scores, phase, zobrist key and bishop counts recomputed from scratch
after every make/unmake).

## License

MIT — see `LICENSE`.
