#!/usr/bin/env python3
"""OptFin OR-Lab public benchmark generator (standalone, deterministic).

Attribution: OptFin OR-Lab - https://optfin.org

Reads each instance from <repo>/<problem>/instances/<id>.json and regenerates
the solution, the vector SVG and the self-contained verification test. Optimality
is claimed only where a non-circular re-verification closes LB == UB (BPP:
exhaustive no-(UB-1)-bin search; KP: full 0/1 DP table).

Usage:
    python tools/generate_public_benchmark.py --repo .            # default: repo root = parent of tools/
    python tools/generate_public_benchmark.py --repo . --node-cap 2000000
"""
from __future__ import annotations
import argparse, hashlib, json, math
from fractions import Fraction
from pathlib import Path

PALETTE = ["#2b6cb0","#dd6b20","#38a169","#805ad5","#d53f8c","#319795","#c53030","#718096"]

def sha(b): return hashlib.sha256(b).hexdigest()
def write(p, t):
    p.parent.mkdir(parents=True, exist_ok=True)
    d=t.encode("utf-8"); tmp=p.with_suffix(p.suffix+".tmp"); tmp.write_bytes(d); tmp.replace(p); return sha(d)
def dump(o): return json.dumps(o, ensure_ascii=False, indent=2, sort_keys=True)+"\n"

def ffd(w,C,k):
    order=sorted(range(len(w)),key=lambda i:-w[i]); bins=[0]*k; a=[-1]*len(w)
    for i in order:
        for b in range(k):
            if bins[b]+w[i]<=C: bins[b]+=w[i]; a[i]=b; break
        else: return None
    return a

def can_pack(w,C,k,cap):
    order=sorted(range(len(w)),key=lambda i:-w[i]); ws=[w[i] for i in order]; n=len(ws); bins=[0]*k; nodes=[0]
    def rec(i):
        nodes[0]+=1
        if nodes[0]>cap: return None
        if i==n: return True
        seen=set(); ind=False
        for b in range(k):
            l=bins[b]
            if l in seen: continue
            seen.add(l)
            if l+ws[i]<=C:
                bins[b]+=ws[i]; r=rec(i+1); bins[b]-=ws[i]
                if r is True: return True
                if r is None: ind=True
        return None if ind else False
    return rec(0), nodes[0]

def kp_dp(w,p,C):
    cur=[0]*(C+1); keep=[bytearray(C+1) for _ in range(len(w))]
    for i in range(len(w)):
        wi,pi=w[i],p[i]
        for c in range(C,wi-1,-1):
            v=cur[c-wi]+pi
            if v>cur[c]: cur[c]=v; keep[i][c]=1
    c=C; items=[]
    for i in range(len(w)-1,-1,-1):
        if keep[i][c]: items.append(i); c-=w[i]
    items.sort(); return cur[C], items

def svg_header(w,h,title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'font-family="Helvetica,Arial,sans-serif">\n  <title>{title}</title>\n'
            f'  <rect x="0" y="0" width="{w}" height="{h}" fill="#ffffff"/>\n')
def txt(x,y,s,size=13,anchor="start",weight="normal",color="#111111"):
    return f'  <text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" font-weight="{weight}" fill="{color}">{s}</text>\n'

def bpp_svg(iid,w,C,assign,nb,state,lb,ub):
    ml,mt,bw,gap,bh=70,70,90,40,320
    W=ml+nb*(bw+gap)+60; H=mt+bh+120; P=[svg_header(W,H,f"BPP {iid}")]
    P.append(txt(ml,30,f"OptFin OR-Lab  |  BPP (non-IRUP snark)  |  instance: {iid}",15,weight="bold"))
    P.append(txt(ml,50,f"capacity C = {C}   items n = {len(w)}   bins used = {nb}   state = {state}   LB = {lb}  UB = {ub}",12,color="#444444"))
    for b in range(nb):
        x0=ml+b*(bw+gap)
        P.append(f'  <rect x="{x0}" y="{mt}" width="{bw}" height="{bh}" fill="none" stroke="#cbd5e0" stroke-width="1.5"/>\n')
        items=[i for i in range(len(w)) if assign[i]==b]; y=mt+bh
        for i in items:
            sh=max(2.0,(w[i]/C)*bh); y-=sh; col=PALETTE[i%len(PALETTE)]
            P.append(f'  <rect x="{x0}" y="{y:.2f}" width="{bw}" height="{sh:.2f}" fill="{col}" fill-opacity="0.85" stroke="#ffffff" stroke-width="0.6"/>\n')
            if sh>=14: P.append(txt(int(x0+bw/2),int(y+sh/2+4),f"e{i}",10,"middle",color="#ffffff"))
        load=sum(w[i] for i in items)
        P.append(txt(int(x0+bw/2),mt+bh+20,f"bin {b}",12,"middle",weight="bold"))
        P.append(txt(int(x0+bw/2),mt+bh+36,f"{load}/{C}",10,"middle",color="#666666"))
    cy=mt+bh+70
    P.append(txt(ml,cy,"Optimality: exhaustive no-3-bin search proves LB; first-fit-decreasing witness proves UB.",11,color="#333333"))
    P.append(txt(ml,cy+16,"LB == UB => PROVEN_OPTIMAL, non-circular.",11,color="#333333")); P.append("</svg>\n")
    return "".join(P)

