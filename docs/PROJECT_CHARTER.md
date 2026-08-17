# EWC3 Labs Music Forensics Workbench
## Project Charter & Claude Handoff Specification

**Status:** Concept / architecture seed  
**Organization:** EWC3 Labs  
**Working title:** *Music Forensics Workbench*  
**Final product name:** TBD  
**License intent:** Open source  
**Primary design principle:** Expose the evidence, not just the answer.

---

# 1. Why This Project Exists

Wilson got tired of replaying Jimmy Page's prologue riff in **Led Zeppelin's "Over the Hills and Far Away"** and did not feel like hand-rolling measure lines and writing stems on a piece of paper.

That is the actual origin story.

The immediate question was deceptively simple:

> What the hell is Jimmy Page doing rhythmically in that intro?

The guitar phrase strongly implies displaced beats and irregular groupings while ultimately reconciling with an underlying pulse. Listening repeatedly and counting eighth notes by hand works, but that is not how EWC3 Labs approaches a problem.

If a problem is tedious to inspect manually, build the microscope.

The project therefore exists to create an **open-source music reverse-engineering and computational-analysis workbench**: a hacker toolbox for recorded music.

Not "hacker" in the exploit/malware sense. Hacker in the original engineering sense: a bench full of sharp, composable tools for interrogating a system until its structure becomes visible.

The goal is not merely:

> Audio in → sheet music out.

The goal is:

> Audio in → evidence → competing hypotheses → musical interpretation → human-readable and machine-readable representations.

---

# 2. Mission

Build a local-first, open-source platform that allows musicians, engineers, researchers, and curious lunatics to attack recorded music from multiple analytical directions.

The system should be capable of:

- inspecting raw waveforms;
- visualizing spectral content;
- separating sources/stems;
- distinguishing harmonic and percussive material;
- detecting transients and note onsets;
- tracking continuous pitch rather than immediately quantizing everything to MIDI notes;
- transcribing polyphonic audio;
- inferring tempo, beats, meter, barlines, chords, and key;
- representing bends, slides, vibrato, and other expressive pitch motion;
- producing standard notation;
- producing piano reductions;
- producing guitar and bass tablature;
- producing drum notation;
- exporting machine-readable representations for further computational study;
- allowing a human to override assumptions and recompute downstream interpretation;
- showing *why* an analyzer reached a conclusion.

The project should function as both:

1. a practical transcription environment; and
2. an audio/music forensics laboratory.

---

# 3. Core Philosophy

## 3.1 No analyzer owns the truth

Every model, DSP algorithm, heuristic, and human annotation produces a **hypothesis**.

A pitch model may identify F#4 with 0.86 confidence.

A beat tracker may identify a downbeat at 12.410 seconds.

A human may override the downbeat and place it at 12.530 seconds.

All three events should remain independently identifiable.

Derived musical interpretations should record their provenance.

---

## 3.2 Preserve evidence

Never throw away useful information prematurely.

Do **not** immediately reduce continuous audio to note names and durations.

Retain:

- source audio;
- channels;
- stems;
- waveform data;
- spectrogram representations;
- harmonic/percussive separation;
- onset candidates;
- continuous pitch trajectories;
- note candidates;
- tempo hypotheses;
- beat/downbeat hypotheses;
- meter hypotheses;
- chord/key hypotheses;
- confidence values;
- model/algorithm identity and version;
- manual annotations;
- relationships between derived artifacts.

MIDI, MusicXML, tablature, and engraved notation are **views of the analysis**, not the canonical source of truth.

---

## 3.3 Make the reasoning inspectable

The user should be able to click a derived musical event and ask, in effect:

> "Okay, motherfucker. Why do you think that's an eighth-note G?"

The application should be able to show the supporting evidence:

- spectral ridge;
- fundamental pitch trajectory;
- harmonics;
- onset transient;
- beat-grid relationship;
- source/stem;
- algorithm/model;
- confidence;
- transformations applied before inference.

This inspectability is one of the project's primary differentiators.

---

# 4. Initial Use Case: The Jimmy Page Problem

The first serious test case should be the acoustic intro to:

**Led Zeppelin — "Over the Hills and Far Away"**

The application should allow the user to:

