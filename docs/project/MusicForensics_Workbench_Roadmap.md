# Music Forensics Workbench — Development Roadmap

## Current Focus

**Milestone 0 is done.** There is an evidence model, a test suite around timing math and evidence
transformations, and documentation. Nothing loads audio yet, which is the intended order: the
charter says define the evidence and provenance model before implementing transcription, because
everything downstream inherits its shape from it.

Next is `MW-2` — the microscope. Waveform, spectrogram, playback, no ML. The first real test of
whether the evidence model survives contact with actual signal.

## ID Prefixes

**Read this before minting an ID.** It sits above the tables because it is an input to writing one,
not a summary of them.

| Prefix | Scope | Owner | Last Used | Series |
| --- | --- | --- | --- | --- |
| MW | global | ewc3-music-forensics-workbench | <!--ewc3:lastMW-->MW-8<!--/ewc3:lastMW--> | milestones, slices and features |
| FIX | repo-local | ewc3-music-forensics-workbench | <!--ewc3:lastFIX-->FIX-0<!--/ewc3:lastFIX--> | small corrections not worth a slice |

**Last Used is derived** from the tables below by `ewc3-docs values`, and CI fails if it is stale.
**Max, not a count** — counting rows agrees with the highest ID only while a series is contiguous.

**Why `MW` and not `MF`.** The obvious abbreviation of "Music Forensics" has other connotations, and
an ID series gets typed into commit messages, issue titles, and conversations with people who do not
have the context. `MW` for *Music Workbench* costs nothing and avoids the joke entirely.

`FIX` is repo-local and that is canon — every roadmap owns its own. See the [prefix
registry][prefix-registry].

## Delivery Index

**Rows are one line.** Anything wanting a paragraph wants a slice document.

| ID | State | Slice | Est | Doc | Status |
| --- | --- | --- | --- | --- | --- |
| MW-2 | ⬜ planned | Milestone 1: the microscope — waveform, spectrogram, playback | L | [architecture](../architecture.md) | no ML. First real test of whether the evidence model survives contact with signal |
| MW-3 | ⬜ planned | Evidence bundle serialization | M | [evidence-model](../evidence-model.md) | large arrays must not land inside ordinary JSON; format still open between MessagePack, Zarr and HDF5 |
| MW-4 | ⬜ planned | Milestone 2: onset detection and meter experiments | L | — | the Jimmy Page question, stated as an experiment rather than a feature |
| MW-5 | ⬜ planned | Milestone 3: continuous pitch tracking | L | — | contours, not immediate MIDI quantization — bends and vibrato have to survive |
| MW-6 | ⬜ planned | Plugin interface for third-party analyzers | M | [architecture](../architecture.md) | same interface as built-ins, or built-ins quietly get privileges |
| MW-7 | ⬜ planned | Milestone 4: source separation | L | — | first component likely to bring a model, and therefore a MODELS_AND_DATASETS row |
| MW-8 | ⬜ planned | Pick the UI framework | M | [architecture](../architecture.md) | after a vertical slice proves the analysis model, not before |

## Done

| ID | State | Slice | Est | Doc | Status |
| --- | --- | --- | --- | --- | --- |
| MW-1 | ✅ done | Milestone 0: skeleton, evidence model, provenance files | M | [evidence-model](../evidence-model.md) | claims, provenance, graph invariants, explicit timebases; 21 tests |

## Notes

**Do not overbuild the skeleton.** The charter says it twice and it is the easiest instruction here
to violate while feeling productive. Empty packages are cheaper to fill than speculative
abstractions are to delete.

**Deferred on purpose:** UI framework, storage format, which ML models, and the project's actual
name. Each would feel like progress and would mostly be guessing.

**Every model is a licensing object as well as a technical one.** A model gets a
[MODELS_AND_DATASETS][models-and-datasets] row *before* it is wired in, because the answer sometimes
disqualifies it.

[models-and-datasets]: ../../MODELS_AND_DATASETS.md
[prefix-registry]: https://github.com/ewc3labs/ewc3labs-hq/blob/main/docs/project/EWC3_Prefix_Registry.md
