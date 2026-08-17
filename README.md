<div align="center">

<img src="images/EWC3LabsLogo-blue-128x128.png" alt="EWC3 Labs" width="96" height="96">

# Music Forensics Workbench

### Build the microscope you wish you had.

**Audio in → evidence → competing hypotheses → musical interpretation.**

An open-source workbench for reverse-engineering recorded music. Not "audio in, sheet music out" — a
bench full of composable tools for interrogating a recording until its structure becomes visible,
and for showing *why* an analyzer reached a conclusion.

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE) [![Status:
skeleton](https://img.shields.io/badge/status-skeleton-lightgrey.svg)](#status) [![Made by EWC3
Labs](https://img.shields.io/badge/EWC3-Labs-1f6feb.svg)](https://github.com/ewc3labs)

</div>

## Status

**Milestone 0 — project skeleton.** There is a data model, a test suite, and documentation. There is
no analysis yet. Nothing here loads audio.

That ordering is deliberate. The charter's instruction is to *define the evidence and provenance
model before implementing transcription*, because everything downstream inherits its shape from it.
Building the transcriber first and retrofitting provenance is how you end up with a pipeline that
can tell you the answer but not the reason.

## Why this exists

Wilson got tired of replaying Jimmy Page's prologue riff in Led Zeppelin's *Over the Hills and Far
Away* and did not feel like hand-rolling measure lines and writing stems on paper.

That is the actual origin story. The immediate question was deceptively simple:

> What the hell is Jimmy Page doing rhythmically in that intro?

The phrase implies displaced beats and irregular groupings while ultimately reconciling with an
underlying pulse. Counting eighth notes by hand works. It is also tedious, and **if a problem is
tedious to inspect manually, build the microscope.**

## The idea in one picture

```text
SourceAudio ──► SpectralRepresentations ──► Events ──► MusicalInterpretations
                                             ▲              ▲
                                             │              │
                                       UserAnnotations ─────┘
```

Every derived object records where it came from, what it claims, how confident it is, and what it
was derived from. A human correction is the same kind of object as a machine claim, with
`source: "human"` and confidence `1.0` — so an override is evidence too, not a special case bolted
on beside the model.

## Three rules the design answers to

**No analyzer owns the truth.** Analyzers produce *claims*, not facts. Two pitch trackers that
disagree are a normal state of the system, not an error to be resolved before storage.

**Preserve evidence.** Raw observed timestamps are kept independently of musical quantization.
Deciding an onset lands on beat 3 must never destroy the record that it was measured at 12.413 s.

**Make the reasoning inspectable.** Any conclusion should be traceable backwards to what produced
it. An answer you cannot interrogate is not much better than a guess.

## Getting started

Nothing to run yet beyond the tests.

```bash
python -m venv .venv && . .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
make test
```

| | |
| --- | --- |
| `make test` | run the suite |
| `make lint` | ruff + format check |
| `make fix` | apply formatting, including the documentation |
| `make verify` | everything CI runs |

## Documentation

- **[Overview](docs/Overview.md)** — the documentation index.
- **[Architecture](docs/architecture.md)** — layers, and what is deliberately not decided yet.
- **[Evidence model](docs/evidence-model.md)** — claims, provenance, timebases. Read this first if
  you are writing an analyzer.
- **[Project charter](docs/PROJECT_CHARTER.md)** — the full architectural source of truth.
- **[Roadmap][roadmap]** — milestones and the `MW` series.

## Licensing

**GPL-3.0-only, provisionally.** The choice is not yet ratified by the EWC3 Labs licensing policy
review, and this project is the reason that review exists — see [licensing](docs/licensing.md) for
what is settled and what is not.

Code, model weights, and training datasets are **three separate license objects**, and a permissive
implementation carrying restrictively-licensed weights is a trap this project intends to walk into
knowingly or not at all. [THIRD_PARTY.md](THIRD_PARTY.md) and
[MODELS_AND_DATASETS.md](MODELS_AND_DATASETS.md) exist from the first dependency onward.

**Unknown licensing status is not "probably okay."** It is unknown, and unknown assets are not
redistributed until resolved.

## Name

*Music Forensics Workbench* is a working title. The final name is undecided — candidates so far
include Wavewright, ToneTrace, PhaseLab, and Signal Forge. Suggestions welcome; "SoundLab" is
already rejected as too generic.

---

<div align="center">

> Or, less formally: Wilson was not about to draw all that shit on paper.

</div>

[roadmap]: docs/project/MusicForensics_Workbench_Roadmap.md
