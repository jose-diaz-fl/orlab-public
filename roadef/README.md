# ROADEF / EURO 2026 Challenge — "Keep the Flow!" (T-ASR)

Attribution: **OptFin OR-Lab — https://optfin.org** (candidate team S84).

This directory publishes OptFin OR-Lab's segment-routing (SR-path) solution
witnesses for the EURO/ROADEF 2026 challenge *Keep the Flow!* (Traffic-Aware
Segment Routing, T-ASR), together with a vector SVG per instance and a
self-contained verification test.

## What is (and is NOT) in this directory

The ROADEF challenge **instances** (the `net.json` / `tm.json` / `scenario.json`
topology, traffic-matrix and interventions files) are authored by the challenge
organizers and are **their intellectual property**. They are therefore **NOT
redistributed here**. Retrieve them from the official challenge site and cite
them per the organizers' terms.

* Official challenge homepage: https://www.roadef.org/challenge/2026/en/
* EURO/ROADEF 2026 "Keep the Flow!" resources and rules: linked from the page
  above (topology, traffic matrices, interventions scenarios, and the official
  solution checker `checker-v1.0.0`).

What **is** published here — all OptFin OR-Lab-authored, released under CC BY 4.0
with attribution to optfin.org:

```
roadef/
  metadata.json              per-instance UB (official-checker MLU), LB,
                             gap, honest state, and LB certificate (our data)
  solutions/<id>-srpaths.json  OUR SR-path witness in the official submission
                             format (our routing decisions, not instance data)
  plots/<id>.svg             vector plot: reported MLU + our solution structure
  verification/<id>_verify.py  self-contained, non-circular state re-derivation
  RESULTS.md                 per-instance table (state, LB, UB, gap, checker)
```

## Objective and oracle

The objective is to minimise the lexicographic **maximum link utilisation
(MLU)** by choosing, per demand and time slot, a segment-routing path subject to
the per-route segment cap and the scenario's per-slot topology. A demand with no
explicit SR-path follows the implicit-default (ECMP) routing; an empty SR-path
set (`{"srpaths": []}`) is thus a valid witness the official checker accepts on
every instance.

The **official ROADEF checker** (`checker-v1.0.0`, `--max-decimal-places 6`) is
the sole feasibility and objective oracle. It is third-party and is **not**
redistributed here.

## Optimality doctrine (honest, non-circular)

* `PROVEN_OPTIMAL` is emitted **only** where an independently re-derived
  directed-capacity-cut lower bound equals the checker-validated upper bound to
  six decimals. The cut is a single node whose forced ingress/egress (crossing)
  demand already saturates an incident link to the reported MLU, so no routing
  can beat it: `LB = crossing_demand / post_intervention_capacity`.
* `FEASIBLE` is used for a checker-valid witness whose LB does not close the gap
  (or for which no independent LB is asserted).
* `OPEN` would be used where no feasible witness exists (none here).

The verification test does **not** trust any solver flag: it recomputes
`LB = crossing_demand / capacity` from the raw certificate numbers and requires
`round(LB, 6) == round(UB, 6)` before it will confirm `PROVEN_OPTIMAL`; a
mislabelled instance makes the test fail.

## Current state (team S84)

* Instances: **32** — Set A: 20, Set B: 12.
* **PROVEN_OPTIMAL: 6** — all in Set B: setB-02, setB-03, setB-06, setB-08,
  setB-09, setB-10 (independent LB == checker-validated UB).
* **FEASIBLE: 26** — 20 Set A (checker-valid, no LB asserted) + 6 Set B (open gap).
* **OPEN: 0.** All 32 witnesses are validated by the official checker.

## Reproduce

Self-contained honest-state re-derivation (no instance data needed):

```
python roadef/verification/setB-02_verify.py
python roadef/verification/setA-01_verify.py
```

To additionally re-prove the upper bound against the ORIGINAL instance, download
the official instance files and the official checker from the challenge site
above and run:

```
run.sh <net.json> <tm.json> <scenario.json> roadef/solutions/<id>-srpaths.json
```

## License

Our SR-path solutions, SVG plots and verification tests are © OptFin OR-Lab and
released under CC BY 4.0 with attribution to https://optfin.org. The ROADEF
challenge instances and the official checker referenced above remain the
property of the challenge organizers and are governed by their own terms.
