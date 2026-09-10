# OptFin OR-Lab - public optimization benchmark

Attribution: **OptFin OR-Lab - https://optfin.org**

This repository publishes a small, honest benchmark of optimization instances that
OptFin OR-Lab has authored, each paired with a solution, a vector SVG plot of the
instance-with-solution, and a self-contained verification test that re-proves the
reported optimality state.

## Optimality doctrine (honest, non-circular)

* `PROVEN_OPTIMAL` is emitted **only** where a self-contained public test closes
  `LB == UB` from the instance itself - never from an internal solver flag.
  * BPP-snark: an exhaustive symmetry-reduced search proves that no packing into
    `UB-1` bins exists (lower bound), and a first-fit-decreasing witness gives the
    upper bound.
  * KP: a full 0/1 dynamic-programming table gives the exact optimum, recomputed by
    the verifier.
* `FEASIBLE` / `OPEN` are used everywhere the bound is not closed; nothing is
  pre-declared optimal.
* For third-party corpora (see `roadef/`) the same doctrine applies: an
  independently re-derived lower bound must equal the official-checker upper
  bound before we label anything `PROVEN_OPTIMAL`.

## Layout

```
<problem>/
  instances/<id>.json        the instance (OptFin-authored problems only)
  solutions/<id>.json        the solution + its structure, LB/UB, proof
  plots/<id>.svg             vector plot: instance + solution
  verification/<id>_verify.py  re-verifies feasibility + objective + optimality
  RESULTS.md                 per-instance table (state, LB, UB, gap, checker)
tools/generate_public_benchmark.py   the deterministic generator (regenerates all)
```

For `roadef/`, whose instances are third-party and are NOT redistributed, there
is no `instances/` directory; we publish only our own SR-path solution witnesses,
plots and verification tests plus a `metadata.json` of our reported bounds.

## Problems covered

* **bpp/** - bin packing, snark non-IRUP construction (integrality gap 1).
* **kp/** - 0/1 knapsack, deterministic development set (exact DP optima).
* **roadef/** - EURO/ROADEF 2026 "Keep the Flow!" (T-ASR) segment-routing MLU
  minimization. OptFin-authored SR-path solution witnesses, plots and honest
  optimality verification. **The ROADEF instances themselves are third-party and
  are NOT redistributed here** - see `roadef/README.md` for the official source
  and attribution. 32 instances: 6 PROVEN_OPTIMAL (Set B), 26 FEASIBLE, 0 OPEN.

## Third-party corpora (linked, not copied)

TSPLIB95, QAPLIB, SINTEF-NEARP, ROADEF 2010/2026 and BPPLIB instances are governed
by their own licenses and are **not** republished here as raw data. For ROADEF 2026
we publish only our own SR-path solutions, plots and verification tests (CC BY 4.0);
the instance topology / traffic / scenario files and the official checker stay with
the challenge organizers (retrieve them from https://www.roadef.org/challenge/2026/en/).
Where OptFin has run other corpora, results are reported as feasible upper bounds
against published references; optimality is not inferred for them. Retrieve the
originals from their official homepages and cite them per their terms.

## Reproduce

```
python tools/generate_public_benchmark.py --repo .
# then, per instance:
python bpp/verification/petersen_verify.py
python kp/verification/kp_n1000_c50_v1_verify.py
python roadef/verification/setB-02_verify.py
```

## License

Instances, solutions, SVG plots and verification tests in this repository are
authored by OptFin OR-Lab and released for research use with attribution to
optfin.org. Third-party benchmark data referenced above remains under its own
license.
