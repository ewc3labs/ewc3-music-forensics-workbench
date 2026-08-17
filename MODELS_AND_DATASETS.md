# Models and datasets

Model weights and training data are **separate license objects from the code that runs them**, and
they are frequently the more restrictive half. A permissive implementation carrying research-only
weights is not a permissive system.

**Nothing here yet.** No models are used, shipped, or downloaded. Milestone 1 is deliberately
DSP-only and requires none.

| Model | Implementation | Impl license | Weights | Weight license | Training data | Data license | Redistribution | Commercial | Research-only | We ship it? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| *(none)* | | | | | | | | | | |

## When you add a model

Fill the row **before** the model is wired in, because the answer sometimes disqualifies it.

Candidates already named in the charter — Basic Pitch, CREPE, Demucs, Essentia, aubio — vary widely
on exactly these axes, and several have implementation and weight licenses that differ from one
another.

## Ship it or fetch it

The architecture keeps licensing coupling low so this stays a real choice. A model we cannot
redistribute can still be **supported**: the user fetches the weights themselves, and we ship the
adapter. That is a licensing decision with an architectural consequence, which is why it is recorded
here rather than in a code comment.

## The rule

**Unknown licensing status is not "probably okay."** It is unknown, and unknown assets are not
redistributed until resolved.
