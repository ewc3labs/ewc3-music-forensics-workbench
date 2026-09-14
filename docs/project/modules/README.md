# Music Forensics Workbench — Modules

**One subsystem per file, spanning several slices.** Use a module doc only when several roadmap
slices clearly belong together and reading them as separate one-page slice docs loses the thread
between them.

## Naming

```text
<Subsystem>.md      e.g.  Evidence_Storage.md,  Pitch_Tracking.md
```

Same rule as everywhere else: the filename should say what it is. The roadmap's `Doc` column pins
these names, so they are how the doc gets found.

## Slices vs modules

| | `slices/` | `modules/` |
| --- | --- | --- |
| Holds | **one** slice or fix | a subsystem spanning **several** slices |
| Size | about a page | longer — its own thin index, sequence, and shared gotchas |
| Lifespan | closes when the slice ships | lives as long as the subsystem |

**Default to `slices/`.** Promote to a module only when the connection between slices is the thing
worth writing down. Template: `ewc3labs-hq/templates/project/template_project_module.md`.

## Rules

- IDs are still minted against the **main roadmap's** ID Prefixes table. A module never runs its own
  ID series — one registry, always.
- The module's own slice table obeys the same **thin** rule: no paragraphs in cells, filenames in
  `Doc`.
- Architecture belongs in `docs/`, not here. A module doc is a *plan*, not a design.
