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

## Layout

```
<problem>/
  instances/<id>.json        the instance (OptFin-authored)
  solutions/<id>.json        the solution + its structure, LB/UB, proof
  plots/<id>.svg             vector plot: instance + solution
  verification/<id>_verify.py  re-verifies feasibility + objective + optimality
  RESULTS.md                 per-instance table (state, LB, UB, gap, checker)
tools/generate_public_benchmark.py   the deterministic generator (regenerates all)
```

## Problems covered

* **bpp/** - bin packing, snark non-IRUP construction (integrality gap 1).
* **kp/** - 0/1 knapsack, deterministic development set (exact DP optima).

## Third-party corpora (linked, not copied)

TSPLIB95, QAPLIB, SINTEF-NEARP, ROADEF 2010/2026 and BPPLIB instances are governed
by their own licenses and are **not** republished here as raw data. Where OptFin has
run these corpora, results are reported as feasible upper bounds against published
references; optimality is not inferred for them. Retrieve the originals from their
official homepages and cite them per their terms.

## Reproduce

```
python tools/generate_public_benchmark.py --out .
# then, per instance:
python bpp/verification/petersen_verify.py
python kp/verification/kp_n1000_c50_v1_verify.py
```

## License

Instances, solutions, SVG plots and verification tests in this repository are
authored by OptFin OR-Lab and released for research use with attribution to
optfin.org. Third-party benchmark data referenced above remains under its own
license.
