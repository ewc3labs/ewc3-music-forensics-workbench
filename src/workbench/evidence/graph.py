"""The evidence graph.

A container for claims that can answer the only question that really matters: **why do you believe
that?** Given any claim, walk `derived_from` backwards until you reach the raw observations.

The graph enforces two invariants, both of which exist because the alternative fails silently:

- **No dangling ancestry.** A claim citing a parent that is not present looks perfectly healthy
  until someone tries to trace it, at which point the trail simply stops with no indication that
  anything is missing.
- **No cycles.** Two claims each citing the other is not a provenance chain, it is a loop, and
  anything that walks ancestry will hang or lie.
"""

from __future__ import annotations

from collections.abc import Iterable, Iterator

from .claim import Claim


class EvidenceError(Exception):
    """The graph is not in a state anything downstream should trust."""


class EvidenceGraph:
    def __init__(self, claims: Iterable[Claim] = ()) -> None:
        self._claims: dict[str, Claim] = {}
        for claim in claims:
            self.add(claim)

    def add(self, claim: Claim) -> Claim:
        if claim.id in self._claims:
            raise EvidenceError(f"claim {claim.id} is already in the graph")
        for parent in claim.derived_from:
            if parent not in self._claims:
                # Rejected at insertion rather than at read time. A graph that accepts a broken
                # reference has already lost the context needed to say which analyzer produced it.
                raise EvidenceError(
                    f"claim {claim.id} ({claim.kind}) cites unknown ancestor {parent}"
                )
        self._claims[claim.id] = claim
        return claim

    def __len__(self) -> int:
        return len(self._claims)

    def __contains__(self, claim_id: object) -> bool:
        return claim_id in self._claims

    def __iter__(self) -> Iterator[Claim]:
        return iter(self._claims.values())

    def get(self, claim_id: str) -> Claim:
        try:
            return self._claims[claim_id]
        except KeyError:
            raise EvidenceError(f"no claim {claim_id}") from None

    def of_kind(self, kind: str) -> list[Claim]:
        return [c for c in self._claims.values() if c.kind == kind]

    def ancestors(self, claim_id: str) -> list[Claim]:
        """Every claim this one rests on, nearest first. Breadth-first, each claim once."""
        seen: set[str] = set()
        out: list[Claim] = []
        queue = list(self.get(claim_id).derived_from)

        while queue:
            current = queue.pop(0)
            if current in seen:
                continue
            seen.add(current)
            claim = self.get(current)
            out.append(claim)
            queue.extend(claim.derived_from)

        return out

    def roots(self, claim_id: str) -> list[Claim]:
        """The raw observations underneath a claim - ancestors that cite nothing themselves."""
        return [c for c in self.ancestors(claim_id) if not c.derived_from]

    def explain(self, claim_id: str) -> str:
        """A human-readable derivation, for the moment someone asks why."""
        claim = self.get(claim_id)
        lines = [_describe(claim)]
        lines += [f"  from {_describe(a)}" for a in self.ancestors(claim_id)]
        return "\n".join(lines)

    def disagreements(self, kind: str, tolerance: float = 0.05) -> list[tuple[Claim, Claim]]:
        """Pairs of same-kind claims about the same moment from different sources.

        Not an error report. Two analyzers disagreeing is the system working, and surfacing it is
        how a human decides what to pin - so this returns the argument rather than resolving it.
        """
        candidates = [c for c in self.of_kind(kind) if c.start is not None]
        pairs: list[tuple[Claim, Claim]] = []

        for i, a in enumerate(candidates):
            for b in candidates[i + 1 :]:
                if a.provenance.source == b.provenance.source:
                    continue
                if abs(a.start - b.start) <= tolerance and a.payload != b.payload:
                    pairs.append((a, b))

        return pairs


def _describe(claim: Claim) -> str:
    where = f"@{claim.start:.3f}s" if claim.start is not None else "@-"
    who = claim.provenance.actor or claim.provenance.source
    return f"{claim.kind} {where} {claim.payload} ({who}, {claim.provenance.confidence:.2f})"