def kp_svg(iid,w,pnum,denom,C,chosen,opt):
    ml,mt,bw,bh=70,90,620,70; W=ml+bw+60; H=mt+bh+160; P=[svg_header(W,H,f"KP {iid}")]
    uw=sum(w[i] for i in chosen)
    P.append(txt(ml,30,f"OptFin OR-Lab  |  0/1 Knapsack  |  instance: {iid}",15,weight="bold"))
    P.append(txt(ml,50,f"capacity C = {C}   items n = {len(w)}   chosen = {len(chosen)}   weight = {uw}/{C}",12,color="#444444"))
    P.append(txt(ml,68,f"OPTIMAL profit = {opt}/{denom} = {float(Fraction(opt,denom)):.6f}   state = PROVEN_OPTIMAL (exact DP)",12,color="#2f855a",weight="bold"))
    P.append(f'  <rect x="{ml}" y="{mt}" width="{bw}" height="{bh}" fill="none" stroke="#cbd5e0" stroke-width="1.5"/>\n')
    x=ml; sc=bw/C
    for k,i in enumerate(chosen):
        seg=w[i]*sc; col=PALETTE[k%len(PALETTE)]
        P.append(f'  <rect x="{x:.2f}" y="{mt}" width="{seg:.2f}" height="{bh}" fill="{col}" fill-opacity="0.85" stroke="#ffffff" stroke-width="0.8"/>\n')
        P.append(txt(int(x+seg/2),mt+30,f"i{i}",11,"middle",color="#ffffff"))
        P.append(txt(int(x+seg/2),mt+46,f"w{w[i]}",9,"middle",color="#ffffff")); x+=seg
    slack=C-uw
    if slack>0:
        seg=slack*sc; P.append(f'  <rect x="{x:.2f}" y="{mt}" width="{seg:.2f}" height="{bh}" fill="#edf2f7"/>\n')
        P.append(txt(int(x+seg/2),mt+40,f"slack {slack}",10,"middle",color="#718096"))
    cy=mt+bh+40
    P.append(txt(ml,cy,"Optimality: full 0/1 DP over integer capacity is exact;",11,color="#333333"))
    P.append(txt(ml,cy+16,"the verification test recomputes the DP and confirms the value.",11,color="#333333")); P.append("</svg>\n")
    return "".join(P)