1. load the recording;
2. select/loop the intro;
3. slow playback without changing pitch;
4. display waveform and spectrogram;
5. identify guitar attack/onset events;
6. overlay an eighth-note and sixteenth-note temporal grid;
7. fit a user-specified tempo;
8. test a forced **4/4** hypothesis;
9. run unconstrained beat/downbeat/meter inference;
10. compare alternative metric interpretations;
11. visualize phrase displacement against barlines;
12. show where attacks move off the psychologically expected grid;
13. show where the phrase realigns;
14. generate conventional notation;
15. generate guitar tablature;
16. preserve bends, hammer-ons, pull-offs, slides, ringing open strings, and other guitar-specific events where detectable.

If the tool can make that intro understandable without Wilson drawing measure lines by hand, the first milestone has succeeded.

---

# 5. Architectural Model

Conceptually:

```text
                         ┌──────────────────┐
                         │   Source Audio   │
                         └────────┬─────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │ Preprocessing / Analysis  │
                    │         Bus               │
                    └─────────────┬─────────────┘
                                  │
       ┌──────────────────────────┼──────────────────────────┐
       │                          │                          │
       ▼                          ▼                          ▼
  DSP analyzers              ML analyzers              Human input
       │                          │                          │
       └──────────────────────────┼──────────────────────────┘
                                  ▼
                     ┌─────────────────────────┐
                     │ Common Evidence Graph   │
                     │ + provenance/confidence │
                     └────────────┬────────────┘
                                  │
            ┌─────────────────────┼─────────────────────┐
            ▼                     ▼                     ▼
      Analysis Views       Musical Interpretation     Exporters
            │                     │                     │
     waveform/spectrum      notes/meter/tab       MIDI/MusicXML/
     contour/onsets/etc.    articulation/etc.     PDF/JSON/etc.
```

---

# 6. Common Evidence Graph / Intermediate Representation

The heart of the system should be an intermediate representation richer than MIDI.

Conceptual model:

```text
Project
├── SourceAudio
│   ├── metadata
│   ├── channels
│   └── timebase
│
├── DerivedAudio
│   ├── stems
│   ├── harmonic component
│   ├── percussive component
│   └── filtered/processed variants
│
├── SpectralRepresentations
│   ├── STFT
│   ├── CQT
│   ├── chromagram
│   └── other feature maps
│
├── Events
│   ├── OnsetCandidates
│   ├── PitchContours
│   ├── NoteCandidates
│   ├── BeatCandidates
│   ├── DownbeatCandidates
│   ├── MeterHypotheses
│   ├── ChordHypotheses
│   ├── KeyHypotheses
│   ├── InstrumentEvents
│   └── ArticulationEvents
│
├── UserAnnotations
│   ├── pinned beat
│   ├── forced barline
│   ├── corrected pitch
│   ├── instrument identity
│   └── arbitrary region annotation
│
└── MusicalInterpretations
    ├── Parts
    ├── Voices
    ├── Measures
    ├── Notes
    ├── Articulations
    ├── Bends
    ├── Slides
    ├── Vibrato
    ├── GuitarStringFretAssignments
    └── Confidence / provenance
```

Every derived object should record something similar to:

```json
{
  "source": "basic_pitch",
  "source_version": "x.y.z",
  "timestamp_start": 12.413,
  "timestamp_end": 12.677,
  "claim": {
    "event": "note",
    "pitch": "F#4"
  },
  "confidence": 0.86,
  "derived_from": [
    "stem:guitar",
    "spectral_region:abc123",
    "onset:event456"
  ]
}
```

Human corrections use the same provenance concept:

```json
{
  "source": "human",
  "actor": "wilson",
  "claim": {
    "event": "downbeat",
    "timestamp": 12.530
  },
  "confidence": 1.0
}
```

---

# 7. Analysis Modules

All major analyzers should eventually be plugins/adapters behind a stable interface.

## 7.1 Audio ingest

Support initially:

- WAV
- FLAC
- MP3
- AAC/M4A where codecs allow
- potentially direct microphone or loopback capture later

Normalize all timing internally to high-resolution timestamps independent of sample rate.

---

## 7.2 Playback

Must support:

