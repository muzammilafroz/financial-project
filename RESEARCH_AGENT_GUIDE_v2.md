# Research Agent Guide
## Growth, Inflation, and Fiscal Health of Arunachal Pradesh
### Financial Programming — Project 1 (Mid-Term) + Project 2 (End-Term)
**Student:** S.M. Muzammil Afroz | **State:** Arunachal Pradesh (AR)  
**Supervisor:** M. Parameswaran | **Institution:** Centre For Development Studies

---

## SECTION 0 — MASTER DATA INVENTORY

### Files Available

| File | Content | Period | Unit | Notes |
|------|---------|--------|------|-------|
| `2011-12_Back_Series_-_GSDP__Constant_Prices__Arunachal_Pradesh.xlsx` | AR GSDP constant prices (2011-12 base), 44 sector columns + 3-sector aggregates + growth rates | 1980-81 to 2024-25 | Rs Lakh | Row 3 = headers; data rows match pattern NNNN-NNNN; last rows are metadata labels |
| `2011-12_Back_Series_-_GSDP__Current_Prices__Arunachal_Pradesh.xlsx` | AR GSDP current prices, same structure | 1980-81 to 2024-25 | Rs Lakh | Same structure as above |
| `2011-12_Back_Series_-_Per_Capita_NSDP__Constant_Prices__Arunachal_Pradesh.xlsx` | Per capita NSDP constant prices, all 33 states + UTs, wide format | 1960-61 to 2024-25 (AR: 1970-71) | Rs | Row 2 = state names; row 3 = "Year"/"Per Capita NSDP" repeated; data from row 4 |
| `2011-12_Back_Series_-_Per_Capita_NSDP__Current_Prices__Arunachal_Pradesh.xlsx` | Per capita NSDP current prices, all states | 1960-61 to 2024-25 (AR: 1970-71) | Rs | Same structure |
| `State_Finances_-_Arunachal.XLSX` | State budget — 353 budget heads across 4 appendices (Revenue Receipts, Revenue Expenditure, Capital Receipts, Capital Disbursements) | 1990-91 to 2025-26 | Rs Crore | Columns: Appendix, State, Budget Head, Fiscal Year, Account, Revised, Budget |
| `All_India_CPI_Base_Year_2012.xlsx` | All-India CPI monthly, 28 sub-items, Rural/Urban/Combined + Weights sheet | Jan 2011 – Dec 2025 | Index (2012=100) | **Month column is numeric integer (1–12)**; 4 extra unnamed columns present — drop them on read; Status: F=Final, P=Provisional |
| `Arunachal_CPI_Base_Year_2012.xlsx` | AR CPI monthly, 6 group-level items, Rural only + Weights sheet | Jan 2011 – Dec 2025 | Index (2012=100) | **Month column is text (e.g., "January")**; Urban column = 100% NA; Combined column = identical to Rural wherever non-null (~8–10 sporadic values in 2018 and 2020 only) — treat Combined as Rural; use Rural column exclusively |
| `All_India_National_Account_Statistics_2011-12_Series.xlsx` | Full NAS India: GVA, GDP, NDP, PFCE, GFCE, GFCF etc., current + constant | 1950-51 to 2025-26 | Rs Crore | Complex multi-row header structure |
| `AllindiaGDP.xlsx` | Simplified: All-India GDP at current and constant prices | 1950-51 to 2025-26 | Rs Crore | Three clean columns: Year, GDP current, GDP constant; use as primary All-India GDP source |

### Confirmed Data Availability by Analysis

| Required Analysis | Available? | Source | Gap |
|---|---|---|---|
| AR GSDP trend growth, constant prices | ✅ | GSDP Constant file | — |
| All-India GDP trend growth | ✅ | AllindiaGDP.xlsx | — |
| Structural breaks, AR and All-India | ✅ | Both GDP files | — |
| Quarterly CPI inflation, All-India | ✅ | All India CPI | — |
| Quarterly CPI inflation, AR (rural) | ✅ | Arunachal CPI | Rural only; no urban |
| GSDP deflator-based inflation, AR | ✅ | Derived from current + constant GSDP | Annual only; quarterly via Denton |
| Annual headline inflation | ✅ | Both CPI files | — |
| Annual core inflation | ✅ | Both CPI files + weights | AR group-level only |
| Sectoral decomposition of GSDP | ✅ | GSDP files | — |
| Convergence analysis, all states | ✅ | Per Capita NSDP files | — |
| **[PROJECT 2] Revenue deficit / GSDP** | ✅ | RBI State Finances backbone + official budget top-up | Final window now extends to 2026-27 |
| **[PROJECT 2] Fiscal deficit / GSDP** | ✅ | RBI State Finances backbone + official budget top-up | Official and broad deficit concepts both retained |
| **[PROJECT 2] Primary deficit / GSDP** | ✅ | Derived from official fiscal deficit - interest | Final window now extends to 2026-27 |
| **[PROJECT 2] Interest / Revenue Expenditure** | ✅ | Both in Appendix-2 of State Finances | — |
| **[PROJECT 2] 2026-27 Budget data** | ✅ | `Data/Project2_Budget_Documents/` | Official Arunachal budget packet downloaded and used |