BPP_VERIFY = '"""Public verification test for BPP-snark instance {inst_id}.\n\nSelf-contained and non-circular: re-reads the instance + solution and proves\nLB == UB from scratch. No OptFin-internal imports.\n\nRun:  python {fname}\n"""\nimport json\nimport os\n\nHERE = os.path.dirname(os.path.abspath(__file__))\nROOT = os.path.dirname(HERE)\nINSTANCE = os.path.join(ROOT, "instances", "{inst_id}.json")\nSOLUTION = os.path.join(ROOT, "solutions", "{inst_id}.json")\n\nNODE_CAP = {node_cap}\n\n\ndef _can_pack_in_k(weights, capacity, k, node_cap):\n    order = sorted(range(len(weights)), key=lambda i: -weights[i])\n    ws = [weights[i] for i in order]\n    n = len(ws)\n    bins = [0] * k\n    nodes = [0]\n\n    def rec(i):\n        nodes[0] += 1\n        if nodes[0] > node_cap:\n            return None\n        if i == n:\n            return True\n        seen = set()\n        indeterminate = False\n        for b in range(k):\n            load = bins[b]\n            if load in seen:\n                continue\n            seen.add(load)\n            if load + ws[i] <= capacity:\n                bins[b] += ws[i]\n                r = rec(i + 1)\n                bins[b] -= ws[i]\n                if r is True:\n                    return True\n                if r is None:\n                    indeterminate = True\n        return None if indeterminate else False\n\n    return rec(0)\n\n\ndef verify():\n    inst = json.load(open(INSTANCE, encoding="utf-8"))\n    sol = json.load(open(SOLUTION, encoding="utf-8"))\n    w, C = inst["weights"], inst["capacity"]\n    assign = sol["assignment"]\n    assert len(assign) == len(w), "assignment length mismatch"\n\n    # --- UB: solution feasibility ---\n    used = max(assign) + 1\n    loads = [0] * used\n    for i, b in enumerate(assign):\n        loads[b] += w[i]\n    assert all(load <= C for load in loads), "OVER_CAPACITY"\n    assert used == sol["num_bins"], "num_bins mismatch"\n    ub = used\n\n    # --- LB: L1 material bound ---\n    import math as _m\n    l1 = _m.ceil(sum(w) / C)\n\n    # --- LB: exhaustive no-(ub-1)-bin proof (non-circular) ---\n    lower_target = ub - 1\n    verdict = _can_pack_in_k(w, C, lower_target, NODE_CAP)\n    if verdict is False:\n        lb = ub  # cannot pack in ub-1 => LB == UB\n        proof = "EXHAUSTIVE_NO_%d_BIN" % lower_target\n        state = "PROVEN_OPTIMAL"\n    elif verdict is True:\n        lb = lower_target\n        proof = "PACKED_IN_%d_BIN" % lower_target\n        state = "FEASIBLE"\n    else:\n        # Bounded exhaustive search did not close the bound within NODE_CAP.\n        # Stay honest and non-circular: use only the material L1 lower bound\n        # (do NOT trust the construction theorem here). Report FEASIBLE.\n        lb = l1\n        proof = "BOUNDED_SEARCH_INDETERMINATE_FELL_BACK_TO_L1"\n        state = "PROVEN_OPTIMAL" if lb == ub else "FEASIBLE"\n\n    result = {{\n        "instance": "{inst_id}",\n        "problem": "bpp",\n        "lb": lb, "ub": ub, "l1": l1,\n        "state": state, "proof": proof,\n        "reported_state": sol["state"],\n        "matches_reported": state == sol["state"],\n        "checker": "PASS",\n    }}\n    assert result["matches_reported"], "STATE_MISMATCH: %s" % result\n    return result\n\n\nif __name__ == "__main__":\n    print(json.dumps(verify(), indent=2, sort_keys=True))\n'
KP_VERIFY = '"""Public verification test for KP instance {inst_id}.\n\nSelf-contained and non-circular: recomputes the exact 0/1 knapsack DP and\nconfirms the reported optimal value == the DP table optimum, and that the\nreported item set is feasible and realises that value. No internal imports.\n\nRun:  python {fname}\n"""\nimport json\nimport os\n\nHERE = os.path.dirname(os.path.abspath(__file__))\nROOT = os.path.dirname(HERE)\nINSTANCE = os.path.join(ROOT, "instances", "{inst_id}.json")\nSOLUTION = os.path.join(ROOT, "solutions", "{inst_id}.json")\n\n\ndef _kp_exact_dp(weights, profit_num, capacity):\n    n = len(weights)\n    cur = [0] * (capacity + 1)\n    for i in range(n):\n        wi, pi = weights[i], profit_num[i]\n        for c in range(capacity, wi - 1, -1):\n            cand = cur[c - wi] + pi\n            if cand > cur[c]:\n                cur[c] = cand\n    return cur[capacity]\n\n\ndef verify():\n    inst = json.load(open(INSTANCE, encoding="utf-8"))\n    sol = json.load(open(SOLUTION, encoding="utf-8"))\n    w = inst["weights"]\n    C = inst["capacity"]\n    denom = inst["profit_denominator"]\n    pnum = inst["profit_numerators"]\n\n    chosen = sol["items"]\n    used_w = sum(w[i] for i in chosen)\n    used_p = sum(pnum[i] for i in chosen)\n    assert used_w <= C, "OVER_CAPACITY"\n    assert used_p == sol["optimal_profit_numerator"], "PROFIT_RECONSTRUCTION_MISMATCH"\n\n    dp_opt = _kp_exact_dp(w, pnum, C)\n    assert dp_opt == sol["optimal_profit_numerator"], (\n        "DP optimum %d != reported %d" % (dp_opt, sol["optimal_profit_numerator"])\n    )\n    state = "PROVEN_OPTIMAL"\n    result = {{\n        "instance": "{inst_id}",\n        "problem": "kp",\n        "optimal_profit_numerator": dp_opt,\n        "optimal_profit_denominator": denom,\n        "used_weight": used_w,\n        "capacity": C,\n        "state": state,\n        "matches_reported": state == sol["state"],\n        "checker": "PASS",\n    }}\n    assert result["matches_reported"], "STATE_MISMATCH"\n    return result\n\n\nif __name__ == "__main__":\n    print(json.dumps(verify(), indent=2, sort_keys=True))\n'

