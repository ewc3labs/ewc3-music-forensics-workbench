# Licensing

**Status: GPL-3.0-only, provisional.** Not yet ratified — and this project is the reason the EWC3
Labs licensing review exists at all.

## How we got here

EWC3 Labs had a simple house rule: MIT everywhere. Designing this project surfaced that the rule was
carrying an assumption MIT does not support — the belief that it prevents others from taking the
work and closing it. It does not. MIT deliberately permits commercial use, modification,
sublicensing, sale, and redistribution under different terms **without source**. That is not a
defect in MIT; it is the point of MIT.

Whether that matches what EWC3 Labs wants downstream users to be allowed to do is a real question,
and a music-analysis workbench that will accumulate third-party models is the worst project to
answer it casually. Hence GPL-3.0-only, provisionally, pending the [organization policy
review][policy].

## Three separate license objects

The trap this project intends to avoid:

| | |
| --- | --- |
| **code** | the implementation, ours and upstream's |
| **model weights** | frequently licensed differently from the code that runs them |
| **training datasets** | frequently more restrictive still, and often unstated |

A permissively-licensed implementation carrying research-only weights is not a permissively-licensed
system. Tracking these separately is the only way to know what can actually be redistributed.

## Provenance files

Maintained **from the first dependency onward**, not retrofitted:

- **[THIRD_PARTY.md](../THIRD_PARTY.md)** — component, upstream URL, version, license, integration
  mode, our modifications, attribution requirements, compatibility decision.
- **[MODELS_AND_DATASETS.md](../MODELS_AND_DATASETS.md)** — model, implementation license, weight
  license, training data and its license, redistribution rights, commercial/research restrictions,
  and whether we ship the asset or fetch it at install time.
- **[NOTICE.md](../NOTICE.md)** — attributions that upstream licenses require us to carry.

Retrofitting these is how projects discover, at release time, that something in the tree cannot be
shipped.

## The rule that matters

> **Unknown licensing status is not "probably okay." It is unknown, and unknown assets are not
> redistributed until resolved.**

An analyzer whose weights have unclear provenance can still be *supported* — the architecture keeps
licensing coupling low precisely so that a model can be something the user fetches themselves rather
than something we redistribute.

## Not silently relicensing history

Existing EWC3 Labs work stays under the license it was published with. A future organization-level
decision applies going forward; it does not quietly rewrite what people already received.

[policy]: https://github.com/ewc3labs/ewc3labs-hq