- region selection;
- loop playback;
- scrub;
- frame/sample-accurate cursor where practical;
- playback-rate reduction;
- pitch-preserving time stretch;
- A/B comparison;
- optional stem solo/mute.

---

## 7.3 Waveform visualization

Capabilities:

- multiresolution waveform;
- zoom to sample/transient level;
- markers;
- regions;
- beat/bar overlays;
- onset overlays;
- stem overlays.

---

## 7.4 Spectral analysis

Initial DSP representations:

- STFT;
- mel spectrogram;
- constant-Q transform;
- chromagram;
- spectral centroid;
- spectral flux;
- harmonic/percussive masks.

The UI must allow synchronization between waveform, spectrogram, piano-roll/pitch contour, and notation views.

---

## 7.5 Harmonic/percussive separation

Use HPSS as a fast deterministic first pass.

This is important because percussion produces broadband transients that contaminate pitch-oriented analysis.

The system should maintain both separated results and the original signal.

---

## 7.6 Stem separation

Support interchangeable separation backends.

Candidate upstream technologies to evaluate:

- Demucs;
- other maintained/open source stem separators.

Possible stems:

- vocals;
- drums;
- bass;
- guitar;
- piano;
- other.

Do not assume source separation is perfect.

All stem-derived conclusions must remain traceable back to the original mix.

---

## 7.7 Onset/transient detection

Provide:

- deterministic DSP onset detection;
- optional learned onset detector;
- confidence;
- comparison view between algorithms.

Useful especially for:

- guitar pick attacks;
- piano;
- percussion;
- rhythm inference.

---

## 7.8 Continuous pitch tracking

This is critical.

The canonical pitch representation should be a continuous function/trajectory:

```text
f0(t)
```

not merely a sequence of MIDI notes.

This allows representation of:

- guitar bends;
- trombone slides;
- fretless bass;
- vocal scoops;
- vibrato;
- portamento;
- pitch correction artifacts;
- intonation drift.

Quantized notes are inferred **from** pitch trajectories.

---

## 7.9 Polyphonic transcription

Provide model adapters instead of hard-wiring one implementation.

Candidate upstream technologies to evaluate:

- Spotify Basic Pitch;
- MT3;
- Omnizart;
- guitar-specific polyphonic transcription models;
- future models.

Desired output:

- note pitch;
- onset;
- offset;
- velocity/intensity;
- pitch bend/contour;
- confidence;
- likely source/instrument.

---

## 7.10 Tempo and beat tracking

Support:

- automatic tempo estimation;
- multiple tempo candidates;
- manual BPM entry;
- tapped tempo;
- beat locations;
- downbeat probabilities;
- variable-tempo maps.

Do not force audio to a rigid tempo grid.

Represent the grid as a hypothesis over actual timestamps.

---

## 7.11 Meter and barline inference

This is a major research/experimentation area.

Support:

- forced meter;
- unconstrained meter inference;
- multiple competing meter hypotheses;
- additive meter;
- mixed meter;
- phrase displacement;
- pickup/anacrusis;
- temporarily displaced accents;
- confidence per bar/downbeat.

Examples:

```text
4/4
7/8
4/4 + 3/4
3+2+2 / 8
2+2+3 / 8
```

The system should make it possible to test:

> Is the meter changing, or is the phrase simply displaced over an unchanged meter?

This distinction is central to the Jimmy Page test case.

---

## 7.12 Harmony analysis

Eventually support:

- chord candidates;
- inversions;
- key center;
- modulations;
- modal analysis;
- chromatic/non-functional harmony.

Again: hypotheses, not immutable answers.

---

# 8. Guitar and Bass Tablature

Tablature must be part of the **core representation**, not a late exporter.

Audio → note is not equivalent to audio → playable tab.

The same pitch may exist at several string/fret locations.

Tab inference therefore becomes a constrained optimization problem.

Possible cost terms:

```text
cost =
    hand_position_change
  + stretch_penalty
  + impossible_fingering_penalty
  + string_crossing_penalty
  + articulation_mismatch
  + tuning_mismatch
  - open_string_preference
  - phrase_position_consistency
```

Inputs may include:

