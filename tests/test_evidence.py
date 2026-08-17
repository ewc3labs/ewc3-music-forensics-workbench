"""Tests for the evidence model.

The charter's instruction is to build automated tests around timing math and evidence
transformations, because those are the two places where a mistake is silent: a wrong number still
renders, and a broken provenance chain still looks like a provenance chain.
"""

from __future__ import annotations

import pytest

from workbench.core import Timebase
from workbench.evidence import HUMAN, Claim, EvidenceError, EvidenceGraph, Provenance

MACHINE = Provenance(source="basic_pitch", source_version="0.3.2", confidence=0.86)
WILSON = Provenance(source=HUMAN, actor="wilson", confidence=1.0)


def onset(at: float, provenance: Provenance = MACHINE) -> Claim:
    return Claim(kind="onset", payload={"strength": 0.7}, provenance=provenance, start=at, end=at)


# --- timebase ---------------------------------------------------------------


def test_seconds_and_samples_round_trip():
    tb = Timebase(sample_rate=44100)
    assert tb.sample_from_seconds(tb.seconds_from_sample(12345)) == 12345


def test_frames_respect_hop_length():
    tb = Timebase(sample_rate=44100, hop_length=512)
    assert tb.seconds_from_frame(100) == pytest.approx(100 * 512 / 44100)
    assert tb.frame_from_seconds(tb.seconds_from_frame(100)) == 100


def test_frame_duration_is_the_resolution_limit():
    assert Timebase(44100, 512).frame_duration == pytest.approx(0.01161, abs=1e-5)


def test_conversion_rounds_rather_than_truncating():
    # Truncation biases every conversion the same direction, and the lean accumulates once onsets
    # are chained through several representations.
    tb = Timebase(sample_rate=1000)
    assert tb.sample_from_seconds(0.0019) == 2


@pytest.mark.parametrize("bad", [{"sample_rate": 0}, {"sample_rate": -1}, {"hop_length": 0}])
def test_a_nonsense_timebase_is_refused(bad):
    kwargs = {"sample_rate": 44100} | bad
    with pytest.raises(ValueError):
        Timebase(**kwargs)


# --- provenance -------------------------------------------------------------


def test_confidence_outside_zero_to_one_is_refused():
    with pytest.raises(ValueError):
        Provenance(source="x", confidence=1.5)


def test_a_human_claim_must_name_the_human():
    # "Wilson decided this" and "somebody decided this" age very differently.
    with pytest.raises(ValueError):
        Provenance(source=HUMAN)


def test_a_human_correction_is_an_ordinary_claim():
    correction = Claim(
        kind="downbeat", payload={"timestamp": 12.53}, provenance=WILSON, start=12.53
    )
    assert correction.provenance.is_human
    assert isinstance(correction, Claim)


# --- claims -----------------------------------------------------------------


def test_a_claim_that_ends_before_it_starts_is_refused():
    with pytest.raises(ValueError):
        Claim(kind="note", payload={}, provenance=MACHINE, start=2.0, end=1.0)


def test_derive_records_ancestry_without_being_asked():
    raw = onset(12.413)
    quantized = raw.derive("beat", {"beat": 3}, WILSON, start=12.5, end=12.5)
    assert raw.id in quantized.derived_from


def test_quantizing_does_not_touch_the_raw_observation():
    """The rule the whole model exists for.

    Deciding an onset lands on beat 3 must not destroy the record that it was measured at 12.413 s -
    the measurement is what you re-examine when the beat grid turns out to be wrong.
    """
    raw = onset(12.413)
    raw.derive("beat", {"beat": 3}, WILSON, start=12.5, end=12.5)
    assert raw.start == 12.413


def test_a_claim_cannot_be_derived_from_itself():
    with pytest.raises(ValueError):
        Claim(kind="note", payload={}, provenance=MACHINE, derived_from=("self",), id="self")


# --- graph ------------------------------------------------------------------


def test_an_unknown_ancestor_is_refused_at_insertion():
    # Rejected on the way in, while it is still possible to say which analyzer produced it.
    graph = EvidenceGraph()
    orphan = Claim(kind="note", payload={}, provenance=MACHINE, derived_from=("nope",))
    with pytest.raises(EvidenceError, match="unknown ancestor"):
        graph.add(orphan)


def test_the_same_claim_cannot_be_added_twice():
    graph = EvidenceGraph()
    claim = onset(1.0)
    graph.add(claim)
    with pytest.raises(EvidenceError):
        graph.add(claim)


def test_ancestors_walk_the_whole_chain():
    graph = EvidenceGraph()
    raw = graph.add(onset(12.413))
    beat = graph.add(raw.derive("beat", {"beat": 3}, MACHINE, start=12.5))
    measure = graph.add(beat.derive("measure", {"bar": 2}, MACHINE, start=12.5))

    ids = [c.id for c in graph.ancestors(measure.id)]
    assert ids == [beat.id, raw.id]
    assert graph.roots(measure.id) == [raw]


def test_a_diamond_reports_each_ancestor_once():
    graph = EvidenceGraph()
    raw = graph.add(onset(12.413))
    left = graph.add(raw.derive("pitch", {"hz": 370.0}, MACHINE))
    right = graph.add(raw.derive("pitch", {"hz": 369.9}, MACHINE))
    merged = graph.add(
        Claim(
            kind="note",
            payload={"pitch": "F#4"},
            provenance=MACHINE,
            derived_from=(left.id, right.id),
        )
    )
    assert [c.id for c in graph.ancestors(merged.id)].count(raw.id) == 1


def test_explain_reaches_the_raw_observation():
    graph = EvidenceGraph()
    raw = graph.add(onset(12.413))
    beat = graph.add(raw.derive("beat", {"beat": 3}, WILSON, start=12.5))

    text = graph.explain(beat.id)
    assert "wilson" in text
    assert "12.413" in text


def test_analyzers_disagreeing_is_reported_not_resolved():
    """Two trackers that disagree are a normal state of the system.

    The graph surfaces the argument so a human can pin one. It does not pick a winner, because
    picking one silently is how the losing evidence stops existing.
    """
    graph = EvidenceGraph()
    a = graph.add(
        Claim(kind="pitch", payload={"note": "F#4"}, provenance=MACHINE, start=12.41, end=12.68)
    )
    b = graph.add(
        Claim(
            kind="pitch",
            payload={"note": "G4"},
            provenance=Provenance(source="crepe", confidence=0.6),
            start=12.43,
            end=12.70,
        )
    )

    assert graph.disagreements("pitch") == [(a, b)]
    assert len(graph) == 2, "both claims survive being in disagreement"


def test_one_source_disagreeing_with_itself_is_not_a_disagreement():
    # Two claims from the same analyzer are that analyzer's business, not evidence of a conflict.
    graph = EvidenceGraph()
    graph.add(Claim(kind="pitch", payload={"note": "F#4"}, provenance=MACHINE, start=12.41))
    graph.add(Claim(kind="pitch", payload={"note": "G4"}, provenance=MACHINE, start=12.42))
    assert graph.disagreements("pitch") == []
