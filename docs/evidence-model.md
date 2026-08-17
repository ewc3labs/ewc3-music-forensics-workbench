# The evidence model

Read this before writing an analyzer. Everything downstream inherits its shape from here, which is
why it exists before any code that loads audio.

## Analyzers produce claims, not facts

A claim is one assertion about the recording, carrying who made it, how sure they were, and what it
was derived from.

```python
Claim(
    kind="pitch",
    payload={"note": "F#4"},
    provenance=Provenance(source="basic_pitch", source_version="0.3.2", confidence=0.86),
    start=12.413,
    end=12.677,
)
```

**Two analyzers disagreeing is a normal state of the system**, not an error to resolve before
storage. `EvidenceGraph.disagreements()` surfaces the argument; it does not pick a winner, because
picking one silently is how the losing evidence stops existing — and the losing evidence is exactly
what you want six months later when the transcription looks wrong.

## A human correction is the same object

```python
Provenance(source="human", actor="wilson", confidence=1.0)
```

Not a flag on a machine claim, not a separate override table. The same kind of thing, so every
consumer that already understands claims understands corrections too.

A human claim **must name the human**. "Wilson decided this" and "somebody decided this" age very
differently once more than one person touches a project, and the constructor refuses the second one.

## Quantization derives, it never edits

This is the rule the whole model exists for.

```python
raw = Claim(kind="onset", ..., start=12.413)
beat = raw.derive("beat", {"beat": 3}, wilson, start=12.5)

raw.start   # still 12.413
```

Deciding an onset lands on beat 3 must not destroy the record that it was **measured** at 12.413 s.
The measurement is what you re-examine when the beat grid turns out to be wrong — and with Page's
prologue riff, the beat grid being wrong is the entire question.

Derivation goes through `.derive()` so `derived_from` cannot be forgotten. An analyzer assembling
output claims by hand will eventually ship one with empty ancestry, and an unattributed conclusion
is precisely what this model exists to prevent.

## The graph enforces two invariants

| | why it is refused |
| --- | --- |
| **dangling ancestry** | a claim citing an absent parent looks healthy until someone traces it, and then the trail just stops with no sign anything is missing |
| **self-derivation** | a loop is not a provenance chain, and anything walking it will hang or lie |

Dangling ancestry is rejected **at insertion**, while it is still possible to say which analyzer
produced it. Validating at read time means discovering the problem with none of the context needed
to fix it.

## Why do you believe that?

```python
graph.explain(note.id)
```

```text
note @12.500s {'pitch': 'F#4'} (basic_pitch, 0.86)
  from beat @12.500s {'beat': 3} (wilson, 1.00)
  from onset @12.413s {'strength': 0.7} (basic_pitch, 0.86)
```

Any conclusion traces backwards to raw observation. An answer you cannot interrogate is not much
better than a guess.

## Timebases are explicit

A bare float called `t` is how sample indices end up compared against seconds and nobody notices
until a barline lands in the wrong bar. `Timebase` converts between samples, frames, and seconds,
and knows its own `frame_duration` — the resolution limit of any claim made in it.

**Seconds are the interchange unit.** Analyzers disagree about frame sizes and hop lengths, and a
claim has to survive being read by something that never saw the STFT that produced it.

Conversions **round rather than truncate**. Truncation biases every conversion the same direction,
and a systematic half-sample lean accumulates into real drift once onsets are chained through
several representations.

## What is deliberately not here yet

No storage format, no serialization, no spectral arrays. The charter is explicit that huge feature
arrays do not belong inside ordinary JSON, and picking between MessagePack, Zarr, and HDF5 before
anything produces an array would be guessing. The in-memory model comes first because it is the part
every later decision has to satisfy.
