"""Public verification test for KP instance kp_n1000_c50_v1.

Self-contained and non-circular: recomputes the exact 0/1 knapsack DP and
confirms the reported optimal value == the DP table optimum, and that the
reported item set is feasible and realises that value. No internal imports.

Run:  python kp_n1000_c50_v1_verify.py
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
INSTANCE = os.path.join(ROOT, "instances", "kp_n1000_c50_v1.json")
SOLUTION = os.path.join(ROOT, "solutions", "kp_n1000_c50_v1.json")


def _kp_exact_dp(weights, profit_num, capacity):
    n = len(weights)
    cur = [0] * (capacity + 1)
    for i in range(n):
        wi, pi = weights[i], profit_num[i]
        for c in range(capacity, wi - 1, -1):
            cand = cur[c - wi] + pi
            if cand > cur[c]:
                cur[c] = cand
    return cur[capacity]


def verify():
    inst = json.load(open(INSTANCE, encoding="utf-8"))
    sol = json.load(open(SOLUTION, encoding="utf-8"))
    w = inst["weights"]
    C = inst["capacity"]
    denom = inst["profit_denominator"]
    pnum = inst["profit_numerators"]

    chosen = sol["items"]
    used_w = sum(w[i] for i in chosen)
    used_p = sum(pnum[i] for i in chosen)
    assert used_w <= C, "OVER_CAPACITY"
    assert used_p == sol["optimal_profit_numerator"], "PROFIT_RECONSTRUCTION_MISMATCH"

    dp_opt = _kp_exact_dp(w, pnum, C)
    assert dp_opt == sol["optimal_profit_numerator"], (
        "DP optimum %d != reported %d" % (dp_opt, sol["optimal_profit_numerator"])
    )
    state = "PROVEN_OPTIMAL"
    result = {
        "instance": "kp_n1000_c50_v1",
        "problem": "kp",
        "optimal_profit_numerator": dp_opt,
        "optimal_profit_denominator": denom,
        "used_weight": used_w,
        "capacity": C,
        "state": state,
        "matches_reported": state == sol["state"],
        "checker": "PASS",
    }
    assert result["matches_reported"], "STATE_MISMATCH"
    return result


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