- tuning;
- capo;
- number of strings;
- scale length if relevant;
- fret count;
- detected string identity where models support it;
- surrounding phrase;
- articulation;
- continuous pitch bend.

The user should be able to choose among alternative fingerings.

---

## 8.1 Guitar-specific events

Represent explicitly where possible:

- hammer-on;
- pull-off;
- slide;
- bend;
- pre-bend;
- release;
- vibrato;
- natural/artificial harmonic;
- palm mute;
- dead note;
- ringing/open string;
- let ring;
- capo;
- alternate tunings.

A bend must not be flattened into a sequence of tiny chromatic MIDI notes.

---

# 9. Piano Reduction / Standard Notation

Do not reinvent an engraving engine.

Candidate strategy:

```text
Evidence Graph
      ↓
Musical Interpretation
      ↓
MusicXML
      ↓
MuseScore / LilyPond / other engraver
      ↓
PDF / SVG / printable notation
```

For piano reduction:

- assign voices;
- infer left/right hand;
- preserve musically meaningful inner voices;
- control simplification/quantization;
- provide difficulty targets later.

Potential upstream tooling to evaluate:

- MuseScore;
- music21;
- LilyPond;
- existing open-source transcription/reduction projects.

---

# 10. Drum Handling

Drums are not simply "frequencies to filter out."

Percussion is broadband and overlaps pitched instruments spectrally.

Use multiple layers:

1. HPSS;
2. stem separation;
3. transient classification;
4. instrument-specific drum transcription.

Eventually identify:

- kick;
- snare;
- toms;
- hi-hat;
- ride;
- crash;
- other percussion.

Drum tracks should support standard drum notation and event timelines.

---

# 11. Pitch-Correction / Performance Forensics

A future analysis module may characterize pitch correction without pretending to establish certainty where evidence is ambiguous.

Potential measurements:

- pitch glide rates;
- pitch trajectory curvature;
- transition time between pitch centers;
- vibrato regularity;
- cent deviation distribution;
- unnatural stair-stepping;
- unusually exact pitch centering;
- discontinuities;
- phase/spectral artifacts where detectable.

Output should be evidence-driven:

```text
"Characteristics consistent with strong pitch correction"
```

rather than an unsupported binary accusation.

This module is secondary to the initial transcription/analysis mission but fits naturally in the architecture.

---

# 12. Plugin Architecture

Conceptual API:

```text
audio
  ↓
analysis bus
  ├── HPSS
  ├── Demucs adapter
  ├── Basic Pitch adapter
  ├── MT3 adapter
  ├── Omnizart adapter
  ├── onset detector
  ├── beat tracker
  ├── chord analyzer
  ├── meter analyzer
  ├── fret solver
  ├── pitch-correction analyzer
  └── weird thing Wilson wrote at 2 AM
  ↓
common evidence graph
  ↓
views / interpreters / exporters
```

The "weird thing Wilson wrote at 2 AM" slot is architecturally mandatory.

Plugin types may include:

- audio preprocessors;
- feature generators;
- event detectors;
- model-based analyzers;
- hypothesis generators;
- interpreters;
- visualizers;
- exporters.

---

# 13. Local-First / Compute Strategy

Primary development target includes an AMD Ryzen-based workstation with integrated Ryzen AI/NPU capability.

The application should run usefully without a giant GPU.

Preferred strategy:

- deterministic DSP on CPU;
- lightweight ML models where possible;
- ONNX Runtime as a likely portability layer;
- model quantization where quality remains acceptable;
- optional NPU acceleration;
- optional GPU acceleration;
- graceful CPU fallback.

Do not design the entire system around a single hardware accelerator.

Hardware acceleration is an optimization layer, not the architecture.

---

# 14. Candidate Technology Stack

This is provisional.

## Core DSP / ML ecosystem

Likely Python initially because the music-analysis ecosystem is strongest there.

Candidate libraries:

- NumPy;
- SciPy;
- librosa;
- soundfile;
- torchaudio where appropriate;
- PyTorch for research/model adapters;
- ONNX Runtime for deployment;
- Essentia;
- aubio.

## Data layer

Initial possibilities:

- structured JSON/MessagePack for portable evidence bundles;
- SQLite for project metadata/indexes;
- NumPy/Zarr/HDF5-style storage for large feature arrays.

