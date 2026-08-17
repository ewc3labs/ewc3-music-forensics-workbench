"""Explicit timebases.

Every timestamp in this system says what it is measured in. A bare float called `t` is how a project
ends up with sample indices compared against seconds and nobody noticing until a barline lands in
the wrong bar.

Seconds are the interchange unit: analyzers disagree about frame sizes and hop lengths, and a claim
has to survive being read by a component that never saw the STFT that produced it.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Timebase:
    """Maps between sample indices, frame indices, and seconds for one representation."""

    sample_rate: int
    hop_length: int = 1

    def __post_init__(self) -> None:
        if self.sample_rate <= 0:
            raise ValueError(f"sample_rate must be positive, got {self.sample_rate}")
        if self.hop_length <= 0:
            raise ValueError(f"hop_length must be positive, got {self.hop_length}")

    def seconds_from_sample(self, sample: int) -> float:
        return sample / self.sample_rate

    def sample_from_seconds(self, seconds: float) -> int:
        # Rounds rather than truncates. Truncation biases every conversion in one direction, and a
        # systematic half-sample lean accumulates into audible drift once onsets are chained through
        # several representations.
        return round(seconds * self.sample_rate)

    def seconds_from_frame(self, frame: int) -> float:
        return (frame * self.hop_length) / self.sample_rate

    def frame_from_seconds(self, seconds: float) -> int:
        return round(seconds * self.sample_rate / self.hop_length)

    @property
    def frame_duration(self) -> float:
        """Seconds per frame - the resolution limit of any claim made in this timebase."""
        return self.hop_length / self.sample_rate
