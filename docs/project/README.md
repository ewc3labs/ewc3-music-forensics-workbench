<div align="center">
<table>
<tr>
<td style="padding: 0 40px; vertical-align: middle;">
<img src="../../images/EWC3LabsLogo-blue-128x128.png" alt="EWC3 Labs" width="72" height="72">
</td>
<td style="vertical-align: middle;">
<h1 style="margin: 0;">Music Forensics Workbench</h1>
<h3 style="margin: 5px 0;"><strong>Project Planning Surface — roadmap, intake, and slice docs</strong></h3>
</td>
</tr>
</table>
</div>

---

## Purpose

`docs/project/` is the durable planning surface for upcoming work.

Use this folder to track slice sequencing and the slice or module documents that need to stand on
their own. Do not use it for generated output, analysis results, or chronological progress evidence;
those belong elsewhere.

## Contents

```text
docs/project/
├── MusicForensics_Workbench_Development_Roadmap.md
├── MusicForensics_Workbench_Checkin_Punchlist.md
├── modules/
│   └── README.md
└── slices/
    └── README.md
```

## Conventions

- **The roadmap is the single planning surface.** Its Delivery Index holds every slice — active,
  planned, and backlogged — distinguished by state. Backlogging means setting `⏸️ deferred` (or
  `🟥 cancelled`) on the row; there is no separate backlog document. Current Focus is the ordered
  delivery queue.
- **The punchlist is the intake surface.** Check-ins, smoke-test findings, and enhancement requests
  land there as newest-first sections, then get reconciled into roadmap slices and checked off.
- **The roadmap's ID Prefixes table is the ID registry.** Mint `MW` and `FIX` IDs only against it,
  including IDs assigned while reconciling the punchlist.
- **`slices/` holds one slice or fix per file**, for work that is risky, multi-session, or needs a
  handoff. **`modules/` holds a subsystem spanning several slices.** Default to slices.
- **Design stays in `docs/`.** [Architecture][architecture] and the [evidence model][evidence-model]
  are the technical anchors; roadmap rows and slice docs link to them rather than restating them.
- **What shipped** lives in git history and GitHub Releases. This folder is for sequencing, scope,
  and what is next.
- **Public, reproducible bugs go to GitHub Issues.** The punchlist is a notebook, not a shadow
  tracker.

Templates for every file here live in `ewc3labs-hq/templates/project/`.

## Key Files

| Path | Purpose | Notes |
| --- | --- | --- |
| `./MusicForensics_Workbench_Development_Roadmap.md` | Slice index, States legend, and the ordered delivery queue. | Start here when deciding what to work on next. |
| `./MusicForensics_Workbench_Checkin_Punchlist.md` | Intake journal, reconciled into roadmap slices. | Capture here first; check off once the roadmap records the item. |
| [`./slices/`](slices/README.md) | One execution doc per slice or fix. | Named `<ID>_<Short_Title>.md`, pinned by the roadmap's `Doc` column. |
| [`./modules/`](modules/README.md) | One plan per subsystem spanning several slices. | Only when separate slice docs lose the thread. |

## Related Documentation

### Planning Surface

- **[Development Roadmap][development-roadmap]** | [GitHub Link 🔗][github-link]
  - *The single planning surface: slice index, states, and ordered delivery queue.*
- **[Check-in Punchlist][check-in-punchlist]** | [GitHub Link 🔗][github-link-2]
  - *Intake journal; every item reconciles into a roadmap slice and gets checked off.*

### Supporting Reference

- **[Architecture](../architecture.md)** | [GitHub Link 🔗][github-link-3]
  - *Layers, boundaries, and what is deliberately still undecided.*
- **[Evidence Model](../evidence-model.md)** | [GitHub Link 🔗][github-link-4]
  - *Claims, provenance, graph invariants, and explicit timebases.*

## Maintenance

- Keep the roadmap narrow and reviewable; do not turn it into a changelog.
- Backlog by state, not by file: a candidate slice enters the Delivery Index as `⏸️ deferred` with
  its admission condition in `Status`.
- When deferred and cancelled rows clutter the active view, move them to a Parked / Retired table at
  the bottom of the roadmap — never to a separate file.
- If a planning decision becomes architectural doctrine, promote it into `docs/` rather than leaving
  it only here.

[architecture]: ../architecture.md
[check-in-punchlist]: ./MusicForensics_Workbench_Checkin_Punchlist.md
[development-roadmap]: ./MusicForensics_Workbench_Development_Roadmap.md
[evidence-model]: ../evidence-model.md
[github-link]: https://github.com/ewc3labs/ewc3-music-forensics-workbench/blob/main/docs/project/MusicForensics_Workbench_Development_Roadmap.md
[github-link-2]: https://github.com/ewc3labs/ewc3-music-forensics-workbench/blob/main/docs/project/MusicForensics_Workbench_Checkin_Punchlist.md
[github-link-3]: https://github.com/ewc3labs/ewc3-music-forensics-workbench/blob/main/docs/architecture.md
[github-link-4]: https://github.com/ewc3labs/ewc3-music-forensics-workbench/blob/main/docs/evidence-model.md
