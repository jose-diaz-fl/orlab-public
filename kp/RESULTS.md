# KP (0/1 knapsack) - deterministic development set

OptFin OR-Lab deterministic generator. Profits are exact rationals
(numerator/denominator); the optimum is proven by a full 0/1
dynamic-programming table over the integer capacity, so every row is
`PROVEN_OPTIMAL` and re-verifiable by recomputation.

| instance | n | capacity | state | optimum (num/den) | gap | proof | checker |
|---|---|---|---|---|---|---|---|
| kp_n1000_c50_v1 | 1000 | 50 | PROVEN_OPTIMAL | 3192 | 0 | `EXACT_0_1_DP_FULL_TABLE` | PASS |
