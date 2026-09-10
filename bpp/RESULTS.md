# BPP (bin packing) - snark non-IRUP construction

OptFin OR-Lab authored family. Items are edges of a snark graph encoded in a
positional carry-free radix so that a capacity-tight bin corresponds to a
perfect matching and three tight bins to a proper 3-edge-colouring. Snarks have
no proper 3-edge-colouring, so OPT = 4 while z_LP = L1 = 3 (integrality gap 1).

Optimality doctrine: `PROVEN_OPTIMAL` is emitted only where the public
verification test exhaustively proves no packing into `UB-1` bins exists
(LB = UB), independent of any internal solver state. Larger flowers where the
bounded exhaustive search is not run are reported `FEASIBLE` with the L1 bound.

| instance | n | state | LB | UB | gap | proof | checker |
|---|---|---|---|---|---|---|---|
| petersen | 15 | PROVEN_OPTIMAL | 4 | 4 | 0 | `EXHAUSTIVE_NO_3_BIN(nodes=58)` | PASS |
| flower_J3 | 18 | PROVEN_OPTIMAL | 4 | 4 | 0 | `EXHAUSTIVE_NO_3_BIN(nodes=152)` | PASS |
| flower_J5 | 30 | PROVEN_OPTIMAL | 4 | 4 | 0 | `EXHAUSTIVE_NO_3_BIN(nodes=842)` | PASS |
| flower_J7 | 42 | PROVEN_OPTIMAL | 4 | 4 | 0 | `EXHAUSTIVE_NO_3_BIN(nodes=3602)` | PASS |
| flower_J9 | 54 | PROVEN_OPTIMAL | 4 | 4 | 0 | `EXHAUSTIVE_NO_3_BIN(nodes=14642)` | PASS |
| flower_J11 | 66 | PROVEN_OPTIMAL | 4 | 4 | 0 | `EXHAUSTIVE_NO_3_BIN(nodes=58802)` | PASS |
| flower_J13 | 78 | PROVEN_OPTIMAL | 4 | 4 | 0 | `EXHAUSTIVE_NO_3_BIN(nodes=235442)` | PASS |
| flower_J15 | 90 | PROVEN_OPTIMAL | 4 | 4 | 0 | `EXHAUSTIVE_NO_3_BIN(nodes=942002)` | PASS |
| flower_J17 | 102 | FEASIBLE | 3 | 4 | 1 | `SKIPPED_N>90_L1_ONLY` | PASS |
| flower_J19 | 114 | FEASIBLE | 3 | 4 | 1 | `SKIPPED_N>90_L1_ONLY` | PASS |
| flower_J21 | 126 | FEASIBLE | 3 | 4 | 1 | `SKIPPED_N>90_L1_ONLY` | PASS |
