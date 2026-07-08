# Sample size — vignette experiment

## Primary contrast (H1, H2)
- **Test:** independent-samples $t$ test (current vs BLE) on a
  participant-level mean of 4 within-participant trials.
- **Alpha:** 0.05 two-sided.
- **Power target:** 0.80.

Expected effect size for **comprehension (H1)**: Cohen's $d = 0.40$
(medium). Rationale: in Zhang et al. (2022) the effect of a labelled
versus an unlabelled iOS condition on category recall was $d \approx
0.45$; we down-weight slightly to be conservative because our
manipulation is "labelled vs better-labelled" rather than
"unlabelled vs labelled".

At $d{=}0.40$, $\alpha{=}0.05$, power $0.80$, two-sided, the required
sample per group is:
$$
n = 2 \cdot \frac{(z_{1-\alpha/2} + z_{1-\beta})^2}{d^2}
  = 2 \cdot \frac{(1.96 + 0.84)^2}{0.16}
  \approx 99 \text{ per group}.
$$
Total target **N = 200** raw, expected $\sim 160$ after exclusions.

## Secondary contrast (H4)
H4 is a within-condition correlation between drawer-opening rate and
the published Maybe-rate per boundary case (9 cases per participant
in the BLE arm). Power is over-determined at $N_{\text{BLE}} \approx
80$ for the expected $\rho \geq 0.5$ across-case correlation.

## Null effect (H5)
H5 is a directional null on installation intent. We run an equivalence
test (TOST) with smallest effect size of interest $d = 0.30$. At
$d_{\text{SESOI}}{=}0.30$, $\alpha{=}0.05$, power $0.80$, the required
$n$ per group is $\sim 175$. **Hence H5 is reported as exploratory
unless we hit the larger budget of $N{=}400$.** The pre-registration
notes this explicitly: H5 is the only hypothesis whose default sample
budget under-powers; we will report a TOST $p$ value plus the
two-sided CI for the install-intent difference and refrain from
making a "no effect" claim if the CI includes $d{=}0.30$.

## Pilot
A pilot of $N{=}10$ (5 per condition) will be run before the main
study to verify
- median completion time ($\approx 15$ min target),
- MCQ option clarity (no option chosen $> 80\%$ regardless of
  condition),
- BLE drawer discoverability (at least 50\% of BLE participants
  open $\geq 1$ drawer).

If discoverability is below 50\%, we will revise the drawer affordance
(e.g., add a subtle pulse animation) before the main collection and
note the revision in the pre-registration.

## Budget
- Prolific compensation: USD~\$3 $\times$ 200 = USD~\$600.
- Prolific platform fee: \$120.
- Pilot: USD~\$30.
- Contingency for re-runs: USD~\$100.
- **Total: USD~\$850.**

## Stopping rule
We stop recruitment when (i) at least 80 valid responses per condition
are reached and (ii) the planned sample (200) is completed, whichever
is later. We do not run interim analyses on the primary contrast.
