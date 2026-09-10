# Changelog

All notable changes to the OptFin OR-Lab public benchmark.

## [Unreleased] - 2026-09-10

### Added
- **`roadef/` — EURO/ROADEF 2026 "Keep the Flow!" (T-ASR) segment-routing MLU
  minimization.** Generated deterministically by
  `tools/generate_public_benchmark.py` (new `build_roadef`). Per instance:
  - our SR-path solution witness in the official submission format
    (`roadef/solutions/<id>-srpaths.json`) — our routing decisions, our content;
  - a vector SVG of the reported MLU + our solution structure
    (`roadef/plots/<id>.svg`);
  - a self-contained, non-circular verification test
    (`roadef/verification/<id>_verify.py`) that RE-DERIVES the optimality state
    from the published directed-capacity-cut arithmetic
    (`LB = crossing_demand / capacity`, `round(LB,6) == round(UB,6)`), never a
    solver flag; a mislabelled instance makes the test fail;
  - `roadef/metadata.json` (our reported UB/LB/gap/state + LB certificates);
  - `roadef/RESULTS.md` per-instance table.
- 32 instances: **6 PROVEN_OPTIMAL** (all Set B: setB-02, setB-03, setB-06,
  setB-08, setB-09, setB-10), **26 FEASIBLE**, **0 OPEN**. All witnesses are
  validated by the official ROADEF checker.

### Intellectual property
- The ROADEF challenge instances (net/tm/scenario) and the official checker are
  third-party (challenge organizers) and are **NOT redistributed** here — they
  are linked and attributed (https://www.roadef.org/challenge/2026/en/). Only
  our SR-path solutions, plots and verification tests are published (CC BY 4.0,
  attribution optfin.org). See `roadef/README.md` and `LICENSES.md`.

### Changed
- `README.md`, `LICENSES.md`: document the `roadef/` section and its strict
  link-not-republish policy for the third-party instances and checker.
- `INDEX.json`: regenerated with the new files and the roadef summary
  (`third_party_instances: true`, `instances_redistributed: false`).

## [0.1.0] - 2026-09-09

### Added
- Initial public benchmark: `bpp/` (bin packing, snark non-IRUP construction) and
  `kp/` (0/1 knapsack), each with instances, solutions, SVG plots and
  self-contained optimality verification, plus the deterministic generator.
