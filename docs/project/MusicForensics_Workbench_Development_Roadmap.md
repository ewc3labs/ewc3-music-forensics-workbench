<div align="center">
<table>
<tr>
<td style="padding: 0 40px; vertical-align: middle;">
<img src="../../images/EWC3LabsLogo-blue-128x128.png" alt="EWC3 Labs" width="72" height="72">
</td>
<td style="vertical-align: middle;">
<h1 style="margin: 0;">Music Forensics Workbench</h1>
<h3 style="margin: 5px 0;"><strong>Development Roadmap — where we are, and what is next</strong></h3>
</td>
</tr>
</table>
</div>

---

AsOf: 2026-09-14

## Current Focus

1. `MW-2` — next
2. `MW-3` — after MW-2

## ID Prefixes

Read this **before** minting an ID. It sits above the tables because it is an input to writing one,
not a summary of them.

**Keep `Prefix` as the first column header.** `ewc3-docs series` locates this table by that word and
by nothing else. Rename it and the table is silently not read, and every ID below goes unchecked.

| Prefix | Scope | Owner | Last Used | Series |
| --- | --- | --- | --- | --- |
| MW | global | ewc3-music-forensics-workbench | <!--ewc3:lastMW-->MW-8<!--/ewc3:lastMW--> | milestones, slices and features |
| FIX | repo-local | ewc3-music-forensics-workbench | <!--ewc3:lastFIX-->FIX-0<!--/ewc3:lastFIX--> | small corrections not worth a slice |

`Last Used` is a cache over the Delivery Index, not a second source of truth — the IDs in the tables
are authoritative. It is derived by the `lastId` resolvers in `.ewc3-docs.json`: `ewc3-docs fix`
keeps the cell current and `check` fails when it drifts. **Do not hand-edit it.**

**Max, never a count.** Counting rows agrees with the highest ID only while a series is contiguous,
and starts handing out taken numbers the moment one entry is retired.

**Why `MW` and not `MF`.** The obvious abbreviation of "Music Forensics" has other connotations, and
an ID series gets typed into commit messages, issue titles, and conversations with people who do not
have the context. `MW` for *Music Workbench* costs nothing and avoids the joke entirely.

**`FIX` is repo-local canon** — every roadmap owns its own. `MW` is registered in the [EWC3 Prefix
Registry][prefix-registry].

## States

Read this **before** choosing a row's state. It sits above the tables for the same reason ID
Prefixes does: it is an input to writing a row, not a summary of them.

| | State | Means |
| --- | --- | --- |
| ⬜ | `planned` | minted, not started |
| 🟨 | `coded` | built, and never run against anything |
| 🟦 | `tested` | unit or smoke tested — probably OK, not proven |
| 🟩 | `proven` | met a **real environment** — `Status` must name *where* |
| ✅ | `done` | complete, and **not software**, so the ladder above does not apply |
| ⛔ | `blocked` | off the ladder — waiting on someone or something |
| ⏸️ | `deferred` | off the ladder — not now, **may return** |
| 🟥 | `cancelled` | off the ladder — decided against; `Status` says `reverted`, `refuted` or `retired`, and why |

**🟩 must name *where*.** `proven 2026-09-14 — work PC, P:\ share`, never a bare `proven`. A proof
is a claim *and the environment it held in*, so a later break somewhere else reads as a gap in scope
rather than a lie. **The where has to be the real environment for that kind of work:** CI is the
real environment for CI tooling, and only a test bench for a product feature.

**✅ is for work that could not be tested at all** — a reply sent, a pattern retired, a guide
written. If a row is software it belongs on the ladder, and ✅ on it is a mislabel.

**Never round up.** If the record does not show which rung a row reached, it is 🟨, with the doubt
in `Status`. **Keep 🟥 rows** — a refuted finding is the record of *why not*, and the next person to
report the same thing needs to find it.

**Est:** `S` an hour or two · `M` a session · `L` several sessions · `XL` a project in itself. Day
counts are fake precision on a project nobody is scheduling. Sizes are for spotting what is big.

`Status`: `pending` · `started YYYY-MM-DD` · `proven YYYY-MM-DD — {where}` ·
`done YYYY-MM-DD — {what done means}` · `deferred — {condition}` · `blocked on {who/what}` ·
`cancelled — {reverted|refuted|retired}: {why}` · `seen again YYYY-MM-DD`

**For this project, a real environment means real recordings.** Until an analyzer has run over
actual audio and a human has checked what it claimed, nothing here is 🟩 — a green CI run over
synthetic fixtures is 🟦.