---

### 2026-04-27 Project 2 Status Update

- RBI State Finance Database remains the backbone for Project 2.
- Official 2026-27 Arunachal budget documents have now been downloaded into `Data/Project2_Budget_Documents/`.
- The final Project 2 window is `2022-23` to `2026-27`.
- `2024-25` now uses official actuals, `2025-26` uses revised estimates, and `2026-27` uses budget estimates from the official budget packet.
- The notebook now reports both the official state-budget deficit concept and the broader PRS-style deficit concept.

### 2026-04-29 Project 2 Research Extension Status

- The final Project 2 paper now adds three empirical extensions: own-tax buoyancy, 16th Finance Commission transfer-shock simulation, and cross-state comparison.
- New output tables are `table23_project2_tax_buoyancy_regression.csv`, `table24_project2_16fc_simulation.csv`, `table25_project2_cross_state_comparison.csv`, and `table26_project2_extension_diagnostics.csv`.
- New figures are `fig19_project2_tax_buoyancy.png`, `fig20_project2_transfer_shock.png`, and `fig21_project2_cross_state_comparison.png`.
- Do not describe Route 1 as weak elasticity. The estimated own-tax elasticity is about 1.69; the paper's stronger claim is that tax buoyancy coexists with a small own-revenue base relative to expenditure responsibilities.

## SECTION 1 — FILE READING NOTES

### GSDP Files
- Header rows are rows 1–2 (title and state name). Row 3 is the column header row.
- Data rows match the pattern `NNNN-NNNN` (e.g., `1980-1981`). Trailing rows contain metadata labels — filter these out.
- Standardize year format to `NNNN-NN` (e.g., `1980-81`) for consistency across all files. Extract numeric year as the first four digits (e.g., 1980) for time trend construction.
- The key column for GSDP series is `State Domestic Product (SDP)(Rs Lakh)`.
- Broad sector columns are labeled `Agriculture and Allied Activities(Rs Lakh)`, `Industry(Rs Lakh)`, `Services(Rs Lakh)` — use these for sectoral composition analysis.

### State Finances File — Appendix Structure
The file has 4 appendices with distinct economic meaning:

| Appendix | Content | Key Total Line |
|----------|---------|----------------|
| Appendix-1 | Revenue Receipts (Tax + Non-Tax + Grants from Centre) | `Total: TOTAL REVENUE (I+II)` |
| Appendix-2 | Revenue Expenditure (Developmental + Non-Developmental + Grants-in-Aid) | `Total: TOTAL EXPENDITURE (I+II+III)` |
| Appendix-3 | Capital Receipts (Internal Debt, Loans from Centre, etc.) | `total: TOTAL CAPITAL RECEIPTS (I to XII)` |
| Appendix-4 | Capital Disbursements (Capital Outlay, Loan Repayments, etc.) | `Total: TOTAL CAPITAL DISBURSEMENTS (I to XII)` |

**Critical interpretation:** `Total: TOTAL EXPENDITURE (I+II+III)` in Appendix-2 is **Revenue Expenditure only** — not total government expenditure. Capital outlay is in Appendix-4. This distinction is essential for computing interest as a percent of revenue expenditure.

### Data Priority Rule (per project instructions)
Use figures in this priority order for each year:
- Up to 2023-24: **Account** column (actual audited figures)
- 2024-25: **Actual** from the 2026-27 Arunachal budget packet
- 2025-26: **Revised Estimate** from the 2026-27 Arunachal budget packet
- 2026-27: **Budget Estimate** from the 2026-27 Arunachal budget packet

### AR CPI Weights (confirmed, already normalized)
| Item | Rural Weight (%) | Urban Weight (%) |
|------|-----------------|-----------------|
| Food and beverages | 52.94 | 41.68 |
| — of which: Cereals and products | 13.43 | 8.59 |
| — of which: Meat and fish | 11.42 | 8.41 |
| — of which: Vegetables | 9.27 | 7.37 |
| Pan, tobacco and intoxicants | 6.14 | 4.74 |
| Clothing and footwear | 6.44 | 7.35 |
| Housing | N/A (rural) | 6.31 |
| Fuel and light | 9.78 | 5.64 |
| Miscellaneous | 24.70 | 34.29 |
| **General Index** | **100.00** | **100.00** |

