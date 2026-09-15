# MW-2 — Milestone 1: the microscope

> **Keep this doc small.** One slice or one fix. If it grows past roughly a page, either the slice is
> really several slices, or it belongs in `modules/`. Architecture goes to `docs/`, investigation to
> `docs/analysis/`, and how-a-hard-problem-was-solved to `docs/RAG_Sessions/`.

| | |
| --- | --- |
| **State** | ⬜ planned |
| **Est** | L |
| **Roadmap** | [`MusicForensics_Workbench_Development_Roadmap.md`][musicforensics] |

## What and why

Load a recording and look at it closely: waveform, spectrogram, playback, a loop, slowdown without
pitch shift, zoom, a cursor time, manual markers, a configurable BPM, a beat/eighth/sixteenth grid
overlay, and manual barlines. No ML. This is charter §18, and it is the first time the evidence
model meets real signal. **The success criterion is the charter's:** Wilson can inspect the intro to
"Over the Hills and Far Away" more effectively than with paper and repeated playback.

## Steps

Headless pieces come first, because they are the ones that last. Each lands with tests over
synthetic signals.

- [ ] **Load.** WAV and FLAC to start, through one decoder recorded in provenance. A loaded
      recording carries its `Timebase`, and every position leaving it is in seconds.
- [ ] **Waveform and spectrogram data.** Min/max peaks at several resolutions, and an STFT keyed by
      its parameters (`n_fft`, hop, window). The STFT is a recomputable view, not a claim.
- [ ] **Human claims.** Markers, barlines, beat one, and "assume N BPM" are `Claim`s with
      `source="human"` and an actor. The grid is **one** claim, a tempo hypothesis citing its
      anchor. Its lines are rendering.
- [ ] **Playback.** Loop a region and slow it down without changing pitch. `rate` is source seconds
      per playback second, so half speed is `0.5`. Inside a loop from `a` to `b`, playback time `p`
      maps to source seconds `a + ((p · rate) mod (b − a))`. Test it slowed: at half speed an
      inverted ratio lands at `a + 2p` before wrapping, which looks plausible and is wrong.
- [ ] **Prototype viewer.** A spike to wire zoom, cursor, overlays, and marker placement onto the
      pieces above. **Disposable by declaration.** MW-8 picks the real UI framework after this.
- [ ] **The session.** Wilson works the intro on his own machine, with his own copy of the
      recording.

## Watch out for

- **The recording never enters the repo.** The repo is public and the track is copyrighted.
  `.gitignore` covers media files (fixed for the package in FIX-1), and tests synthesize their
  signals.
- **MP3 shifts time.** A typical LAME encode plus decode adds 1,105 samples of delay, 25 ms at 44.1
  kHz. That is about 15% of a sixteenth note at 90 BPM, and decoders do not agree on trimming it.
  That is why WAV and FLAC come first. When MP3 arrives, the decoder goes in provenance.
- **A marker placed by ear is late.** Output latency and reaction time both delay it, and slowed
  playback changes how much. Record the playback rate on the claim; do not correct it silently.
- **A marker never snaps.** Snapping to the grid is a derived claim that cites the marker, and the
  raw seconds survive. This is the rule the evidence model exists for.
- **Viewer state is not evidence.** Zoom, loop region, and scroll are UI state. Markers, barlines,
  and the tempo hypothesis live in the `EvidenceGraph`, never only in a widget.
- **Every dependency brings a `THIRD_PARTY.md` row in the same change.** Time stretchers vary on
  license, and a GPL one narrows the open licensing question. Prefer permissive where quality
  allows, and write the decision down.

## Done when

- 🟦 **tested:** load, peaks, STFT, human claims, and the playback mapping have tests over synthetic
  signals that CI runs. One of them stretches a 440 Hz sine to half speed and checks that it lasts
  twice as long and is still 440 Hz.
- 🟩 **proven:** in one session on the intro, Wilson loops a region, slows it down and hears the
  pitch hold, zooms to individual attacks, sets a BPM and sees the grid, and places markers and
  barlines. They survive as human claims with their raw seconds, and Wilson says it beat paper.
  `Status` names the machine and the recording.

## Links

- **[Project charter §4 and §18](../../PROJECT_CHARTER.md)** — *the Jimmy Page problem, and
  Milestone 1's feature list.*
- **[Evidence model](../../evidence-model.md)** — *claims, human provenance, and why quantization
  derives.*
- **[Architecture](../../architecture.md)** — *why the viewer is not the canonical model, and why
  the UI framework waits.*

[musicforensics]: ../MusicForensics_Workbench_Development_Roadmap.md
