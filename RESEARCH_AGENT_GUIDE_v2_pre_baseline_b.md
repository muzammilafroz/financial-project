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
| **[PROJECT 2] Revenue deficit / GSDP** | ✅ | State Finances + GSDP Current | GSDP for 2025-26 not in file |
| **[PROJECT 2] Fiscal deficit / GSDP** | ✅ | State Finances + GSDP Current | Same |
| **[PROJECT 2] Primary deficit / GSDP** | ✅ | Derived from Fiscal Deficit - Interest | Same |
| **[PROJECT 2] Interest / Revenue Expenditure** | ✅ | Both in Appendix-2 of State Finances | — |
| **[PROJECT 2] 2026-27 Budget data** | ❌ | Not in files | Must download from AR Finance Dept |

---

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
- 2024-25: **Revised** column (RE)
- 2025-26: **Budget** column (BE)
- 2026-27: Must download from AR Finance Department website — **not in the provided files**

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
**Definition (standard RBI):** CPI General Index excluding Food and Beverages (Group 1) and Fuel and Light (Group 5).

**Exclusion formula** (exact, using Laspeyres decomposition):
```
Core_Index = [w_total × General_Index − w_food × Food_Index − w_fuel × Fuel_Index] 
             / [w_total − w_food − w_fuel]
```

For **All-India Rural**: w_food = 54.18, w_fuel = 7.94, w_core = 37.88  
For **AR Rural**: w_food = 52.94, w_fuel = 9.78, w_core = 37.28

All-India weights are at sub-item level — can also compute core directly as a weighted average of non-food, non-fuel sub-items using their individual weights. Both methods should give the same result; the exclusion formula is simpler.

Annual inflation = compute annual average CPI from monthly values (12 months per fiscal year), then take year-on-year percentage change.

**Limitation for AR:** AR CPI is only at group level — cannot decompose core further into health, education, transport etc. AR core inflation = General Index minus Food and Beverages minus Fuel and Light, expressed as an index and then its year-on-year change.

Report for 2011-12 to 2023-24 as required.

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

