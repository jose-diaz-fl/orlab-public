# ROADEF 2026 - Keep the Flow! (T-ASR) - segment routing, MLU minimization

OptFin OR-Lab candidate (team S84). **Instances are third-party (ROADEF/EURO 2026
organizers) and are NOT redistributed here** - see `roadef/README.md` for the
official source + attribution. Only our SR-path solution witnesses, the SVG plots
and the verification tests are OptFin-authored (CC BY 4.0).

Objective: minimise the lexicographic maximum link utilisation (MLU). The OFFICIAL
checker (checker-v1.0.0, 6 dp) is the sole feasibility/objective oracle. An instance
is `PROVEN_OPTIMAL` only where an independently re-derived directed-capacity-cut
lower bound equals the checker-validated UB to 6 decimals; otherwise `FEASIBLE`
with its reported gap. Nothing is pre-declared optimal.

| instance | dataset | state | LB | UB (MLU) | gap % | checker |
|---|---|---|---|---|---|---|
| setA-01 | A | FEASIBLE | n/a | 0.929383 | n/a | OFFICIAL (external) |
| setA-02 | A | FEASIBLE | n/a | 0.903074 | n/a | OFFICIAL (external) |
| setA-03 | A | FEASIBLE | n/a | 0.943543 | n/a | OFFICIAL (external) |
| setA-04 | A | FEASIBLE | n/a | 0.582809 | n/a | OFFICIAL (external) |
| setA-05 | A | FEASIBLE | n/a | 0.204985 | n/a | OFFICIAL (external) |
| setA-06 | A | FEASIBLE | n/a | 0.239436 | n/a | OFFICIAL (external) |
| setA-07 | A | FEASIBLE | n/a | 0.907989 | n/a | OFFICIAL (external) |
| setA-08 | A | FEASIBLE | n/a | 0.39131 | n/a | OFFICIAL (external) |
| setA-09 | A | FEASIBLE | n/a | 0.84965 | n/a | OFFICIAL (external) |
| setA-10 | A | FEASIBLE | n/a | 0.097826 | n/a | OFFICIAL (external) |
| setA-11 | A | FEASIBLE | n/a | 0.785788 | n/a | OFFICIAL (external) |
| setA-12 | A | FEASIBLE | n/a | 0.879872 | n/a | OFFICIAL (external) |
| setA-13 | A | FEASIBLE | n/a | 0.136752 | n/a | OFFICIAL (external) |
| setA-14 | A | FEASIBLE | n/a | 0.517621 | n/a | OFFICIAL (external) |
| setA-15 | A | FEASIBLE | n/a | 0.898695 | n/a | OFFICIAL (external) |
| setA-16 | A | FEASIBLE | n/a | 0.57377 | n/a | OFFICIAL (external) |
| setA-17 | A | FEASIBLE | n/a | 1.000075 | n/a | OFFICIAL (external) |
| setA-18 | A | FEASIBLE | n/a | 0.999998 | n/a | OFFICIAL (external) |
| setA-19 | A | FEASIBLE | n/a | 0.166276 | n/a | OFFICIAL (external) |
| setA-20 | A | FEASIBLE | n/a | 0.991312 | n/a | OFFICIAL (external) |
| setB-01 | B | FEASIBLE | 0.141921 | 0.536053 | 277.7122 | OFFICIAL (external) |
| setB-02 | B | PROVEN_OPTIMAL | 1.0 | 1.0 | 0.0 | OFFICIAL (external) |
| setB-03 | B | PROVEN_OPTIMAL | 1.0 | 1.0 | 0.0 | OFFICIAL (external) |
| setB-04 | B | FEASIBLE | 0.6694 | 0.778099 | 16.2383 | OFFICIAL (external) |
| setB-05 | B | FEASIBLE | 0.091323 | 0.632314 | 592.3929 | OFFICIAL (external) |
| setB-06 | B | PROVEN_OPTIMAL | 1.0 | 1.0 | 0.0 | OFFICIAL (external) |
| setB-07 | B | FEASIBLE | 0.664909 | 0.68361 | 2.8126 | OFFICIAL (external) |
| setB-08 | B | PROVEN_OPTIMAL | 1.000001 | 1.000001 | 0.0 | OFFICIAL (external) |
| setB-09 | B | PROVEN_OPTIMAL | 1.000001 | 1.000001 | 0.0 | OFFICIAL (external) |
| setB-10 | B | PROVEN_OPTIMAL | 0.992426 | 0.992426 | 0.0 | OFFICIAL (external) |
| setB-11 | B | FEASIBLE | 0.363609 | 0.772908 | 112.5657 | OFFICIAL (external) |
| setB-12 | B | FEASIBLE | 0.603087 | 0.780491 | 29.416 | OFFICIAL (external) |

## Summary

- instances: **32** (Set A: 20, Set B: 12)
- **PROVEN_OPTIMAL: 6** (all in Set B: setB-02, setB-03, setB-06, setB-08, setB-09, setB-10)
- **FEASIBLE (open gap or no LB asserted): 26**
- **OPEN (no feasible witness): 0**
- checker-valid: **all** witnesses validated by the official checker.

