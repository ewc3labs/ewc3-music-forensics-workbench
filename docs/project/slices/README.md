# Music Forensics Workbench — Slices

**One slice or one fix per file.** These are the tiny execution docs the roadmap's Delivery Index
points at, so that table rows can stay one line instead of swelling into paragraphs.

## Naming

```text
<SLICE_ID>_<Short_Title>.md      e.g.  MW-2_Microscope.md,  FIX-1_Timebase_Rounding.md
```

The filename is the interface. Someone scanning this folder — or the roadmap's `Doc` column, which
pins these filenames — should know what a doc is without opening it. Never `MW-2.md`, never
`notes.md`.

## What goes in one

Execution detail: what to do, in what order, what will bite you, and how you will know it is done.
Template: `ewc3labs-hq/templates/project/template_project_slice.md`. **Keep it to about a page.**

**`Est` uses the roadmap's sizes** — `S`, `M`, `L`, `XL` — not day counts.

**`Done when` must say where it was proven.** For analysis work the real environment is a real
recording checked by a human; a green test run over synthetic fixtures is `🟦 tested`, not
`🟩 proven`. See the States legend in the roadmap.

## What does not

| Content | Home |
| --- | --- |
| architecture, and *why*, options rejected | `docs/` design documents |
| current-state investigation and evidence | `docs/analysis/` |
| how a hard problem was actually solved | `docs/RAG_Sessions/` |
| sequencing and priority | the roadmap's Current Focus |
| several slices in one subsystem | `modules/` |
| experiment code and notebooks | `experiments/` |

## Lifecycle

A slice doc closes when the slice ships. Delete it or leave it as history — but do not let a
finished slice doc sit in the folder pretending to be active work. The roadmap row's state is the
truth.
