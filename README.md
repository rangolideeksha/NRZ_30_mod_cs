# Project Requirements & Specification
**C-band Silicon Microring Modulator — Open PDK Extension on CORNERSTONE SOI 220 nm Active**

| | |
|---|---|
| Status | Draft v0.1 |
| Owner | Deeksha |
| Type | Design-only (no fabrication in scope) |
| Last updated | 2026-10-03 |

---

## 1. Problem statement

Design a carrier-depletion **microring modulator** on the CORNERSTONE SOI 220 nm active platform, C-band (1550 nm), TE, delivering **30 Gb/s NRZ-OOK**, with edge-coupled optical I/O and RF-probeable GSG electrical I/O.

Deliver it as versioned, CI-verified **PDK cells with compact models**, together with **process-monitor and yield test structures**, placed within a **partial-reticle MPW tile**.

Outputs: DRC-clean GDS, simulated performance against spec, and a test plan.

## 2. Goals

1. Learn and demonstrate the full PDK flow: layer stack → cross-sections → parametric cells → compact models → layout → DRC → regression tests → release.
2. Demonstrate device design under real foundry constraints (fixed implant doses, fixed etch depths, real design rules).
3. Produce a public repository that shows design reasoning, not just results.

## 3. Platform

| Item | Choice | Note |
|---|---|---|
| Foundry process | CORNERSTONE SOI 220 nm active | Fixed p/n implant doses, heaters, metal |
| Base PDK | `cspdk.si220.cband` (gdsfactory) | Passive layers, cross-sections, CI scaffolding |
| Active layers & rules | `cornerstone-community/Si_220nm_active` | Doping, contacts, metal, DRC deck |
| Wavelength | C-band, 1550 nm, TE | O-band port noted as future work |
| Reference device | CORNERSTONE `SOI220nm_1550nm_TE_MZI_Modulator` | Sanity check for junction model |

**Rationale for C-band:** existing C-band edge coupler in the CORNERSTONE community library; plasma-dispersion coefficients and published ring-modulator benchmarks are most widely available at 1550 nm; most open-tool tutorials default to 1550 nm. Porting to O-band requires re-optimising the coupler, ring FSR and dispersion coefficients.

## 4. Device specification

Simulated, nominal process corner, room temperature.

| ID | Parameter | Target | Verified by |
|---|---|---|---|
| D1 | Data rate | 30 Gb/s NRZ-OOK | Time-domain eye simulation |
| D2 | EO bandwidth (3 dB) | ≥ 20 GHz | Photon lifetime + RC model |
| D3 | Drive swing | ≤ 2 Vpp, reverse bias only | Junction simulation |
| D4 | Dynamic extinction ratio | ≥ 4 dB | Eye simulation |
| D5 | On-chip insertion loss at operating point | ≤ 3 dB | Ring model with doped loss |
| D6 | Thermal tuning range | ≥ 1 FSR; report mW/FSR | Heater thermal model |
| D7 | Loaded Q | Chosen to satisfy D2 (expected ~3k–6k) | Ring model |
| D8 | Fibre-to-fibre loss budget | Tabulated per element | Loss budget table |

## 5. Design decisions

| Decision | Choice | Reason |
|---|---|---|
| Modulator type | Microring, carrier depletion | Short doped length → lower loss and footprint than MZM |
| Doping | Fixed by process | Design knobs are geometric only |
| Design knobs | Junction offset, p++/n++ spacing from waveguide, ring radius, coupling gap, doped arc fraction | — |
| Optical I/O | Edge couplers | Packaging-relevant, broadband |

## 6. Packaging constraints

**Optical**
- All optical I/O on one chip edge.
- 127 µm pitch for fibre-array attach.
- Edge couplers at facet; CORNERSTONE dicing/trench rules applied.

**Electrical**
- RF: GSG pads, 100 or 150 µm pitch, on the edge opposite the optical I/O.
- DC: heater and bias pads in a single row at standard probe-card pitch.
- Pads stated as wire-bond compatible; no wire-bond or flip-chip design in scope.

## 7. Test structures

| ID | Structure | Extracts |
|---|---|---|
| T1 | Waveguide cutback (strip and rib) | Propagation loss |
| T2 | Edge-coupler back-to-back pairs | Coupling loss per facet |
| T3 | Undoped rings, gap sweep | Intrinsic Q, coupling coefficient, gap sensitivity |
| T4 | Doped vs undoped ring pairs | Doping-induced loss |
| T5 | Doped-silicon TLM bars | Sheet and contact resistance |
| T6 | Junction-only device | Capacitance vs voltage |
| T7 | Ring width/radius variants + replicated DUTs (N ≥ 5) | Resonance spread for yield |
| T8 | Heater-only ring | Thermal tuning efficiency |

**Root-cause mapping:** an under-performing modulator is attributed to optical loss (T1, T4), coupling (T2, T3), resistance (T5), capacitance (T6) or process variation (T7).

## 8. Yield analysis (design-only)

- Monte Carlo over waveguide width, slab thickness and junction misalignment, using CORNERSTONE design-rule tolerances.
- Report: fraction of devices meeting D2–D5; heater power required to recover resonance alignment.
- Test plan maps the analysis onto T7 so yield measurement is defined for a future fabrication run.

## 9. PDK deliverables

| Cell | Parametric cell | Ports | Model | GDS regression |
|---|---|---|---|---|
| Rib cross-section with junction | ✓ | — | n_eff(V), α(V) | — |
| Ring modulator | ✓ | ✓ | S-params vs V, λ | ✓ |
| GSG pad | ✓ | ✓ | RC (lumped) | ✓ |
| Edge coupler (ported if needed) | ✓ | ✓ | S-params | ✓ |
| Test structures T1–T8 | ✓ | ✓ | where applicable | ✓ |
| Full tile | — | — | — | ✓ |

## 10. Verification & CI

On every pull request:
- Unit tests for models.
- GDS regression tests for all cells.
- DRC on all cells and the full tile (KLayout, headless).
- Full tile build.

Releases: semantic version tags, changelog, built docs.

## 11. Definition of done

- [ ] All D1–D8 reported against target, with the trade-off plot (loss vs efficiency vs bandwidth).
- [ ] 30 Gb/s eye diagram from the compact model.
- [ ] Monte Carlo yield plot.
- [ ] All cells and tile DRC-clean in CI.
- [ ] Tagged release with docs and loss budget.

## 12. Out of scope

Driver electronics, thermal control loop, PAM4, WDM, travelling-wave electrode design, fabrication, measurement.

## 13. Open questions

| ID | Question | Action |
|---|---|---|
| Q1 | Tile size for partial reticle | Check current CORNERSTONE MPW call; assume 2.5 × 5 mm until confirmed |
| Q2 | Is the C-band edge coupler compatible with active-platform layers and rules? | Port and run DRC |
| Q3 | Implant doping concentrations | Request from CORNERSTONE (pdk.cornerstone@soton.ac.uk) |
| Q4 | Junction simulation tool | Evaluate gplugins DEVSIM status; fallback: analytic depletion model |
| Q5 | Metal stack for RF pads | Confirm layers available in active platform |

## 14. Revision history

| Version | Date | Change |
|---|---|---|
| 0.1 | 2026-10-03 | Initial draft |