## Delivery Index

Every slice lives here — active, planned, deferred, cancelled — distinguished by state. There is no
separate backlog doc and no separate status file.

**Rows are one line.** `Doc` pins a filename; anything wanting a paragraph wants a slice doc.

### The product

The analysis features that are the reason the project exists. Keeping these in their own table is a
standing check against building infrastructure and calling it progress.

| ID | State | Slice | Est | Doc | Status |
| --- | --- | --- | --- | --- | --- |
| MW-2 | ⬜ planned | Milestone 1: the microscope — waveform, spectrogram, playback | L | [architecture](../architecture.md) | pending — no ML; first test of the evidence model against real signal |
| MW-4 | ⬜ planned | Milestone 2: onset detection and meter experiments | L | — | pending — the Jimmy Page question, stated as an experiment rather than a feature |
| MW-5 | ⬜ planned | Milestone 3: continuous pitch tracking | L | — | pending — contours, not immediate MIDI quantization; bends and vibrato must survive |
| MW-7 | ⬜ planned | Milestone 4: source separation | L | — | pending — likely the first model, so a MODELS_AND_DATASETS row comes first |

### Foundations

The evidence model and the machinery every analyzer stands on.

| ID | State | Slice | Est | Doc | Status |
| --- | --- | --- | --- | --- | --- |
| MW-1 | 🟦 tested | Milestone 0: skeleton, evidence model, provenance files | M | [evidence-model](../evidence-model.md) | tested 2026-08-17 — 21 unit tests green in CI on py3.11–3.13; no audio consumes it yet |
| MW-3 | ⬜ planned | Evidence bundle serialization | M | [evidence-model](../evidence-model.md) | pending — large arrays stay out of plain JSON; MessagePack, Zarr or HDF5 still open |
| MW-6 | ⬜ planned | Plugin interface for third-party analyzers | M | [architecture](../architecture.md) | pending — same interface as built-ins, or built-ins quietly get privileges |
| MW-8 | ⬜ planned | Pick the UI framework | M | [architecture](../architecture.md) | pending — after a vertical slice proves the analysis model, not before |

## Working Rules

- The roadmap is the single planning surface and owns the status of everything minted into it.
- New work arrives via the punchlist and is promoted here once the problem is understood well enough
  to describe with receipts.
- Backlogging = state `⏸️ deferred`, with the admission condition in `Status`.
- Technical detail lives in `docs/` design documents; rows link, they do not duplicate.
- Load the `ewc3labs-project-roadmap` skill before structural edits.
- **Do not overbuild the skeleton.** The charter says it twice and it is the easiest instruction
  here to violate while feeling productive. Empty packages are cheaper to fill than speculative
  abstractions are to delete.
- **Deferred on purpose:** UI framework, storage format, which ML models, and the project's actual
  name. Each would feel like progress and would mostly be guessing.
- **Every model is a licensing object as well as a technical one.** A model gets a
  [MODELS_AND_DATASETS][models-and-datasets] row *before* it is wired in, because the answer
  sometimes disqualifies it.

## Related Documentation

- **[Project Charter](../PROJECT_CHARTER.md)** | [GitHub Link 🔗][github-link]
  - *The founding brief: what the workbench is for, and the order to build it in.*
- **[Architecture](../architecture.md)** | [GitHub Link 🔗][github-link-2]
  - *Package layout and the boundaries between analysis, evidence, and interpretation.*
- **[Evidence Model](../evidence-model.md)** | [GitHub Link 🔗][github-link-3]
  - *Claims, provenance, graph invariants, and explicit timebases.*
- **[Models and Datasets][models-and-datasets]** | [GitHub Link 🔗][github-link-4]
  - *License record for every model and dataset, filled before anything is wired in.*

[github-link]: https://github.com/ewc3labs/ewc3-music-forensics-workbench/blob/main/docs/PROJECT_CHARTER.md
[github-link-2]: https://github.com/ewc3labs/ewc3-music-forensics-workbench/blob/main/docs/architecture.md
[github-link-3]: https://github.com/ewc3labs/ewc3-music-forensics-workbench/blob/main/docs/evidence-model.md
[github-link-4]: https://github.com/ewc3labs/ewc3-music-forensics-workbench/blob/main/MODELS_AND_DATASETS.md
[models-and-datasets]: ../../MODELS_AND_DATASETS.md
[prefix-registry]: https://github.com/ewc3labs/ewc3labs-hq/blob/main/docs/project/EWC3_Prefix_Registry.md
