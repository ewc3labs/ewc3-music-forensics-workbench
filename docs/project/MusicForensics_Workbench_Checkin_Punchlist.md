<div align="center">
<table>
<tr>
<td style="padding: 0 40px; vertical-align: middle;">
<img src="../../images/EWC3LabsLogo-blue-128x128.png" alt="EWC3 Labs" width="72" height="72">
</td>
<td style="vertical-align: middle;">
<h1 style="margin: 0;">Music Forensics Workbench</h1>
<h3 style="margin: 5px 0;"><strong>Check-in Punchlist — stuff we noticed, and what is still open</strong></h3>
</td>
</tr>
</table>
</div>

---

Started: 2026-09-14

## How this works

Things we saw happening and need to address **sometime**. No evidence required to write one down —
that is the point. An item can sit here indefinitely without guilt.

An item is promoted to a roadmap slice **once someone has done enough analysis to document the
problem with receipts** — not when it gets scheduled, not when it feels important, but when it is
understood well enough to describe honestly.

**Unchecked items are "what's still open."** That is the whole status mechanism; there is no
separate status file.

| Mark | Means |
| --- | --- |
| `- [ ]` | open — noticed, not yet understood |
| `- [~]` | being looked at |
| `- [x]` | minted into the roadmap, or just delivered |

A checked item names its slice: `[MW-nn] minted in roadmap to address`. `[ ]` and `[x]` render as
real checkboxes in Markdown Preview, so either of us can tick them. `[~]` is not task-list syntax
and renders as plain text; that is acceptable for a short-lived marker, but tick or clear it when
the look is over.

**Before minting anything new, search the roadmap.** The same thing gets noticed months apart, and
it usually already has a row. Fold it in rather than duplicating, and treat the re-report as a
signal that the deferral was wrong.

Newest section on top. Older sections are append-only history: never rewrite them except to tick a
box or add a slice ID.

---

## Check-in — 2026-09-14 (MW takes ownership; planning surface stood up)

> Context: the repo changed hands to MW. HQ-3 moved the roadmap onto the canonical template and States
> legend, which regraded MW-1 from done to tested. Wilson then asked for the rest of the planning
> surface before any slice work begins.

**Decisions (Wilson, 2026-09-14):**

- "Tooling up for proper development slices is your first task after fixing the roadmap to agree
  with the canonical template." The punchlist, `slices/` and `modules/` are stood up ahead of the
  first slice doc.
- On MW-2 vs MW-3 order: "I don't have an opinion. We move this project forward one step at a time,
  so I'll say Dealer's Choice on this one." MW chose MW-2 first — storage format is deferred on
  purpose, and the microscope produces the first real arrays to choose a format against.

**Items:**

- [ ] Both workflows log Node 20 deprecation warnings: the runner forces the `@v4`/`@v5` actions
      onto Node 24, and `docs.yml` still pins `node-version: "20"` for `ewc3-docs-tools`. Still
      green.
- [x] MW-2 and MW-3 are both "next" in Current Focus with no order between them. Does serialization
      have to exist before the microscope has anything worth saving? — decided: MW-2 first, [MW-3]
      follows once there are real arrays to store
- [x] No row has a slice doc yet; the `Doc` column points at design documents or is `—` (MW-4, MW-5,
      MW-7). MW-2 is `L` and the first to touch real audio, so it is the likeliest to earn one
      first. — [MW-2] slice doc written: `slices/MW-2_Microscope.md`