Urban weights shown for reference only — Urban CPI is absent for AR. All AR CPI analysis uses Rural only.

---

## SECTION 2 — KEY DERIVED VARIABLES AND THEIR CONSTRUCTION

### 2.1 GSDP Implicit Deflator (AR and All-India)
Computed as: `Deflator(t) = [GSDP_current(t) / GSDP_constant(t)] × 100`  
Base year: 2011-12 = 100 for both.  
Year-on-year change in log deflator × 100 gives annual deflator-based inflation rate.

### 2.2 Quarterly CPI Inflation
CPI data is monthly. Aggregate to quarters using arithmetic mean of 3 monthly values. Indian fiscal year quarters:

| Quarter | Calendar Months | Month numbers (All-India) |
|---------|----------------|--------------------------|
| Q1 | April, May, June | 4, 5, 6 |
| Q2 | July, August, September | 7, 8, 9 |
| Q3 | October, November, December | 10, 11, 12 |
| Q4 | January, February, March | 1, 2, 3 |

**CRITICAL — two different month encodings in the two files:**
- **All-India CPI:** Month column is **integer** (1 = January, 12 = December). Use numeric comparisons directly.
- **Arunachal Pradesh CPI:** Month column is **text string** (e.g., `"January"`, `"February"`). Must map to integers before fiscal quarter assignment.

**Note:** Jan–Mar 2011 in the CPI data belongs to Q4 of FY 2010-11, not FY 2011-12. Be careful with fiscal year assignment. Fiscal year = calendar year if month ≥ 4, else calendar year − 1.

Quarterly inflation = year-on-year percentage change: `[CPI_q(t) / CPI_q(t−4) − 1] × 100`  
This eliminates seasonal effects. First available quarterly YoY inflation is Q1 FY 2012-13.

**AR CPI data gap — 2020:** April and May 2020 values are missing (COVID-19 lockdown). Q1 FY 2020-21 will therefore be based on only one month (June 2020). Flag this clearly in the output rather than computing a potentially misleading average.

### 2.3 Core Inflation — Computation Method
**Implemented method:** inclusion-method core inflation using the retained non-food, non-fuel components that are consistently available in the uploaded CPI files.

For **All-India Core**, use:
- Clothing and footwear
- Housing
- Miscellaneous

For **AR Core**, use:
- Clothing and footwear
- Miscellaneous

This is the method currently implemented in `full_analysis.ipynb` and reflected in the updated Project 1 paper. It is preferred here because the Arunachal CPI file is rural-only, group-level, and does not provide a usable housing series.

Annual inflation = compute annual average CPI from monthly values (12 months per fiscal year, except clearly flagged missing-data years), then take year-on-year percentage change.

**Limitation for AR:** AR CPI is only at group level and lacks housing. AR core inflation is therefore a narrower two-component rural measure and should be treated as indicative rather than exactly comparable to the all-India core series.

Report for 2011-12 to 2024-25 in the current notebook outputs.

### 2.4 Quarterly GSDP Deflator via Denton-Cholette Interpolation
AR GSDP is annual. To derive a quarterly deflator, quarterly current-price and constant-price GSDP estimates are needed.

**Method:** Denton-Cholette temporal disaggregation (additive variant, no related indicator), using the `tempdisagg` R package. This distributes annual GSDP across quarters while exactly preserving the annual benchmark (sum of four quarters = annual total). The procedure minimises revisions between adjacent quarters.

Apply separately to:
- AR GSDP at current prices (1980-81 to 2024-25 → quarterly)
- AR GSDP at constant prices (same period)

Verify after interpolation that sum of each year's four quarters exactly equals the published annual figure.

**Important caveat:** Denton-interpolated quarterly GSDP is smoother than true quarterly data. The quarterly deflator derived from it reflects annual trends distributed smoothly — do not over-interpret quarter-to-quarter movements. State this in the paper.

### 2.5 Project 2 Fiscal Indicators — Construction

**All figures in Rs Crore. GSDP in Rs Lakh → convert to Crore by dividing by 100.**

#### Revenue Deficit (Project 2 definition)
In the Indian state accounts framework, the Revenue Account records Revenue Receipts (Appendix-1) and Revenue Expenditure (Appendix-2). The balance is:

`Revenue Surplus/Deficit = Revenue Receipts − Revenue Expenditure`