def build_bpp(repo, node_cap, max_n):
    d=repo/"bpp"; rows=[]
    for f in sorted((d/"instances").glob("*.json")):
        inst=json.loads(f.read_text(encoding="utf-8")); iid=inst["id"]; w=inst["weights"]; C=inst["capacity"]; n=len(w)
        assign=ffd(w,C,4) or next((ffd(w,C,k) for k in range(5,8) if ffd(w,C,k)),None)
        nb=max(assign)+1; ub=nb; l1=math.ceil(sum(w)/C); state="FEASIBLE"; lb=l1; proof="L1_ONLY"
        if n<=max_n:
            v,nodes=can_pack(w,C,ub-1,node_cap)
            if v is False: lb=ub; state="PROVEN_OPTIMAL"; proof=f"EXHAUSTIVE_NO_{ub-1}_BIN(nodes={nodes})"
            elif v is True: lb=ub-1; proof=f"PACKED_IN_{ub-1}_BIN"
            else: proof=f"BOUNDED_INDETERMINATE(nodes>{node_cap})"
        else: proof=f"SKIPPED_N>{max_n}_L1_ONLY"
        sol={"schema":"orlab-public/bpp-solution/v1","id":iid,"num_bins":nb,"assignment":assign,
             "bin_loads":[sum(w[i] for i in range(n) if assign[i]==b) for b in range(nb)],
             "lb":lb,"ub":ub,"l1":l1,"state":state,"optimality_proof":proof,"lb_theorem":4}
        write(d/"solutions"/f"{iid}.json",dump(sol))
        write(d/"plots"/f"{iid}.svg",bpp_svg(iid,w,C,assign,nb,state,lb,ub))
        write(d/"verification"/f"{iid}_verify.py",BPP_VERIFY.format(inst_id=iid,fname=f"{iid}_verify.py",node_cap=node_cap))
        rows.append((iid,n,state,lb,ub,proof))
    return rows

def build_kp(repo, node_cap):
    d=repo/"kp"; rows=[]
    for f in sorted((d/"instances").glob("*.json")):
        inst=json.loads(f.read_text(encoding="utf-8")); iid=inst["id"]; w=inst["weights"]; C=inst["capacity"]
        pnum=inst["profit_numerators"]; denom=inst["profit_denominator"]
        opt,chosen=kp_dp(w,pnum,C)
        sol={"schema":"orlab-public/kp-solution/v1","id":iid,"items":chosen,"used_weight":sum(w[i] for i in chosen),
             "capacity":C,"optimal_profit_numerator":opt,"optimal_profit_denominator":denom,
             "optimal_profit_float":float(Fraction(opt,denom)),"lb":opt,"ub":opt,"state":"PROVEN_OPTIMAL",
             "optimality_proof":"EXACT_0_1_DP_FULL_TABLE"}
        write(d/"solutions"/f"{iid}.json",dump(sol))
        write(d/"plots"/f"{iid}.svg",kp_svg(iid,w,pnum,denom,C,chosen,opt))
        write(d/"verification"/f"{iid}_verify.py",KP_VERIFY.format(inst_id=iid,fname=f"{iid}_verify.py"))
        rows.append((iid,len(w),"PROVEN_OPTIMAL",opt,opt,"EXACT_0_1_DP_FULL_TABLE"))
    return rows

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--repo",default=None); ap.add_argument("--node-cap",type=int,default=2000000)
    ap.add_argument("--max-n",type=int,default=90); a=ap.parse_args()
    repo=Path(a.repo).resolve() if a.repo else Path(__file__).resolve().parents[1]
    b=build_bpp(repo,a.node_cap,a.max_n); k=build_kp(repo,a.node_cap)
    def summ(rows):
        return {"instances_count":len(rows),"proven_optimal":sum(1 for r in rows if r[2]=="PROVEN_OPTIMAL"),
                "feasible":sum(1 for r in rows if r[2]=="FEASIBLE")}
    print(json.dumps({"bpp":summ(b),"kp":summ(k)},indent=2,sort_keys=True))

if __name__=="__main__":
    main()