This is directly available as: **`A: Surplus (+)/Deficit (-) on Revenue Account`**  
A **positive value = Revenue Surplus** (AR's case). A negative value = Revenue Deficit.  
Express as percentage of GSDP (current prices).

#### Fiscal Deficit
`Fiscal Surplus/Deficit = Revenue Account Balance + Capital Account Balance`

Directly available as: **`C: Overall Surplus (+)/Deficit (-) (A+B)`**  
Sign convention: positive = surplus, negative = deficit.  
Express as percentage of GSDP.

**Gross Fiscal Deficit (GFD)** = negative of C when C < 0 (standard positive presentation).

#### Primary Deficit
`Gross Primary Deficit = Gross Fiscal Deficit − Net Interest Payments`

Or equivalently: `Primary Balance = Overall Balance + Interest Payments`

Interest Payments available as: **`II.C.2: Interest Payments (i to iv)`** (Appendix-2, Non-Developmental Expenditure)

Primary Surplus/Deficit = `C + Interest_Payments`  
Express as percentage of GSDP.

#### Interest Expenditure as % of Revenue Expenditure
`Interest/RevExp ratio = [II.C.2: Interest Payments] / [Total: TOTAL EXPENDITURE (I+II+III)] × 100`

Both from Appendix-2. This measures the debt service burden on the revenue account.

### 2.6 Pre-computed Key Numbers (Verified from Data)

**AR GSDP at Current Prices (Rs Crore):**
| Year | GSDP (Cr) |
|------|-----------|
| 2020-21 | 30,525 |
| 2021-22 | 32,705 |
| 2022-23 | 35,712 |
| 2023-24 | 38,565 |
| 2024-25 | 44,229 |

**Project 2 Indicators — Best Available Figures (Account where available, else Revised, else Budget):**

| Year | Rev Surplus (Cr) | Overall Fiscal (Cr) | Interest (Cr) | RevExp (Cr) | Figure Type |
|------|-----------------|--------------------|--------------|--------------|----|
| 2021-22 | +5,385 | +1,064 | 778 | 15,847 | Account |
| 2022-23 | +6,370 | −281 | 835 | 17,418 | Account |
| 2023-24 | +6,877 | +3,110 | 858 | 20,564 | Account |
| 2024-25 | +7,210 | +1,281 | 948 | 26,337 | Revised |
| 2025-26 | +4,581 | +1,265 | 994 | 29,963 | Budget |

**Derived ratios (approximate, for verification):**

| Year | Rev Surplus/GSDP | Fiscal Surplus/GSDP | Interest/RevExp | Primary Surplus/GSDP |
|------|-----------------|--------------------|-----------------|--------------------|
| 2021-22 | +16.5% | +3.3% | 4.9% | +5.6% |
| 2022-23 | +17.8% | −0.8% | 4.8% | +1.6% |
| 2023-24 | +17.8% | +8.1% | 4.2% | +10.3% |
| 2024-25 | ~16.3% | ~2.9% | ~3.6% | ~5.0% |
| 2025-26 | ~10.4% | ~2.9% | ~3.3% | ~5.6% |

**CRITICAL ANALYTICAL FINDING:** AR consistently runs a **revenue surplus** of 10–18% of GSDP and even a **fiscal surplus** in most years. Interest burden is very low (3–5% of revenue expenditure). This is extraordinary — virtually no other Indian state achieves this. The explanation is that central grants flow in as revenue receipts, dwarfing revenue expenditure. Fiscal "health" indicators are therefore misleading for AR: they reflect **transfer dependency**, not fiscal self-sufficiency. This is the central finding of Project 2 and the link to Project 1's growth narrative.

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

### 3.3 Kinked Exponential Growth Model (Boyce 1986)
When breaks are identified at years T₁*, T₂*, ..., the kinked model is:

`ln GDP(t) = α + β₁·t + β₂·(t−T₁*)·D₁(t) + β₃·(t−T₂*)·D₂(t) + u(t)`

where D_i(t) = 1 if t > T_i*, else 0. This model is **continuous at break points** (kinked, not segmented) — the ln GDP series does not jump at breaks, only the growth rate changes. This is the correct specification for growth rate breaks vs. level shifts.

Growth rates by regime:
- Before T₁*: β₁
- Between T₁* and T₂*: β₁ + β₂
- After T₂*: β₁ + β₂ + β₃

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

Plot this ratio from 1990-91 to 2024-25. Also test: does higher transfer growth in year t predict higher GSDP growth in year t+1? (Transfer-growth nexus regression.)

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
- **Debt sustainability:** Fiscal deficit / GSDP over time (1990-91 to 2024-25 from State Finances).
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
The 16th Finance Commission (constituted 2024, recommendations for 2026-31) is the relevant reference document. Check:
- What fiscal norms has it recommended for special category states?
- How does AR's fiscal position compare with these norms?
- Are there recommendations on fiscal dependence reduction for NE states?

Note: The 16th FC report may not yet be publicly available (it is to submit recommendations by October 2025 for the period starting 2026-27). Check the 16th FC website. If unavailable, reference the 15th Finance Commission report and its recommendations for NE states, and note the pending status of the 16th FC.

### 5.4 FRBM Compliance
AR enacted its FRBM Act in 2006 (amended multiple times). The 3% fiscal deficit norm applies. Check compliance across the five project years. Given AR runs fiscal surpluses in most years, it is trivially FRBM-compliant — but note that this is due to transfers, not fiscal discipline.

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

**Table 5 — Annual Headline and Core Inflation: AR vs All-India, 2011-12 to 2023-24**  
AR Rural CPI vs All-India Combined CPI; headline and core separately

**Table 6 — Inflation Premium Analysis**  
Columns: Category, Mean Premium (%), Std Dev, t-statistic, p-value, Significant?

**Table 7 — Project 2: Fiscal Indicators, Arunachal Pradesh, 2021-22 to 2025-26**  
Columns: Year, Revenue Surplus/GSDP (%), Fiscal Surplus/GSDP (%), Primary Surplus/GSDP (%), Interest/RevExp (%), Figure Type (Account/RE/BE)

**Table 8 — Extended Fiscal Analysis: 1990-91 to 2024-25**  
Columns: Year, Fiscal Dependence Ratio (%), Own Revenue/RevExp (%), Capital Outlay/Total Expenditure (%), Fiscal Balance/GSDP (%)

**Table 9 — AR vs Other NE States: Fiscal Indicators Comparison (where data allows)**

### Required Figures

**Figure 1:** Log GSDP — AR and All-India, 1950-51 to 2024-25, with break year vertical lines  
**Figure 2:** Sectoral shares in AR GSDP (Agriculture/Industry/Services) — stacked area, 1980-81 to 2024-25  
**Figure 3:** Quarterly CPI inflation — AR Rural vs All-India Combined, 2012 Q1 to latest  
**Figure 4:** Annual Headline vs Core Inflation — AR and All-India, bar chart 2011-12 to 2023-24  
**Figure 5:** Inflation premium by category — AR minus All-India (box plots or bar + CI)  
**Figure 6:** Fiscal dependence ratio — AR, 1990-91 to 2024-25 (line chart)  
**Figure 7:** Revenue Surplus, Fiscal Balance, Primary Balance as % GSDP — three-line chart, all available years  
**Figure 8:** Capital Outlay vs Interest Payments as % of Revenue Expenditure — two axes, 1990-91 to 2024-25  
**Figure 9:** Own Revenue / Revenue Expenditure — AR, 1990-91 to 2024-25

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

9. **State Finances data uses Revised/Budget for 2024-25/2025-26.** Label clearly in all tables.

10. **GSDP for 2025-26 not available in files.** Use trend-based projection and label accordingly.

11. **1987-88 break not detected for AR.** The Bai-Perron procedure identified breaks at 1995-96 and 2013-14, not at the statehood year. This is an empirical finding that must be reported and discussed — it means statistically, the growth trajectory did not change at statehood, which has its own interpretation (transfers may have been rising smoothly rather than jumping at statehood).

---

## SECTION 8 — UNIFIED RESEARCH NARRATIVE

The two projects together constitute a unified analytical narrative about Arunachal Pradesh:

**The paradox of Arunachal Pradesh:** A frontier state that grows above the national average, runs consistent fiscal surpluses, and yet cannot finance even 10% of its own expenditure, has no meaningful industrial sector, carries one of India's highest inflation premiums, and remains absent from the Labour Bureau's industrial workforce tracking network.

**Project 1 finding:** Growth is transfer-fed, not productivity-driven. The dominant structural break in GSDP is likely 1987-88 (statehood) — an administrative event, not a market event. Sectoral composition shows rising public administration, stagnant agriculture, negligible industry. Structural transformation has not accompanied growth.

**Project 2 finding:** Fiscal health is also transfer-fed. Revenue surplus is large but illusory — it reflects massive central grants on the revenue account. Own revenue covers less than 10% of expenditure. The state is FRBM-compliant trivially, because it borrows minimally (it doesn't need to borrow when transfers are this large). Interest burden is low for the same reason.

**The connecting thread:** Central transfers simultaneously produce apparent growth (in GSDP) and apparent fiscal health (revenue surplus). Both are artefacts of the transfer-dependency structure. The 16th Finance Commission recommendations — whatever they are — will determine whether this structure continues or is reformed. This is the policy punchline.

---

## SECTION 9 — ANALYSIS EXECUTION SEQUENCE

Execute analyses in this order:

1. Load and clean all data files; standardize year variables
2. Construct GSDP deflator (AR and All-India)
3. Run Denton-Cholette interpolation for quarterly AR GSDP
4. Prepare CPI data with fiscal quarter labels
5. Compute quarterly CPI inflation (AR and All-India)
6. Compute quarterly GSDP deflator inflation (AR)
7. Compute AR core CPI using exclusion formula
8. Compute All-India core CPI using exclusion formula
9. Compute annual headline and core inflation, 2011-12 to 2023-24
10. Compute inflation premium by category; run t-tests
11. Construct log GSDP series with time trend
12. Run Bai-Perron structural break detection — All-India GDP
13. Run Bai-Perron structural break detection — AR GSDP
14. Test COVID intercept shift (separate from main break analysis)
15. Estimate kinked exponential growth rates — All-India
16. Estimate kinked exponential growth rates — AR
17. Compute sectoral composition by growth regime (AR)
18. Run convergence analysis (all states, then special category states)
19. Compute fiscal dependence ratio — AR, 1990-91 to 2024-25
20. Compute Project 2 fiscal indicators — four required ratios, five years
21. Compute extended fiscal indicators (Own Revenue/RevExp, Capital Outlay ratio)
22. Run transfer-growth nexus regression
23. Generate all figures
24. Save all findings, tables, and figures to RESEARCH_FINDINGS.md

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
## 7. Annual Headline and Core Inflation (2011-12 to 2023-24)
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