Do not bury huge spectrogram arrays directly inside ordinary JSON.

## UI

Requirements matter more than framework choice.

Needs:

- smooth waveform rendering;
- spectrogram rendering;
- timeline synchronization;
- low-latency selection/zoom;
- layered annotations;
- piano roll;
- notation pane;
- tab pane.

Potential directions:

- desktop app with native/web hybrid UI;
- Qt/PySide;
- Tauri + web frontend;
- Electron only if benefits outweigh footprint;
- custom high-performance rendering if necessary later.

Pick after a vertical-slice prototype proves the analysis model.

---

# 15. External/Open-Source Components

We should reuse open-source work aggressively and responsibly.

Candidate projects/components already identified:

- Basic Pitch;
- MT3;
- Omnizart;
- Demucs or maintained derivatives;
- MuseScore;
- music21;
- LilyPond;
- guitar-specific tablature transcription projects;
- research implementations for continuous guitar pitch/string tracking.

Before copying code or binding components tightly, document:

- repository;
- upstream version/commit;
- license;
- whether linked, invoked, vendored, translated, or modified;
- redistribution obligations;
- model-weight licensing separately from source-code licensing.

---

# 16. Licensing Policy

## 16.1 Status: project decision is provisional pending EWC3 Labs policy review

EWC3 Labs currently uses MIT as its documented default and HQ policy presently treats MIT as mandatory
for repositories. During design of this project, that assumption was re-examined.

MIT permits commercial use, modification, redistribution, sublicensing, and proprietary redistribution.
That may be appropriate for some EWC3 Labs work, but it does **not** provide reciprocal source-sharing:
someone may take MIT-licensed EWC3 Labs code, modify it, distribute a proprietary derivative, and owe
the project no source-code contribution back beyond preservation of the required notices.

The Music Forensics Workbench is philosophically better aligned with a **strong copyleft** model:
commercial use should remain allowed, but distributed covered derivatives should preserve source
availability and downstream software freedoms.

The current proposed project license is therefore:

```text
GPL-3.0-only
```

However, Wilson has identified that this question is larger than one repository. EWC3 Labs may choose
to revise its organization-wide licensing model and document the reason for doing so. Until that policy
decision is made, Claude should treat GPL-3.0-only for this repository as **proposed, not yet final**.

See the companion document:

```text
EWC3_Labs_Licensing_Policy_Proposal.md
```

for the organization-wide decision framework and migration plan.

## 16.2 The licensing objective

The desired behavior is not:

> Prevent anyone from making money with EWC3 Labs software.

Open-source software must permit commercial use.

The desired behavior is closer to:

> EWC3 Labs publishes useful work openly. Anyone may use it, study it, modify it, and commercialize it.
> If someone distributes a covered derivative of work released under a reciprocal license, the people
> receiving that derivative should receive the corresponding source and the same essential freedoms.

## 16.3 Code, model weights, and datasets are separate license objects

For this project, never treat "the repo is open source" as a sufficient license audit.

Track independently:

1. source-code license;
2. model architecture/implementation license;
3. pretrained model-weight/checkpoint license;
4. dataset/training-corpus license;
5. generated-artifact restrictions where applicable.

Examples of unsafe assumptions:

```text
repo code is MIT
therefore its weights are MIT                 ← false assumption

model implementation is Apache-2.0
therefore its training data is Apache-2.0     ← false assumption

dataset can be downloaded publicly
therefore we may redistribute it              ← false assumption
```

## 16.4 Required provenance files

Create and maintain from the first dependency onward:

```text
LICENSE
THIRD_PARTY.md
MODELS_AND_DATASETS.md
```

`THIRD_PARTY.md` records, at minimum:

- component/project name;
- upstream URL;
- version, tag, or commit;
- source-code license;
- integration mode: dependency, linked library, subprocess, vendored code, translated code, etc.;
- modifications made by EWC3 Labs;
- attribution/NOTICE requirements;
- compatibility decision.

`MODELS_AND_DATASETS.md` records, at minimum:

- model name;
- implementation source and license;
- weight/checkpoint source and license;
- training dataset(s), if known;
- dataset license(s);
- redistribution rights;
- commercial-use restrictions;
- research-only restrictions;
- whether EWC3 Labs redistributes the asset or downloads it separately at install/runtime.

