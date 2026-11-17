# Copilot Instructions — Music Forensics Workbench

## Read first

1. `AGENTS.md` — what this repo is, the architecture fence, and what is deliberately out of scope.
2. `docs/evidence-model.md` — read before touching any analyzer. Everything inherits its shape.
3. `docs/project/MusicForensics_Workbench_Development_Roadmap.md` — what is minted, and what is
   next.

## Rules that are enforced in code

- Analyzers emit `Claim`s with provenance. None of them owns the truth, and two disagreeing is a
  normal state, surfaced by `EvidenceGraph.disagreements(kind)`.
- Quantization **derives**: `Claim.derive()` makes a new claim citing the old one. Raw measured
  seconds are never edited.
- Timebases are explicit, and seconds are the interchange unit.
- A dependency gets its `THIRD_PARTY.md` row in the same change; a model gets its
  `MODELS_AND_DATASETS.md` row before it is wired in.
- This repo is public: no absolute paths, no credentials, and no audio in fixtures.