This can be cross-checked against the direct head **`A: Surplus (+)/Deficit (-) on Revenue Account`** when using the RBI State Finance Database.  
A **positive value = Revenue Surplus** (AR's case). A negative value = Revenue Deficit.  
For the final Project 2 table, use budget-document values for `2024-25 Actual`, `2025-26 RE`, and `2026-27 BE`.

#### Fiscal Deficit
Do **not** treat the RBI head **`C: Overall Surplus (+)/Deficit (-) (A+B)`** as the final Project 2 fiscal-deficit concept. It is useful historically, but it does not line up cleanly with the official 2026-27 budget presentation.

Use a two-layer approach instead:

1. **Broad PRS-style fiscal deficit**

`Broad Fiscal Deficit = Net Expenditure − Net Receipts`

where:
- `Net Expenditure = Revenue Expenditure + Total Capital Disbursements (Excluding Public Accounts)`
- `Net Receipts = Revenue Receipts + Recovery of Loans and Advances`

This is the broader accounting presentation used in the PRS 2026-27 budget analysis.

2. **Official state-budget fiscal deficit baseline**

`Official Fiscal Deficit = Broad Fiscal Deficit − Loans and Advances from the Centre`

This deduction captures the treatment of central capex loans in the official Arunachal budget presentation.  
For the assignment table, use the **official state-budget fiscal balance** as the baseline and retain the broad measure as a sensitivity/reconciliation table.

#### Primary Deficit
`Primary Balance = Fiscal Balance + Interest Payments`

Compute this for both:
- the official state-budget fiscal balance baseline, and
- the broad PRS-style fiscal balance sensitivity check.

Interest Payments available as: **`II.C.2: Interest Payments (i to iv)`** (Appendix-2, Non-Developmental Expenditure)

Primary Surplus/Deficit is then expressed as a percentage of GSDP.

#### Interest Expenditure as % of Revenue Expenditure
`Interest/RevExp ratio = [II.C.2: Interest Payments] / [Total: TOTAL EXPENDITURE (I+II+III)] × 100`

Both from Appendix-2. This measures the debt service burden on the revenue account.

### 2.6 Pre-computed Key Numbers (Verified from Data)

**Updated Project 2 baseline table (official state-budget presentation with RBI backbone):**

| Year | Rev Balance/GSDP | Official Fiscal Balance/GSDP | Official Primary Balance/GSDP | Interest/RevExp | Figure Type |
|------|------------------|------------------------------|-------------------------------|----------------|-------------|
| 2022-23 | +17.8% | -2.0% | +0.3% | 4.8% | Account |
| 2023-24 | +17.8% | +0.5% | +2.8% | 4.2% | Account |
| 2024-25 | +18.0% | +2.0% | +3.9% | 4.2% | Actual |
| 2025-26 | +16.9% | -1.6% | +0.8% | 3.6% | Revised Estimate |
| 2026-27 | +8.9% | -1.7% | +0.8% | 3.8% | Budget Estimate |

**Deficit-definition reconciliation (critical):**

| Year | Broad Fiscal Deficit/GSDP | Official Fiscal Deficit/GSDP | Central Capex Loans (Cr) |
|------|---------------------------|------------------------------|--------------------------|
| 2024-25 | 3.1% | -2.0% balance | 2,471 |
| 2025-26 | 10.5% | 1.6% deficit | 3,704 |
| 2026-27 | 11.0% | 1.7% deficit | 3,850 |

**CRITICAL ANALYTICAL FINDING:** AR consistently runs a very large **revenue surplus** and a very low **interest burden**, but that does not imply fiscal self-sufficiency. The state remains transfer dependent, and the fiscal-rule reading changes materially depending on whether central capex loans are deducted. This accounting distinction is now part of the Project 2 contribution and must be stated explicitly in the paper.

---

## SECTION 3 — STRUCTURAL BREAK METHODOLOGY

### 3.1 Theoretical Framework
Following Balakrishnan and Parameswaran (2007), the baseline growth model is:

`ln GDP(t) = α + β·t + u(t)`

where β is the instantaneous trend growth rate. CAGR = (e^β − 1) × 100.

Structural breaks are tested using **Bai and Perron (1998, 2003)** — the `strucchange` package in R implements this. The procedure tests for up to m breaks simultaneously, uses BIC to select the optimal number, and reports 95% confidence intervals for break dates.

Key settings: maximum breaks m = 5, trimming parameter ε = 0.10 (no breaks in outer 10% of observations).

### 3.2 Candidate Break Years for Arunachal Pradesh

| Year | Event | Prior Expectation for AR |
|------|-------|--------------------------|
| 1987-88 | NEFA → State of Arunachal Pradesh | **High** — regime change; central plan allocations surged |
| 1991-92 | Economic liberalisation | **Low** — AR insulated from market integration |
| 2004-05 | NE infrastructure push, DONER reforms | **Medium** |
| 2014-15 | NDA government, Pema Khandu era | **Low-Medium** |
| 2020-21 | COVID-19 | **Medium** — test as intercept shift separately |

The 1987-88 break is the primary novel hypothesis. If not selected by Bai-Perron, that is itself an important finding — it means the statehood transition did not statistically alter the growth trajectory, suggesting growth was already on the NEFA-era path.

### 3.3 Growth-Rate Models After Break Detection

Report two specifications, clearly separated:

**Baseline A: Boyce continuous kinked exponential model.** When breaks are identified at years T1*, T2*, ..., estimate:

`ln GDP(t) = alpha + beta1*t + beta2*(t-T1*)*D1(t) + beta3*(t-T2*)*D2(t) + u(t)`

where D_i(t) = 1 if t > T_i*, else 0. This is continuous at break points: the fitted log GDP path does not jump at breaks, only the growth rate changes. Regime slopes are linear combinations: before T1* = beta1; between T1* and T2* = beta1 + beta2; after T2* = beta1 + beta2 + beta3. Standard errors for these regime slopes must be HC1 delta-method standard errors for the relevant coefficient combinations, not the raw standard errors of the slope-change terms alone.

**Baseline B: segment-wise OLS / pure structural-change sensitivity.** Estimate a separate log-linear trend in each Bai-Perron regime:

`ln GDP_t = alpha_j + beta_j*t + u_t`

for regime j. This allows both intercept and slope to differ by regime, so it can show discontinuous level shifts at the break dates and gives direct regime-specific HC1 standard errors. Do not label this as the Boyce kinked model; Boyce (1986) proposed the continuity restriction as an alternative to discontinuous separate segment trend lines. Use Baseline B as a robustness and interpretation check, especially for administrative changes, rebasing, state reorganisation, or COVID-related level movements.

**Literature positioning:** Bai and Perron (1998, 2003) provide the multiple-break framework. Balakrishnan and Parameswaran (2007) estimate break dates in a pure structural-change setup where intercept and slope can vary, discuss partial vs pure structural breaks and level shifts, and then report growth rates by imposing Boyce kinks. Therefore the report should preserve Baseline A for comparability and add Baseline B for sensitivity.

**Always report heteroskedasticity-robust standard errors** (HC1) for all regression results.

**COVID intercept test:** Add a dummy D_covid = 1 for 2020-21 and after. A significant negative coefficient confirms a level shift below trend from COVID. Test this separately from the main break analysis.

---

## SECTION 4 — EXTENDED ANALYSIS (BEYOND PROJECT REQUIREMENTS)

### 4.1 Sectoral Decomposition of Growth
For each identified growth regime, decompose GSDP growth into Agriculture, Industry, and Services contributions. The decomposition is:

`g(GSDP) = Σᵢ [share_i × g_i] + Σᵢ [Δshare_i × g_i] + Interaction`

Rising share of public administration within services (visible in the sectoral GSDP columns) over time would confirm "growth without transformation."

### 4.2 Convergence Analysis
Using per capita NSDP for all states:
- **Sigma-convergence:** Does cross-state dispersion (standard deviation of log per capita NSDP) decline over time?
- **Beta-convergence:** Does AR grow faster when it starts from a lower base?

Regression: `(1/T) × ln[y_i(T) / y_i(0)] = α + β × ln[y_i(0)] + ε_i`

Negative β = convergence. Run for (i) all major states and (ii) special category states only.

### 4.3 Fiscal Dependence Ratio (Linking Project 1 and Project 2)
`Fiscal Dependence Ratio = (Share in Central Taxes + Grants from Centre) / Total Revenue Receipts × 100`

Budget heads: `I.B: Share in Central Taxes` + `II.D: Grants from the Centre` / `Total: TOTAL REVENUE`

Plot this ratio from 1990-91 to 2026-27 after appending the official budget top-up. Also test: does higher transfer growth in year t predict higher GSDP growth in year t+1? (Transfer-growth nexus regression.)

### 4.4 Transfer-Inflation Nexus (Balassa-Samuelson Test)
Central transfers finance public sector wages → non-tradable price increases in AR. Test informally by plotting growth in central transfers against AR core inflation (non-food, non-fuel). Periods of large pay commission implementations (6th PC: 2008-09, 7th PC: 2016-17) should show AR core inflation spikes.

### 4.5 Inflation Premium Analysis
`Premium(t) = AP_inflation(t) − AllIndia_inflation(t)`

Compute for: Overall CPI, Food, Fuel, Core. Run one-sample t-tests (H₀: mean premium = 0) for each category.

Expected finding: food and fuel premiums positive and significant (supply-chain and transport cost premium of a landlocked frontier economy). Core premium depends on whether Balassa-Samuelson mechanism is operating.

---

## SECTION 5 — PROJECT 2 EXTENDED ANALYSIS

Beyond the four required indicators, Project 2 asks for interpretation of fiscal health and its relationship with the state's economic performance. The following additional analyses elevate the project:

### 5.1 Fiscal Sustainability Assessment
- **Debt sustainability:** Keep both deficit concepts visible. Use the official state-budget fiscal balance as the baseline and the broad PRS-style deficit as the sensitivity check.
- **Revenue mobilisation:** Own Tax Revenue / GSDP trend — has AR improved its own resource generation?
- **Expenditure quality:** Capital Outlay / Total Expenditure — what share of spending is capital formation vs. consumption?
- **Grant dependence:** Grants from Centre / Total Revenue over time (expected: very high and persistent).

### 5.2 The Revenue Surplus Paradox
AR's consistent and large revenue surplus (10–18% of GSDP) requires careful interpretation:
- Revenue surplus is NOT a sign of fiscal prudence in AR's case — it reflects massive central grants on the revenue account exceeding revenue expenditure.
- A better measure of fiscal health is **Own Revenue / Revenue Expenditure** — what fraction of expenditure can AR finance without central support?
- From the data: Own Tax Revenue + Own Non-Tax Revenue ≈ 3–5% of total revenue → AR cannot finance even 10% of its revenue expenditure from its own resources.
- This should be presented as the central interpretive finding of Project 2.

### 5.3 16th Finance Commission Context
The 16th Finance Commission is no longer just a future placeholder in this workspace. The PRS summary of the final report is now locally saved under `Data/Project2_Budget_Documents/`, and the key current takeaway is that Arunachal Pradesh's devolution share falls from **1.76** under the 15th Finance Commission to **1.35** under the 16th.

Use this in the paper as the policy hinge:
- current fiscal comfort is highly transfer-dependent,
- devolution is set to tighten relative to the previous award period, and
- the key question is whether own-resource mobilisation and structural transformation can offset that change.

### 5.4 FRBM Compliance
AR enacted its FRBM Act in 2006 (amended multiple times). Do not describe compliance as simple or automatic without specifying the deficit concept used.

- Under the **official state-budget presentation**, the latest deficits are small: about **1.6%** of GSDP in 2025-26 RE and **1.7%** in 2026-27 BE.
- Under the **broad PRS-style measure**, the latest deficits are much larger: **10.5%** and **11.0%** of GSDP.

This gap is the reason the Project 2 notebook now includes an explicit reconciliation module. The paper should treat official compliance as real within the state's budget framework, but also show that the underlying fiscal position is being stabilised by central capex loans and transfers rather than by a broad own-resource base.

---

## SECTION 6 — OUTPUT TABLES AND FIGURES

### Required Tables

**Table 1 — AR GSDP Trend Growth Rates by Regime (Kinked Exponential Model)**  
Columns: Period, β (growth coefficient), CAGR (%), Robust SE, t-statistic, n

**Table 2 — All-India vs AR: Growth Rate Comparison**  
Columns: Period, All-India CAGR (%), AR CAGR (%), Differential (%)

**Table 3 — Bai-Perron Structural Break Results**  
Columns: Series, No. of Breaks (BIC), Break Year 1 [95% CI], Break Year 2 [95% CI]

**Table 4 — Quarterly Inflation Rates: AR vs All-India (select years)**  
Both CPI-based and GSDP deflator-based

**Table 5 — Annual Headline and Core Inflation: AR vs All-India, 2011-12 to 2024-25**  
AR Rural CPI vs All-India Combined CPI; headline and core separately

**Table 6 — Inflation Premium Analysis**  
Columns: Category, Mean Premium (%), Std Dev, t-statistic, p-value, Significant?

**Table 7 — Project 2: Fiscal Indicators, Arunachal Pradesh, 2022-23 to 2026-27**  
Columns: Year, Revenue Balance/GSDP (%), Official Fiscal Balance/GSDP (%), Official Primary Balance/GSDP (%), Interest/RevExp (%), Figure Type, source note

**Table 8 — Extended Fiscal Analysis: 1990-91 to 2026-27**  
Columns: Year, Fiscal Dependence Ratio (%), Own Revenue/RevExp (%), Own Tax/Own Revenue (%), Capital Outlay/Total Expenditure (%), committed-expenditure snapshot where available

**Table 9 — Project 2 Deficit Reconciliation**  
Columns: Year, Broad Fiscal Deficit/GSDP (%), Official Fiscal Deficit/GSDP (%), Central Capex Loans (Cr)

**Table 10 — Project 2 Buoyancy Time-Series Diagnostics**  
Columns: Test, Series, Deterministic terms, test statistic, p-value, 5% decision

**Table 11 — Project 2 16th FC Transfer Trajectory**  
Columns: Year, tax devolution, annual FC local/disaster grants, revenue balance, revenue balance/GSDP

### Required Figures

**Figure 1:** Log GSDP — AR and All-India, 1950-51 to 2024-25, with break year vertical lines  
**Figure 2:** Sectoral shares in AR GSDP (Agriculture/Industry/Services) — stacked area, 1980-81 to 2024-25  
**Figure 3:** Quarterly CPI inflation — AR Rural vs All-India Combined, 2012 Q1 to latest  
**Figure 4:** Annual Headline vs Core Inflation — AR and All-India, bar chart 2011-12 to 2024-25  
**Figure 5:** Inflation premium by category — AR minus All-India (box plots or bar + CI)  
**Figure 6:** Fiscal dependence ratio — AR, long run with 2026-27 top-up  
**Figure 7:** Revenue balance, official fiscal balance, and official primary balance as % of GSDP — five-year Project 2 window  
**Figure 8:** Capital Outlay vs Interest Payments as % of Revenue Expenditure — long run with 2026-27 top-up  
**Figure 9:** Own Revenue / Revenue Expenditure — AR, long run with 2026-27 top-up  
**Figure 10:** Official vs broad fiscal-balance measures — Project 2 reconciliation figure  
**Figure 11:** Own revenue vs central transfers — five-year Project 2 window
**Figure 12:** Long-run four core fiscal indicators, 1990-91 to 2026-27  
**Figure 13:** Committed expenditure trajectory — salaries, pensions, interest as shares of revenue receipts  
**Figure 14:** Transfer breakdown — tax devolution, CSS grants, FC grants, other grants, own revenue  
**Figure 15:** Illustrative 16th FC transfer path, 2026-31

---

## SECTION 7 — CRITICAL DATA LIMITATIONS TO STATE IN PAPER

1. **AR GSDP pre-1987 is NEFA data.** Before February 20, 1987, Arunachal Pradesh was a centrally administered Union Territory (NEFA). Pre-1987 GSDP reflects central administration accounts, not a state government's independent economy.

2. **AR CPI is rural-only.** Urban CPI for AR does not exist — the Urban column is 100% NA across all items and all years. The Combined column contains values identical to Rural for approximately 8–10 sporadic observations in 2018 and 2020 only; these are not genuine combined indices. **Use only the Rural column for all AR CPI analysis.**

3. **AR CPI is group-level only.** Unlike All-India CPI with 28 sub-items, AR has only 6 group-level series. Core inflation for AR cannot be decomposed further into health, transport, education sub-categories. The agent's actual implementation used the **inclusion method** (Clothing+footwear + Miscellaneous) rather than the exclusion formula — this is acceptable given the group-level data constraint and should be documented clearly.

4. **AR CPI Housing item is absent.** No index and no rural weight. Core inflation for AR (inclusion method) therefore covers only Clothing+footwear (6.44%) and Miscellaneous (24.70%), totalling 31.14% of the basket — substantially narrower than All-India core.

5. **AR CPI 2020 data gap.** April and May 2020 values are missing across all items. Q1 FY 2020-21 CPI is based on June 2020 only. Annual averages for FY 2020-21 are based on 10 months. This affects 2020-21 annual inflation figures and year-on-year quarterly comparisons involving Q1 2020-21.

6. **Month encoding differs between files.** All-India CPI uses integer months (1–12). AR CPI uses text month names. Handle separately when assigning fiscal quarters.

7. **All-India CPI file has 4 extra unnamed columns.** Drop columns `Unnamed: 6` through `Unnamed: 9` when reading — these are empty artefacts from the Excel file structure.

8. **Denton interpolation introduces smoothing.** Quarterly GSDP estimates are derived, not observed. Sub-annual deflator movements should not be over-interpreted.

9. **Project 2 now uses a hybrid source design.** RBI State Finance Database remains the backbone; official 2026-27 budget documents supply the final-year top-up and replace projected-denominator logic.

10. **The official fiscal deficit and the broad PRS-style fiscal deficit are different concepts.** The analysis now reports both. Do not collapse them into one number in the paper.

10a. **Own-tax buoyancy must be caveated.** The log-log coefficient is high, about 1.69, and ADF tests reject unit roots with deterministic trend, but the Engle-Granger cointegration test does not reject no cointegration at 5 percent. Write the regression as a descriptive association, not as a settled causal long-run equilibrium.

10b. **Committed-expenditure salary data are not available for the full 1990-91 history at the same granularity.** Use the PRS/AFS trajectory for 2024-25 actual, 2025-26 BE, 2025-26 RE, and 2026-27 BE rather than imputing salaries for older years.

11. **1987-88 break not detected for AR.** The Bai-Perron procedure identified breaks at 1995-96 and 2013-14, not at the statehood year. This remains an empirical finding that must be reported and discussed.

---

## SECTION 8 — UNIFIED RESEARCH NARRATIVE

The two projects together constitute a unified analytical narrative about Arunachal Pradesh:

**The paradox of Arunachal Pradesh:** A frontier state that grows above the national average, shows strong headline fiscal ratios, and yet finances only about 17 to 19 percent of recent revenue expenditure from its own revenue base, has no deep industrial transformation, and carries persistent frontier-economy inflation pressure. In the final Project 2 paper this is quantified as average 2022-23 to 2026-27 revenue surplus of 15.9 percent of GSDP alongside average own-revenue financing of only 18.2 percent of revenue expenditure.

**Project 1 finding:** Growth is transfer-supported rather than productivity-led in a standard industrialization sense. The detected GSDP breaks are 1995-96 and 2013-14, not a clean statehood or liberalization break. Sectoral composition shows services-heavy expansion without deep industrial transformation.

**Project 2 finding:** Fiscal health is also transfer-fed. Revenue balance is large, but it sits on an own-resource base that remains weak. The paper should distinguish the official state-budget fiscal deficit from the broader PRS-style deficit, because the treatment of central capex loans changes the interpretation of FRBM compliance materially.

**The connecting thread:** Central transfers simultaneously support growth, services-heavy structural change, and headline fiscal strength. The 16th Finance Commission context now matters directly because Arunachal Pradesh's devolution share is set to decline from 1.76 to 1.35.

---

## SECTION 9 — ANALYSIS EXECUTION SEQUENCE

Execute analyses in this order:

1. Load and clean all data files; standardize year variables
2. Construct GSDP deflator (AR and All-India)
3. Run Denton-Cholette interpolation for quarterly AR GSDP
4. Prepare CPI data with fiscal quarter labels
5. Compute quarterly CPI inflation (AR and All-India)
6. Compute quarterly GSDP deflator inflation (AR)
7. Compute AR core CPI using the implemented inclusion method
8. Compute All-India core CPI using the implemented combined-core construction
9. Compute annual headline and core inflation, 2011-12 to 2024-25
10. Compute inflation premium by category; run t-tests
11. Construct log GSDP series with time trend
12. Run Bai-Perron structural break detection — All-India GDP
13. Run Bai-Perron structural break detection — AR GSDP
14. Test COVID intercept shift (separate from main break analysis)
15. Estimate kinked exponential growth rates — All-India
16. Estimate kinked exponential growth rates — AR
17. Compute sectoral composition by growth regime (AR)
18. Run convergence analysis (all states, then special category states)
19. Compute fiscal dependence ratio — AR, 1990-91 to 2026-27 with RBI backbone plus official top-up
20. Load the Project 2 budget-document manifest and reference-value top-up
21. Compute Project 2 fiscal indicators — four required ratios, five years, with source-status labels
22. Compute extended fiscal indicators and the official-versus-broad deficit reconciliation
23. Run own-tax buoyancy with ADF and Engle-Granger diagnostics
24. Build long-run core-indicator, committed-expenditure, transfer-breakdown, and 16th FC path figures
25. Run transfer-growth nexus regression if needed as a secondary extension
26. Generate all figures
27. Save all findings, tables, and figures to RESEARCH_FINDINGS.md

---

## SECTION 10 — OUTPUT FILE STRUCTURE

Save all outputs to `RESEARCH_FINDINGS.md`. Structure as follows:

```
# RESEARCH FINDINGS
## 1. Data Summary and Verification
## 2. Growth Analysis — All India
## 3. Growth Analysis — Arunachal Pradesh
## 4. Structural Break Results
## 5. Quarterly Inflation — CPI Based
## 6. Quarterly Inflation — GSDP Deflator Based
## 7. Annual Headline and Core Inflation (2011-12 to 2024-25)
## 8. Inflation Premium Analysis
## 9. Sectoral Decomposition
## 10. Convergence Analysis
## 11. Fiscal Dependence (Long Run)
## 12. Project 2 — Fiscal Health Indicators (Last 5 Years)
## 13. Extended Fiscal Analysis
## 14. Transfer-Growth Nexus
## 15. Summary of Findings
```

Each section: one or more markdown tables, one brief interpretation paragraph, any caveats.

Figures: save as high-resolution PNG (300 dpi, width 10 inches, height 6 inches) and embed paths in the markdown.

For regression outputs: report coefficient, robust standard error, t-statistic, p-value, R², n. For Bai-Perron: report break years, 95% confidence intervals, BIC values for 0 through m breaks.
