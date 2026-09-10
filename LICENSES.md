# Licenses and attribution

## Our artifacts (CC BY 4.0, attribution OptFin OR-Lab - https://optfin.org)

* `bpp/` snark non-IRUP construction instances, solutions, plots, verification.
* `kp/` deterministic knapsack instances, solutions, plots, verification.
* `roadef/` our EURO/ROADEF 2026 "Keep the Flow!" (T-ASR) SR-path solution
  witnesses, `metadata.json` (our reported bounds/states), SVG plots and
  verification tests. **NOT included: the ROADEF instances or the official
  checker** — those are third-party (see below). Our SR-path witnesses encode
  our own routing decisions in the official submission format and are our work.
* `tools/generate_public_benchmark.py` the deterministic generator.

These are original works authored by OptFin OR-Lab.

## Third-party corpora (linked, NOT redistributed here)

The following corpora are governed by their own terms and are **not** included
as raw data in this repository. Retrieve them from their official sources and
cite them per their licenses:

| corpus | policy | where |
|---|---|---|
| TSPLIB95 | metadata/results only until license review | official TSPLIB homepage |
| QAPLIB | metadata/results only until license review | official QAPLIB homepage |
| SINTEF NEARP | metadata/results only until license review | SINTEF benchmark page |
| ROADEF 2010 | metadata/results only until license review | ROADEF/EURO challenge site |
| ROADEF 2026 "Keep the Flow!" instances (net/tm/scenario) | our SR-path solutions + plots + tests only; instances & official checker NOT redistributed | https://www.roadef.org/challenge/2026/en/ |
| ROADEF 2026 official checker (checker-v1.0.0) | referenced as the objective oracle; binary/source NOT redistributed | ROADEF/EURO 2026 challenge site |
| BPPLIB | CC BY-NC-ND 4.0 - no redistribution here | BPPLIB homepage |

Where OptFin has run these corpora, published results are reported as feasible
upper bounds against published references; optimality is not inferred for them.
