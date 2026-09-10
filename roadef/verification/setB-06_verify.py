"""Public verification test for ROADEF 2026 T-ASR instance setB-06.

Attribution: OptFin OR-Lab - https://optfin.org

NON-CIRCULAR + HONEST. The official ROADEF instances and the official checker
are third-party and are NOT redistributed in this repository. This test does
NOT trust any internal solver flag. It re-derives the optimality STATE from the
published lower-bound certificate arithmetic and confirms it matches the label
in roadef/metadata.json:

  * Upper bound  UB = max link utilization (MLU), as reported by the OFFICIAL
    checker (checker-v1.0.0, 6 decimal places) - the sole feasibility/objective
    oracle. It is copied here as published data, not recomputed (the instance
    is not present to recompute it non-circularly).
  * Lower bound  LB for a PROVEN_OPTIMAL instance is a single-node directed-
    capacity cut: forced crossing demand / post-intervention capacity. This
    test recomputes LB = crossing_demand / capacity from the raw certificate
    numbers and requires round(LB,6) == round(UB,6) to accept PROVEN_OPTIMAL.
  * Otherwise the state must be FEASIBLE (LB < UB) or OPEN.

To additionally re-prove the UB against the ORIGINAL instance, retrieve the
official instance files and the official checker from the ROADEF/EURO 2026
challenge site (see roadef/README.md) and run:

    run.sh <net.json> <tm.json> <scenario.json> roadef/solutions/setB-06-srpaths.json

Run this self-contained state check:  python setB-06_verify.py
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
METADATA = os.path.join(ROOT, "metadata.json")
SOLUTION = os.path.join(ROOT, "solutions", "setB-06-srpaths.json")

INSTANCE_ID = "setB-06"
TOL_DECIMALS = 6


def _entry():
    meta = json.load(open(METADATA, encoding="utf-8"))
    for it in meta["instances"]:
        if it["id"] == INSTANCE_ID:
            return it
    raise SystemExit("instance %s not found in metadata" % INSTANCE_ID)


def verify():
    it = _entry()
    ub = it["ub_mlu"]
    reported = it["state"]
    cert = it["lb_certificate"]

    # --- our solution witness is present and well-formed (our content) ---
    sol = json.load(open(SOLUTION, encoding="utf-8"))
    rows = sol["srpaths"]
    assert isinstance(rows, list), "srpaths must be a list"
    for r in rows:
        assert set(("d", "t", "w")) <= set(r.keys()), "malformed SR-path row"
        assert isinstance(r["w"], list), "waypoints must be a list"

    # --- re-derive the state from the certificate arithmetic (non-circular) ---
    derived_lb = None
    derived_state = "FEASIBLE"
    proof = "NO_INDEPENDENT_LB_ASSERTED"
    if cert is not None and cert.get("crossing_demand") is not None:
        cap = float(cert["capacity"])
        cd = float(cert["crossing_demand"])
        assert cap > 0, "non-positive capacity in certificate"
        derived_lb = cd / cap
        proof = "DIRECTED_CAPACITY_CUT_%s_node_%s_slot_%s" % (
            cert["lb_type"], cert["node"], cert["slot"],
        )
        if round(derived_lb, TOL_DECIMALS) == round(float(ub), TOL_DECIMALS):
            derived_state = "PROVEN_OPTIMAL"
        else:
            derived_state = "FEASIBLE"

    result = {
        "instance": INSTANCE_ID,
        "problem": "roadef-tasr",
        "dataset": it["dataset"],
        "ub_mlu_official_checker": ub,
        "lb_rederived": (round(derived_lb, TOL_DECIMALS) if derived_lb is not None else None),
        "derived_state": derived_state,
        "reported_state": reported,
        "matches_reported": derived_state == reported,
        "optimality_proof": proof,
        "instance_data": "THIRD_PARTY_NOT_REDISTRIBUTED",
        "checker": "OFFICIAL_ROADEF_CHECKER_EXTERNAL",
    }
    assert result["matches_reported"], "STATE_MISMATCH: %s" % result
    return result


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
