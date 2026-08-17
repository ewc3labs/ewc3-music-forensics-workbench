"""Claims and provenance.

THE CENTRAL IDEA: an analyzer does not produce facts. It produces a *claim*, attributed to whatever
made it, at whatever confidence it can honestly state, pointing back at what it was derived from.

Two pitch trackers that disagree are a normal state of this system, not an error to resolve before
storage. Whichever one you eventually believe, the other one's claim is the evidence that the
question was hard - and that is exactly what you want six months later when the transcription looks
wrong and you are trying to work out where it went astray.

A HUMAN CORRECTION IS THE SAME OBJECT. `source="human"`, confidence 1.0. Not a special case beside
the model, not an override flag on a machine claim - the same kind of thing, so every consumer that
understands claims already understands corrections.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Any

HUMAN = "human"


@dataclass(frozen=True)
class Provenance:
    """Who said it, what version of them said it, and how sure they were."""

    source: str
    source_version: str | None = None
    actor: str | None = None
    confidence: float = 1.0

    def __post_init__(self) -> None:
        if not self.source:
            raise ValueError("provenance requires a source")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError(f"confidence must be in [0, 1], got {self.confidence}")
        # A human claim identifies the human. "Wilson decided this" and "somebody decided this" age
        # very differently once more than one person touches a project.
        if self.source == HUMAN and not self.actor:
            raise ValueError("a human claim requires an actor")

    @property
    def is_human(self) -> bool:
        return self.source == HUMAN


@dataclass(frozen=True)
class Claim:
    """One assertion about the recording, with its provenance and its ancestry.

    `start` and `end` are seconds in the source timebase, and they are the RAW OBSERVED values.
    Quantizing an onset to a beat produces a NEW claim derived from this one; it never edits these
    numbers. Deciding an event lands on beat 3 must not destroy the record that it was measured at
    12.413 s, because the measurement is what you re-examine when the beat grid turns out to be
    wrong.
    """

    kind: str
    payload: dict[str, Any]
    provenance: Provenance
    start: float | None = None
    end: float | None = None
    derived_from: tuple[str, ...] = ()
    id: str = field(default_factory=lambda: uuid.uuid4().hex)

    def __post_init__(self) -> None:
        if not self.kind:
            raise ValueError("a claim requires a kind")
        if self.start is not None and self.end is not None and self.end < self.start:
            raise ValueError(f"claim ends before it starts: {self.start} -> {self.end}")
        if self.id in self.derived_from:
            raise ValueError("a claim cannot be derived from itself")

    @property
    def duration(self) -> float | None:
        if self.start is None or self.end is None:
            return None
        return self.end - self.start

    def derive(self, kind: str, payload: dict[str, Any], provenance: Provenance, **kwargs) -> Claim:
        """Make a new claim that cites this one.

        The point of routing derivation through here is that `derived_from` cannot be forgotten. An
        analyzer that builds its output claims by hand will eventually ship one with an empty
        ancestry, and an unattributed conclusion is the thing this whole model exists to prevent.
        """
        parents = tuple(kwargs.pop("derived_from", ())) + (self.id,)
        return Claim(
            kind=kind, payload=payload, provenance=provenance, derived_from=parents, **kwargs
        )
