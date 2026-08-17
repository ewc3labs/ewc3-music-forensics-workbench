# Overview

Documentation for the Music Forensics Workbench.

The [README](../README.md) says what this is and why it exists. These pages are the detail.

## Design

- [Architecture](architecture.md): the layers, and what is deliberately still undecided.
- [Evidence model](evidence-model.md): claims, provenance, timebases. **Read this first if you are
  writing an analyzer** — everything downstream inherits its shape from it.
- [Project charter](PROJECT_CHARTER.md): the full architectural source of truth, including the
  analysis modules the skeleton has not built yet.

## Policy

- [Licensing](licensing.md): why GPL-3.0-only provisionally, and why code, weights, and datasets are
  tracked as three separate objects.

## Project

- [Roadmap][roadmap]: milestones, and the `MW` prefix registration.

## The idea in one paragraph

The goal is not "audio in, sheet music out." It is **audio in, evidence, competing hypotheses,
musical interpretation** — with every conclusion traceable back to what produced it. Analyzers emit
claims rather than facts, two analyzers disagreeing is a normal state rather than an error, a human
correction is the same kind of object as a machine claim, and quantizing an onset to a beat never
destroys the record of where it was actually measured. That last one is the whole point: when the
beat grid turns out to be wrong, the measurement is what you go back to.

[roadmap]: project/MusicForensics_Workbench_Roadmap.md