Unknown licensing status is not "probably okay." It is **unknown**, and unknown assets must not be
redistributed until resolved.

## 16.5 Architecture should reduce licensing coupling

Where practical, keep externally licensed tools behind explicit adapters and ordinary process/data
boundaries.

Examples include:

```text
MusicXML -> MuseScore subprocess -> PDF/SVG
notation source -> LilyPond subprocess -> PDF/SVG
```

This is good architecture regardless of licensing because it keeps the analysis core replaceable.

Do not treat process isolation as a magical legal firewall. Whether components form a derivative or
combined work may depend on facts beyond "we used a subprocess." Architecture reduces coupling and risk;
it does not replace license review.

## 16.6 Upstream code reuse rule

Before borrowing code:

1. identify the exact source and version;
2. read the actual license;
3. verify compatibility with the project license;
4. preserve required notices;
5. document modifications;
6. separately verify any model weights and datasets;
7. do not copy code from repositories with no explicit license grant.

Studying an unlicensed repository for ideas is not the same thing as receiving permission to copy its
implementation.

## 16.7 Do not silently relicense EWC3 Labs history

If EWC3 Labs adopts a new default license, existing MIT releases require a deliberate migration plan.
Changing the license at repository HEAD does not erase rights already granted to recipients of earlier
MIT-licensed versions.

Relicensing an existing codebase also depends on who owns copyright in the current code. If third-party
contributors own portions of the work, a license change may require contributor permission, continued
dual licensing of those portions, or replacement/removal of the affected contribution.

This project should not trigger automatic license changes in other repositories.

---

# 17. Milestone 0 — Project Skeleton

Deliver:

```text
/
├── README.md
├── PROJECT_CHARTER.md
├── LICENSE
├── NOTICE.md
├── THIRD_PARTY.md
├── pyproject.toml
├── src/
│   ├── core/
│   ├── audio/
│   ├── analysis/
│   ├── plugins/
│   ├── evidence/
│   ├── interpretation/
│   ├── export/
│   └── ui/
├── tests/
├── docs/
│   ├── architecture.md
│   ├── evidence-model.md
│   └── licensing.md
└── experiments/
```

Do not overbuild the skeleton.

---

# 18. Milestone 1 — Build the Microscope

No ML required initially.

Load a recording and provide:

- waveform;
- spectrogram;
- playback;
- looping;
- slowdown without pitch shift;
- zoom;
- cursor time;
- manual markers;
- configurable BPM;
- beat/eighth/sixteenth grid overlay;
- manual barline placement.

Success criterion:

Wilson can inspect the Jimmy Page intro more effectively than with paper and repeated playback.

---

# 19. Milestone 2 — Attack Detection and Meter Experiments

Add:

- onset detection;
- onset markers;
- onset confidence;
- tempo estimation;
- beat tracking;
- downbeat tracking;
- forced meter;
- competing meter hypotheses.

First research question:

> Can the application objectively show the attack displacement in the "Over the Hills and Far Away" intro and its subsequent realignment to the underlying grid?

---

# 20. Milestone 3 — Pitch Evidence

Add:

- monophonic continuous F0;
- polyphonic pitch candidates;
- piano-roll visualization;
- continuous bends;
- note grouping/quantization;
- confidence.

Do not flatten expressive pitch motion.

---

# 21. Milestone 4 — Source Separation

Add:

- HPSS;
- stem separator adapter;
- stem waveform/spectrogram views;
- solo/mute;
- analyzers selectable per stem.

---

# 22. Milestone 5 — Notation

Add internal musical interpretation sufficient to export:

- MIDI;
- MusicXML.

Use an existing engraver for:

- standard notation;
- PDF/SVG output.

Then add initial piano reduction.

---

# 23. Milestone 6 — Guitar Tab

Add:

- tuning model;
- string/fret solver;
- alternative fingering candidates;
- bend-aware representation;
- ASCII/debug tab;
- MusicXML/native tab export where practical.

The same note sequence should support multiple tab hypotheses.

---

# 24. Milestone 7 — Analysis Ecosystem

Add plugin discovery and third-party analyzers.

