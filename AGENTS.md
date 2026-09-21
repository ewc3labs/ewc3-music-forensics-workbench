# AGENTS.md — ewc3-music-forensics-workbench

> **This file adds to `ewc3labs-hq/AGENTS.md`; it never weakens it.** The HQ baseline carries the
> identity, tone, method and engineering discipline for every EWC3 Labs repo. Repeat none of it here.
> Write only what an agent would get **wrong** in this repository without being told.
>
> Precedence: platform instructions → HQ baseline → this file → `.github/copilot-instructions.md`.

---

## Read this first

- **[docs/PROJECT_CHARTER.md](docs/PROJECT_CHARTER.md)** — the architectural source of truth until a
  repository document or Wilson supersedes it. It settles the build order (evidence model before
  transcription), the first test case, and the milestone contents. Most "should we just…" questions
  are already answered there, usually with a reason.
- **[docs/evidence-model.md](docs/evidence-model.md)** — read before writing any analyzer.
  Everything downstream inherits its shape, and the rules below are enforced in code.

## What this actually is

A workbench for interrogating a recording until its structure becomes visible, and for showing *why*
an analyzer reached a conclusion. **It is not "audio in, sheet music out."** It is not a DAW, not a
notation editor, and not a transcription service: those all end at an answer, and the answer is the
least interesting output here. Analyzers produce competing, attributed claims; a human decides.

## The constraint that bites

**A convenient shortcut through the evidence model is always available and always wrong.** Writing a
"resolved" value, snapping a measurement to a grid, or letting an analyzer edit another's output
costs nothing today and destroys the record that makes the tool worth building. `Claim.derive()`
exists so ancestry cannot be forgotten, and `EvidenceGraph` refuses dangling ancestry at insertion.
Work with those, never around them.

The trap that has already cost real time: **`.gitignore` data patterns silently swallowing source.**
An unanchored `audio/` pattern matched `src/workbench/audio/`, so that package was never committed
and a fresh clone did not have it — CI stayed green because nothing imported it yet (FIX-1,
526faa7). Anchor data-folder patterns to the repo root, and when a new package appears under `src/`,
run `git check-ignore -v` on it.

## Architecture, in the amount an agent needs to not break it

- **Dependencies point inwards toward `evidence/`.** An analyzer emits claims; it does not know what
  the interpretation layer does with them, and it never knows about the UI.
- **No analyzer owns the truth.** Two analyzers disagreeing is a normal state, surfaced by
  `EvidenceGraph.disagreements(kind)`, not an error to resolve before storage.
- **Quantization derives, it never edits.** A beat claim cites the onset claim; the raw measured
  seconds survive untouched.
- **The UI data model is not the canonical data model.** Zoom, loop regions and scroll are viewer
  state. Markers, barlines and hypotheses are claims.
- **Timebases are explicit**, and seconds are the interchange unit. A bare float called `t` is how
  sample indices end up compared against seconds.

## Scope, and what is deliberately out

In flight is `MW-2`, the microscope: waveform, spectrogram, playback, loop, slowdown, zoom, manual
markers and a tempo grid. **No ML.** See the [roadmap][roadmap] for what is minted and what is next.

Deliberately out, and each would feel like progress: the UI framework choice (`MW-8`, after a
vertical slice proves the model), the storage format (`MW-3`, after there are real arrays to choose
against), which ML models, notation and tablature output, and the project's final name.

## Repo standards

- **Language and toolchain** — Python ≥ 3.11, `pyproject.toml`, ruff and pytest. `make test`,
  `make lint`, `make verify`. `make fix` rewrites; `make verify` only asks.
- **Layout** — `src/workbench/` with
  `audio/ analysis/ evidence/ interpretation/ export/ plugins/ ui/ core/`, `tests/`, `experiments/`
  for throwaway probes, `docs/` for everything written down.
- **Tests** — `pytest -q`; green means all pass. Tests **synthesize their signals**; no recording is
  ever committed. Concentrate tests on timing math and evidence transformations, where a mistake is
  silent because a wrong number still renders.
- **CI** — `ci.yml` runs ruff and pytest on 3.11, 3.12 and 3.13 and ignores documentation paths;
  `docs.yml` runs `ewc3-docs check` on documentation changes. Both gate a PR.
- **Licensing is load-bearing here.** A dependency gets its `THIRD_PARTY.md` row **in the same
  change** that adds it, with its integration mode. A model gets a `MODELS_AND_DATASETS.md` row
  **before** it is wired in, because the answer sometimes disqualifies it. Code, weights and
  training data are three separate license objects. The project licence is GPL-3.0-only,
  provisional.
- **Public repo** — nothing machine-specific, no absolute paths, no credentials or audio in
  fixtures. The source recordings are copyrighted and stay on the machine that owns them.

## Files this repo does NOT commit

Tooling writes into working trees. **Decide per file by what reads it:**

| File | Read by | Verdict |
| --- | --- | --- |
| `AGENTS.md`, `.github/copilot-instructions.md` | every clone, and GitHub | **tracked** — authored, reviewed, useful to others |
| `CLAUDE.md`, `.codex/`, `.cavemanrc` | one machine's tooling, rewritten on open | **ignored** — machine-local, not repo canon |
| `.aicache/`, `.codegraph/` | one machine's caches and indexes | **ignored** |
| `.vscode/settings.json` | this editor, on this machine | **ignored** — this repo is public, and the AI extension writes absolute user paths into it. Shared editor settings belong in the multi-root `.code-workspace` instead |

Audio, feature arrays and model weights are ignored by extension and by root folder, for size and
for licence. Anchor any new folder pattern to the repo root.

**A tracked file is not automatically a checked one.** `format` and `values` act on
`.ewc3-docs.json`'s `include`, which defaults to `README.md` plus `docs/**.md` — a new root document
is checked by nothing while the run still reports green. `AGENTS.md` is in `include` for that
reason; adding it raised the file count from 11 to 12 and immediately found it unformatted.
`.github/copilot-instructions.md` is deliberately **out**: `format` would rewrap lines inside the
generated block, and the extension would rewrite them back on the next workspace open.

## Conventions inherited from the org

- `docs/project/` roadmap, punchlist and slices · `docs/RAG_Sessions/` how a hard problem was
  actually solved. Design currently lives in flat documents under `docs/`; `docs/design/` and
  `docs/analysis/` appear when there is something to put in them.
- Roadmap states, ID prefixes and the thin-table rule: load the `ewc3labs-project-roadmap` skill.
- Branching, review and merge policy:
  `ewc3labs-hq/docs/project_development/Branch_And_Review_Discipline.md`.
- LF everywhere, enforced by `.gitattributes` and `.editorconfig`.

## When in doubt

The charter decides, until a repository document or Wilson supersedes it. The [roadmap][roadmap]
owns the status of everything minted, and its Current Focus says what is actually next. MW owns this
lane; LabsHQ owns estate-wide rulings.

The question worth asking before building rather than after: **what claim does this produce, and
what does it cite?** Anything that cannot answer that is probably a shortcut through the evidence
model.

[roadmap]: docs/project/MusicForensics_Workbench_Development_Roadmap.md
