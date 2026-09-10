"""Public verification test for BPP-snark instance petersen.

Self-contained and non-circular: re-reads the instance + solution and proves
LB == UB from scratch. No OptFin-internal imports.

Run:  python petersen_verify.py
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
INSTANCE = os.path.join(ROOT, "instances", "petersen.json")
SOLUTION = os.path.join(ROOT, "solutions", "petersen.json")

NODE_CAP = 2000000


def _can_pack_in_k(weights, capacity, k, node_cap):
    order = sorted(range(len(weights)), key=lambda i: -weights[i])
    ws = [weights[i] for i in order]
    n = len(ws)
    bins = [0] * k
    nodes = [0]

    def rec(i):
        nodes[0] += 1
        if nodes[0] > node_cap:
            return None
        if i == n:
            return True
        seen = set()
        indeterminate = False
        for b in range(k):
            load = bins[b]
            if load in seen:
                continue
            seen.add(load)
            if load + ws[i] <= capacity:
                bins[b] += ws[i]
                r = rec(i + 1)
                bins[b] -= ws[i]
                if r is True:
                    return True
                if r is None:
                    indeterminate = True
        return None if indeterminate else False

    return rec(0)


def verify():
    inst = json.load(open(INSTANCE, encoding="utf-8"))
    sol = json.load(open(SOLUTION, encoding="utf-8"))
    w, C = inst["weights"], inst["capacity"]
    assign = sol["assignment"]
    assert len(assign) == len(w), "assignment length mismatch"

    # --- UB: solution feasibility ---
    used = max(assign) + 1
    loads = [0] * used
    for i, b in enumerate(assign):
        loads[b] += w[i]
    assert all(load <= C for load in loads), "OVER_CAPACITY"
    assert used == sol["num_bins"], "num_bins mismatch"
    ub = used

    # --- LB: L1 material bound ---
    import math as _m
    l1 = _m.ceil(sum(w) / C)

    # --- LB: exhaustive no-(ub-1)-bin proof (non-circular) ---
    lower_target = ub - 1
    verdict = _can_pack_in_k(w, C, lower_target, NODE_CAP)
    if verdict is False:
        lb = ub  # cannot pack in ub-1 => LB == UB
        proof = "EXHAUSTIVE_NO_%d_BIN" % lower_target
        state = "PROVEN_OPTIMAL"
    elif verdict is True:
        lb = lower_target
        proof = "PACKED_IN_%d_BIN" % lower_target
        state = "FEASIBLE"
    else:
        # Bounded exhaustive search did not close the bound within NODE_CAP.
        # Stay honest and non-circular: use only the material L1 lower bound
        # (do NOT trust the construction theorem here). Report FEASIBLE.
        lb = l1
        proof = "BOUNDED_SEARCH_INDETERMINATE_FELL_BACK_TO_L1"
        state = "PROVEN_OPTIMAL" if lb == ub else "FEASIBLE"

    result = {
        "instance": "petersen",
        "problem": "bpp",
        "lb": lb, "ub": ub, "l1": l1,
        "state": state, "proof": proof,
        "reported_state": sol["state"],
        "matches_reported": state == sol["state"],
        "checker": "PASS",
    }
    assert result["matches_reported"], "STATE_MISMATCH: %s" % result
    return result


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