Long-term goal:

Someone should be able to write:

```python
class MyRidiculousAnalyzer(AnalyzerPlugin):
    ...
```

install it, run it against a region, and have its results appear as a first-class evidence layer without modifying the core application.

---

# 25. Non-Goals for Early Versions

Do **not** initially attempt:

- perfect full-band transcription;
- perfect instrument separation;
- perfect meter inference;
- DAW replacement;
- professional notation editor replacement;
- automatic musicological truth;
- cloud service;
- massive foundation-model training.

The first goal is a useful microscope.

---

# 26. Definition of Done for an Analysis Result

An analysis result is not complete merely because it emits a label.

Where practical, it should contain:

- result;
- timestamp/region;
- confidence;
- algorithm/model identity;
- algorithm/model version;
- parameters;
- input layer;
- derived-from links;
- reproducibility metadata.

This is foundational to forensic inspection.

---

# 27. Reproducibility

Analysis runs should be recordable.

Conceptually:

```json
{
  "plugin": "basic_pitch",
  "version": "x.y.z",
  "parameters": {},
  "input": "stem:guitar:sha256...",
  "created_results": [
    "event:123",
    "event:124"
  ]
}
```

Users should eventually be able to rerun an analysis after:

- changing a parameter;
- changing tempo;
- moving a barline;
- replacing a model;
- selecting another stem;
- forcing an instrument identity.

Dependent interpretations can then invalidate/recompute.

---

# 28. Human-in-the-Loop Model

Manual intervention is a feature.

Support commands conceptually equivalent to:

- "This is beat one."
- "Assume 91 BPM."
- "Assume 4/4."
- "Do not assume meter."
- "That note is wrong; this is F#."
- "Treat this as guitar."
- "The guitar is in DADGAD."
- "Try standard tuning."
- "This region is a pickup."
- "Ignore drum transients here."

Manual facts become constraints in subsequent analysis.

---

# 29. Research Questions

Interesting longer-term questions include:

- Can barline perception be inferred separately from physical onset timing?
- Can competing metric interpretations be ranked rather than collapsed?
- Can guitar string identity be inferred reliably from spectral/timbral evidence?
- Can expressive bends be reconstructed from a dense mix?
- Can instrument geometry improve transcription accuracy?
- Can source-separation uncertainty propagate into transcription confidence?
- Can automatic transcription report *where it knows it is probably wrong*?
- Can human edits become training/evaluation data without contaminating canonical source evidence?
- Can computational analysis identify rhythmic illusions that are easy to feel but hard to notate?

---

# 30. Naming

"SoundLab" is almost certainly too generic.

Previously discussed directions:

- Wavewright
- Sonic Lens
- Fourier Forge
- Signal Forge
- ToneTrace
- WaveTrace
- PhaseLab
- Resonance Engine

No final name has been selected.

Use **Music Forensics Workbench** as a working project name until naming is resolved.

---

# 31. Claude Implementation Guidance

Claude should treat this document as the architectural source of truth until superseded by repository docs or explicit Wilson instructions.

## Initial task sequence

1. Create the repository skeleton.
2. Write a minimal architecture document.
3. Define the evidence/provenance data model before implementing transcription.
4. Implement Milestone 1 as the first vertical slice.
5. Keep DSP and ML analyzers behind interfaces.
6. Avoid premature distributed architecture.
7. Keep the application local-first.
8. Add dependency/license metadata as components are introduced.
9. Build automated tests around timing math and evidence transformations.
10. Preserve the raw timestamps of observed events independently from musical quantization.

## Engineering bias

Prefer:

- composability;
- debuggability;
- evidence retention;
- deterministic reproducibility;
- replaceable models;
- explicit timebases;
- observability;
- boring interfaces around interesting algorithms.

Avoid:

- opaque pipelines;
- hard-coded model assumptions;
- throwing away intermediate representations;
- letting the UI data model become the canonical data model;
- treating MIDI as ground truth;
- silently quantizing uncertain events;
- coupling core analysis to one ML framework;
- solving engraving from scratch.

---

# 32. Project Motto

> **Build the microscope you wish you had.**

Or, less formally:

> Wilson was not about to draw all that shit on paper.
