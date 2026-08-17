# Architecture

The shape of the system, and — more usefully at this stage — what is deliberately still undecided.

## Layers

```text
audio/           loading, decoding, playback, derived audio (stems, HPSS)
analysis/        DSP and ML analyzers. Each emits claims; none owns the truth.
evidence/        claims, provenance, the graph. The canonical data model.
interpretation/  beats, meter, barlines, parts, voices, notation-facing structure
export/          notation, tab, MIDI, machine-readable bundles
plugins/         third-party analyzers, behind the same interface as built-ins
ui/              rendering and interaction. NOT the canonical model.
core/            timebases and shared primitives
```

**Dependencies point inwards toward `evidence/`.** An analyzer knows how to emit claims; it does not
know what the interpretation layer will do with them, and it certainly does not know about the UI.

## Three rules the design answers to

**No analyzer owns the truth.** Analyzers are replaceable and frequently wrong. The moment one of
them gets to write directly into a "the answer" structure, disagreement becomes unrepresentable and
you lose the ability to ask why.

**Preserve evidence.** Raw observed timestamps live independently of musical quantization. See
[evidence-model](evidence-model.md) — this is the constraint most likely to be violated by a
convenient shortcut.

**The UI data model is not the canonical data model.** A rendering structure optimized for smooth
scrolling will quietly become the source of truth if allowed to, and then the analysis model starts
inheriting decisions made for a piano roll widget.

## Interfaces around interesting algorithms

Analyzers sit behind boring interfaces on purpose. Pitch tracking is going to be swapped several
times, the ML ecosystem moves faster than this project will, and none of that churn should reach the
evidence model.

A corollary the charter makes explicit: **do not couple core analysis to one ML framework.** ONNX
Runtime is the likely portability layer, hardware acceleration is an optimization, and CPU fallback
is not a degraded mode — it is the baseline the thing has to be usable in.

## Not decided, on purpose

| | why not yet |
| --- | --- |
| **UI framework** | Qt/PySide, Tauri, and custom rendering are all live. Pick after a vertical slice proves the analysis model, not before. |
| **Storage format** | MessagePack, SQLite, Zarr, HDF5 — the requirement is only that huge arrays never land inside ordinary JSON. |
| **Which ML models** | Every model is a licensing object as well as a technical one. See [licensing](licensing.md). |
| **The name** | *Music Forensics Workbench* is a working title. |

Deciding these early would feel like progress and would mostly be guessing. The charter's phrasing
is worth keeping: **do not overbuild the skeleton.**

## Where to start reading

1. [evidence-model](evidence-model.md) — the data model everything else is shaped by.
2. [PROJECT_CHARTER](PROJECT_CHARTER.md) — the full architectural source of truth, including the
   analysis modules this skeleton has not built yet.
3. [Roadmap][roadmap] — what happens next, in what order.

[roadmap]: project/MusicForensics_Workbench_Roadmap.md
