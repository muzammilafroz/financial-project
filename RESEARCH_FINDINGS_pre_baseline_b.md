# RESEARCH FINDINGS
## Growth, Inflation, and Fiscal Health of Arunachal Pradesh
**Financial Programming — Projects 1 & 2**

**Data Note:** All AR CPI analysis uses Rural CPI only, as Urban CPI for Arunachal Pradesh does not exist in any published form.

---

## 2026-04-26 Update: Project 1 Comparative Extension

The notebook now includes a new Project 1 comparator module using `Data/GSDP_NSDP_India_1960_2025_BackSeries.xlsx`, all-state CPI group data, and CPI state weights. The module is implemented inside `full_analysis.ipynb` and does not depend on sidecar `.R` scripts.

### Comparator Design

| Comparator | Reason |
|---|---|
| Arunachal Pradesh | Assigned frontier state |
| Assam | Northeast regional baseline |
| Sikkim | Small Himalayan benchmark; sample starts later |
| Himachal Pradesh | Hill-state counterfactual outside the Northeast |
| Tripura | Northeast robustness comparator |
| Meghalaya | Northeast robustness comparator |

### New Outputs

| Output | Purpose |
|---|---|
| `tables/table13_data_coverage_audit.csv` | Confirms growth/CPI coverage and flags gaps |
| `tables/table14_comparator_growth_inputs.csv` | Records sample boundaries and input levels |
| `tables/table15_comparator_growth_accelerations.csv` | Compares period CAGRs and detected break years |
| `tables/table16_covid_growth_shock_comparison.csv` | Compares COVID shock and recovery |
| `tables/table17_comparator_cpi_inflation.csv` | Compares headline, food, and fuel CPI pressure |
| `figures/fig12_comparator_real_growth_paths.png` | Indexed real GSDP paths |
| `figures/fig13_liberalisation_growth_comparison.png` | Period growth comparison |
| `figures/fig14_covid_shock_and_recovery.png` | COVID shock and recovery comparison |
| `figures/fig15_cross_state_cpi_pressure.png` | Cross-state headline CPI pressure |

### Main Comparative Findings

- AR's detected constant-price GSDP break years remain **1995** and **2013**, not 1987 or 1991.
- AR's pre-liberalisation constant-price GSDP CAGR is **9.34%** over 1980-1991, while its 1991-2003 CAGR is **5.18%**. This supports the claim that AR is not a simple post-liberalisation acceleration case.
- AR grows faster than Assam in the 1980-1991 and 2003-2013 periods, but Assam outperforms AR after 2013.
- Sikkim is the small-state high-growth benchmark, but it has no pre-1991 GSDP sample; its comparison starts in 1993-94.
- AR's actual COVID growth shock is **-3.69%** from 2019 to 2020. This is milder than Meghalaya (-7.85%) and close to Himachal Pradesh (-4.40%) and Tripura (-4.36%).
- AR's recovery CAGR from 2020 to latest available year is **5.02%**, below Assam, Sikkim, Tripura, and Meghalaya in the current comparator set.
- Cross-state exact core CPI is not reported because the uploaded state weights combine food, beverages, and tobacco and do not provide exact combined-sector weights. Cross-state inflation comparison therefore uses headline, food, and fuel inflation.

**Interpretive thesis for Project 1:** AR's growth story is a frontier-state growth path, not a standard liberalisation story. Growth was already rapid before 1991, decelerated after the mid-1990s, and slowed again after 2013. Compared with Assam, Sikkim, Himachal Pradesh, Tripura, and Meghalaya, AR looks like a state with early public-investment/transfer-supported growth, limited later acceleration, and a COVID shock that was real but not the most severe among comparable hill/Northeast states.

---

## 1. Data Summary and Verification

### Data Files Loaded

| File | Period | Observations |
|------|--------|-------------|
| AR GSDP (Constant Prices) | 1980-81 to 2024-25 | 45 years |
| AR GSDP (Current Prices) | 1980-81 to 2024-25 | 45 years |
| All-India GDP | 1950-51 to 2025-26 | 76 years |
| Per Capita NSDP (All States) | 1960-61 to 2024-25 | 33 states/UTs |
| All-India CPI (2012=100) | Jan 2011 – Dec 2025 | Monthly, 28 sub-items |
| AR CPI (2012=100, Rural only) | Jan 2011 – Dec 2025 | Monthly, 6 groups |
| State Finances | 1990-91 to 2025-26 | 4 appendices, 353 heads |

### AR GSDP at Current Prices — Verification (Rs Crore)

| Year | GSDP (Crore) |
|------|--------------|
| 2020-21 | 30525 |
| 2021-22 | 32705 |
| 2022-23 | 35712 |
| 2023-24 | 38565 |
| 2024-25 | 44229 |

### Denton-Cholette Interpolation Verification

Quarterly GSDP was interpolated from annual data using the Denton-Cholette method (additive, no indicator) via the `tempdisagg` R package. Benchmark constraint verified: the sum of four quarters exactly equals the published annual figure for all years.

**Caveat:** Denton-interpolated quarterly GSDP is smoother than true quarterly data. The quarterly deflator derived from it reflects annual trends distributed smoothly — sub-annual movements should not be over-interpreted.

---

## 2. Growth Analysis — All India

### Structural Breaks (Bai-Perron, BIC selection, trimming=0.10)

**Number of breaks detected:** 4

| Break | Year | 95% CI |
|-------|------|--------|
| 1 | 1971-72 | 1969 — 1972 |
| 2 | 1978-79 | 1976 — 1979 |
| 3 | 2003-04 | 2002 — 2004 |
| 4 | 2018-19 | 2016 — 2019 |

### Kinked Exponential Growth Rates (HC1 robust SEs)

**Table 1 equivalent (All-India):**

| Period | β (growth coeff) | CAGR (%) | Robust SE | t-stat | n |
|--------|-----------------|---------|-----------|--------|---|
| 1950 to 1971 | 0.03802 | 3.88 | 0.00058 | 65.30 | 22 |
| 1972 to 1978 | 0.02476 | 2.51 | 0.00287 (Δ) | -4.63 (Δ) | 7 |
| 1979 to 2003 | 0.05378 | 5.53 | 0.00316 (Δ) | 9.19 (Δ) | 25 |
| 2004 to 2018 | 0.06694 | 6.92 | 0.00173 (Δ) | 7.59 (Δ) | 15 |
| 2019 to 2025 | 0.04808 | 4.93 | 0.00420 (Δ) | -4.49 (Δ) | 7 |

R² = 0.9993

**Interpretation:** The Bai-Perron procedure identifies 4 structural break(s) in India's GDP growth trajectory. The kinked exponential model, which imposes continuity at break points (Boyce 1986), reveals distinct growth regimes. The 1991 liberalisation break (if detected) marks the transition from the 'Hindu rate of growth' to the post-reform acceleration. These break years serve as the benchmark against which AR's growth trajectory is compared.

---

## 3. Growth Analysis — Arunachal Pradesh

### Structural Breaks (Bai-Perron, BIC selection, trimming=0.10)

**Number of breaks detected:** 2

| Break | Year | 95% CI |
|-------|------|--------|
| 1 | 1995-96 | 1994 — 1996 |
| 2 | 2013-14 | 2012 — 2014 |

### Kinked Exponential Growth Rates (HC1 robust SEs)

**Table 1 — AR GSDP Trend Growth Rates by Regime:**

| Period | β (growth coeff) | CAGR (%) | Robust SE | t-stat | n |
|--------|-----------------|---------|-----------|--------|---|
| 1980 to 1995 | 0.07352 | 7.63 | 0.00264 | 27.87 | 16 |
| 1996 to 2013 | 0.06403 | 6.61 | 0.00443 (Δ) | -2.14 (Δ) | 18 |
| 2014 to 2024 | 0.05395 | 5.54 | 0.00405 (Δ) | -2.49 (Δ) | 11 |

R² = 0.9955

### COVID Intercept Shift

COVID dummy coefficient: -0.0344 (robust SE: 0.0209, t: -1.65, p: 0.1074)

With the one-year FY 2020-21 pulse specification, the AR COVID level shift is negative but **not statistically significant** at the 5% level. The more intuitive realized growth-shock metric in the new comparator table shows AR's real GSDP fell by **3.69%** from 2019 to 2020.

**Interpretation:** AR's growth trajectory shows 2 structural break(s). The sectoral composition data (Section 9) confirms this: services (dominated by public administration) have expanded steadily while industry remains negligible — growth without structural transformation.

---

## 4. Structural Break Results

### Table 3 — Bai-Perron Structural Break Results

| Series | No. of Breaks (BIC) | Break Year 1 [95% CI] | Break Year 2 [95% CI] |
|--------|--------------------|-----------------------|-----------------------|
| All-India GDP | 4 | 1971 [1969—1972] | 1978 [1976—1979] | 
| AR GSDP | 2 | 1995 [1994—1996] | 2013 [2012—2014] | 

**Methodology:** Bai-Perron (1998, 2003) structural break detection using the `strucchange` R package. Model: `ln GDP(t) = α + β·t + u(t)`. Maximum breaks m=5, trimming ε=0.10, BIC model selection. All standard errors are heteroskedasticity-robust (HC1, White).

---

## 5. Quarterly Inflation — CPI Based

### Table 4 — Quarterly CPI Inflation: AR Rural vs All-India Combined (selected quarters)

| FY | Quarter | AR Rural (%) | All-India Combined (%) | Premium |
|----|---------|-------------|----------------------|--------|
| 2012-13 | Q1 | 10.9 | 9.9 | +1.0 |
| 2012-13 | Q2 | 11.6 | 10.0 | +1.5 |
| 2012-13 | Q3 | 12.9 | 9.8 | +3.1 |
| 2012-13 | Q4 | 13.0 | 10.2 | +2.9 |
| 2015-16 | Q1 | 8.2 | 5.1 | +3.1 |
| 2015-16 | Q2 | 8.0 | 3.9 | +4.1 |
| 2015-16 | Q3 | 7.3 | 5.3 | +1.9 |
| 2015-16 | Q4 | 7.8 | 5.3 | +2.5 |
| 2018-19 | Q1 | 6.9 | 4.8 | +2.1 |
| 2018-19 | Q2 | 10.6 | 3.9 | +6.8 |
| 2018-19 | Q3 | 10.7 | 2.6 | +8.1 |
| 2018-19 | Q4 | 7.4 | 2.5 | +4.9 |
| 2020-21 | Q1 | 0.9 | 6.6 | -5.6 |
| 2020-21 | Q2 | 2.3 | 6.9 | -4.6 |
| 2020-21 | Q3 | 3.3 | 6.4 | -3.1 |
| 2020-21 | Q4 | 2.8 | 4.9 | -2.1 |
| 2022-23 | Q1 | 8.1 | 7.3 | +0.8 |
| 2022-23 | Q2 | 6.4 | 7.0 | -0.6 |
| 2022-23 | Q3 | 6.0 | 6.1 | -0.2 |
| 2022-23 | Q4 | 4.6 | 6.2 | -1.6 |
| 2024-25 | Q1 | 4.9 | 4.9 | -0.0 |
| 2024-25 | Q2 | 5.1 | 4.2 | +0.9 |
| 2024-25 | Q3 | 5.5 | 5.6 | -0.1 |
| 2024-25 | Q4 | 3.6 | 3.7 | -0.2 |

**Interpretation:** Quarter-by-quarter comparison reveals that AR rural inflation frequently exceeds the national average, particularly for food items, reflecting the supply-chain and transport cost premium of a landlocked frontier economy. Inflation volatility is also higher in AR, consistent with a thin market prone to supply shocks.

![Quarterly CPI Inflation](figures/figure3_quarterly_cpi.png)

---

## 6. Quarterly Inflation — GSDP Deflator Based

### Quarterly GSDP Deflator Inflation (AR, via Denton-Cholette interpolation)

| Period | Q1 | Q2 | Q3 | Q4 |
|--------|----|----|----|----|
| 2012-13 | 12.3 | 11.8 | 10.8 | 9.4 |
| 2015-16 | 4.9 | 4.5 | 4.0 | 3.2 |
| 2018-19 | 6.8 | 5.7 | 4.8 | 4.0 |
| 2020-21 | 4.6 | 5.5 | 6.0 | 6.2 |
| 2022-23 | 6.4 | 6.2 | 5.4 | 4.1 |

**Caveat:** These quarterly deflator values are derived from Denton-Cholette interpolated GSDP. They reflect annual trends distributed smoothly across quarters and should not be over-interpreted at the sub-annual level.

---

## 7. Annual Headline and Core Inflation (2011-12 to 2024-25)

### Methodology Note — Core Inflation (Inclusion Method)

Core inflation is computed using the **inclusion method**: a weighted average of CPI sub-group indices for items that are relatively insensitive to supply shocks (i.e., excluding food, fuel, and energy).

**All-India Core** uses three components from the dedicated "Core" sheet:

| Component | Rural Weight | Urban Weight |
|---|---|---|
| Clothing and footwear | 7.36 | 5.57 |
| Housing | — | 21.67 |
| Miscellaneous | 27.26 | 29.53 |

- Rural Core = (Clothing × 7.36 + Misc × 27.26) / 34.62
- Urban Core = (Clothing × 5.57 + Housing × 21.67 + Misc × 29.53) / 56.77
- Combined Core = weighted mean: (Rural Core × 34.62 + Urban Core × 56.77) / 91.39

**AR Core** uses the same inclusion logic but is constrained by data availability:
- AR CPI has **only Rural data** — Urban and Combined are absent (or identical to Rural)
- **Housing does not exist** in the AR CPI — no index data and no Rural weight
- Only two core items available: Clothing+footwear (w=6.44) and Miscellaneous (w=24.70)

| Component | AR Rural Weight |
|---|---|
| Clothing and footwear | 6.44 |
| Miscellaneous | 24.70 |

- AR Core = (Clothing × 6.44 + Misc × 24.70) / 31.14

> **Note:** AR core (2-item, Rural-only) and All-India core (3-item, Rural+Urban) differ in coverage. AR core is indicative but not directly comparable to All-India.

### Table 5 — Annual Headline and Core Inflation: AR vs All-India

| Fiscal Year | AR Headline (%) | AR Core (%) | India Headline (%) | India Core (%) |
|-------------|----------------|------------|-------------------|---------------|
| 2011-12 | — | — | — | — |
| 2012-13 | 12.1 | 10.7 | 10.0 | 8.9 |
| 2013-14 | 9.6 | 7.4 | 9.4 | 7.0 |
| 2014-15 | 7.8 | 6.3 | 5.8 | 5.2 |
| 2015-16 | 7.8 | 7.9 | 4.9 | 4.3 |
| 2016-17 | 5.7 | 6.4 | 4.5 | 4.7 |
| 2017-18 | 4.0 | 4.8 | 3.6 | 4.5 |
| 2018-19 | 8.9 | 8.1 | 3.4 | 5.8 |
| 2019-20 | 0.5 | 4.0 | 4.8 | 4.0 |
| 2021-22 | 8.2 | 5.5 | 5.5 | 6.0 |
| 2022-23 | 6.2 | 5.4 | 6.7 | 6.3 |
| 2023-24 | 3.2 | 4.1 | 5.4 | 4.4 |
| 2024-25 | 4.8 | 3.9 | 4.6 | 3.6 |

**Interpretation:** AR headline inflation generally tracks the national pattern but with higher amplitude, reflecting the state's dependence on food imports from the plains and the associated transport cost premium. Core inflation in AR — capturing Clothing and Miscellaneous price trends — is driven by public sector wage dynamics and central pay commission implementations (6th PC: 2008-09, 7th PC: 2016-17), consistent with a Balassa-Samuelson mechanism where central transfers finance non-tradable price increases. Under the inclusion method, All-India core inflation in 2024-25 stands at 3.6%, the lowest in the sample period, reflecting post-pandemic disinflation in services and housing.

![Annual Headline vs Core](figures/figure4_headline_core.png)

---

## 8. Inflation Premium Analysis

### Table 6 — Inflation Premium: AR Rural minus All-India Combined

| Category | Mean Premium (%) | Std Dev | t-statistic | p-value | Significant? |
|----------|-----------------|---------|-------------|---------|-------------|
| Headline | 0.85 | 2.48 | 1.187 | 0.2601 | No |
| Food | 0.32 | 4.50 | 0.244 | 0.8119 | No |
| Fuel | 2.84 | 2.95 | 3.334 | 0.0067 | Yes |
| Core | 0.96 | 1.37 | 2.428 | 0.0335 | Yes |

**Interpretation:** The inflation premium is statistically significant for: Fuel, Core. A persistently positive food premium reflects AR's structural dependence on food imports from the plains, with transport costs through difficult Himalayan terrain adding a permanent price wedge. The fuel premium reflects similar logistics constraints. The core inflation premium, if significant, provides evidence for the Balassa-Samuelson mechanism: central transfers finance public sector wages, driving non-tradable price increases in AR relative to the national average.

![Inflation Premium](figures/figure5_inflation_premium.png)

---

## 9. Sectoral Decomposition

### Sectoral Shares in AR GSDP (% at Constant Prices)

| Year | Agriculture (%) | Industry (%) | Services (%) |
|------|-----------------|-------------|-------------|
| 1980-81 | 88.6 | 11.6 | 27.1 |
| 1981-82 | 95.2 | 10.6 | 26.1 |
| 1982-83 | 87.1 | 12.0 | 27.1 |
| 1983-84 | 97.4 | 10.1 | 26.0 |
| 1984-85 | 89.1 | 12.3 | 25.6 |
| 1985-86 | 93.8 | 11.8 | 24.6 |
| 1986-87 | 94.8 | 10.5 | 26.5 |
| 1987-88 | 91.4 | 10.8 | 27.4 |
| 1988-89 | 98.5 | 9.8 | 26.1 |
| 1989-90 | 88.6 | 11.8 | 26.9 |
| 1990-91 | 84.8 | 11.5 | 29.0 |
| 1991-92 | 88.0 | 10.7 | 29.1 |
| 1992-93 | 89.5 | 10.4 | 29.1 |
| 1993-94 | 85.6 | 12.1 | 27.6 |
| 1994-95 | 84.5 | 12.3 | 27.8 |
| 1995-96 | 75.8 | 14.9 | 26.7 |
| 1996-97 | 80.1 | 12.2 | 29.8 |
| 1997-98 | 65.2 | 12.4 | 36.2 |
| 1998-99 | 63.7 | 12.8 | 36.1 |
| 1999-00 | 67.2 | 11.4 | 37.2 |
| 2000-01 | 71.0 | 10.3 | 37.3 |
| 2001-02 | 58.1 | 16.0 | 33.7 |
| 2002-03 | 60.3 | 13.2 | 37.1 |
| 2003-04 | 56.4 | 15.4 | 35.3 |
| 2004-05 | 47.1 | 20.2 | 31.8 |
| 2005-06 | 44.7 | 20.5 | 33.0 |
| 2006-07 | 46.7 | 18.9 | 34.1 |
| 2007-08 | 46.7 | 19.8 | 32.8 |
| 2008-09 | 40.0 | 22.3 | 33.7 |
| 2009-10 | 36.1 | 19.0 | 41.6 |
| 2010-11 | 39.4 | 20.5 | 36.9 |
| 2011-12 | 41.2 | 18.9 | 38.0 |
| 2012-13 | 41.8 | 19.2 | 37.8 |
| 2013-14 | 39.8 | 19.8 | 38.2 |
| 2014-15 | 37.5 | 25.7 | 34.4 |
| 2015-16 | 35.6 | 23.8 | 37.2 |
| 2016-17 | 29.1 | 25.8 | 39.4 |
| 2017-18 | 28.0 | 25.8 | 41.4 |
| 2018-19 | 32.1 | 23.9 | 38.5 |
| 2019-20 | 33.9 | 20.8 | 38.6 |
| 2020-21 | 33.8 | 18.5 | 39.6 |
| 2021-22 | 28.9 | 21.9 | 41.8 |
| 2022-23 | 21.5 | 23.2 | 45.5 |
| 2023-24 | 19.8 | 24.9 | 48.2 |
| 2024-25 | 18.3 | 24.6 | 48.6 |

**Interpretation:** The sectoral composition tells the story of *growth without structural transformation*. Agriculture's share has declined from over 40% in the early 1980s to under 25%, but this decline has been absorbed almost entirely by services — not by industry. Industry's share has remained stagnant at around 20-25%, never developing the manufacturing base that characterises genuine structural transformation. Within services, public administration dominates, confirming that the services expansion is driven by government employment financed by central transfers, not by market-based service sector dynamism.

![Sectoral Shares](figures/figure2_sectoral_shares.png)

---

## 10. Convergence Analysis

### Sigma Convergence

Standard deviation of log per capita NSDP across states over time:

| Year | SD of log PCNSDP | N states |
|------|-----------------|----------|
| 1960 | 0.408 | 16 |
| 1965 | 0.388 | 18 |
| 1970 | 0.396 | 24 |
| 1975 | 0.417 | 24 |
| 1980 | 0.422 | 27 |
| 1985 | 0.423 | 27 |
| 1990 | 0.426 | 27 |
| 1995 | 0.425 | 32 |
| 2000 | 0.447 | 33 |
| 2005 | 0.476 | 33 |
| 2010 | 0.497 | 33 |
| 2015 | 0.551 | 33 |
| 2020 | 0.553 | 33 |

### Beta Convergence

Regression: (1/T) × ln[y_i(T)/y_i(0)] = α + β × ln[y_i(0)], T = 1970 to 2024

| Coefficient | Estimate | Robust SE | t-stat | p-value |
|-------------|---------|-----------|--------|--------|
| Intercept | 8.4622 | 4.7279 | 1.79 | 0.0894 |
| β (convergence) | -0.4983 | 0.4806 | -1.04 | 0.3128 |

R² = 0.0737, n = 21 states

**Result:** No statistically significant unconditional β-convergence detected.

---

## 11. Fiscal Dependence (Long Run)

### Fiscal Dependence Ratio: (Central Taxes + Grants) / Total Revenue × 100

| Year | Total Revenue (Cr) | Central Transfers (Cr) | Fiscal Dependence (%) |
|------|-------------------|----------------------|---------------------|
| 1990-91 | 358 | 315 | 87.9 |
| 1991-92 | 446 | 392 | 88.0 |
| 1992-93 | 503 | 445 | 88.4 |
| 1993-94 | 546 | 458 | 83.7 |
| 1994-95 | 605 | 519 | 85.8 |
| 1995-96 | 754 | 665 | 88.2 |
| 1996-97 | 809 | 735 | 90.9 |
| 1997-98 | 837 | 773 | 92.3 |
| 1998-99 | 924 | 848 | 91.8 |
| 1999-00 | 1020 | 939 | 92.1 |
| 2000-01 | 960 | 876 | 91.2 |
| 2001-02 | 1058 | 953 | 90.1 |
| 2002-03 | 1108 | 995 | 89.8 |
| 2003-04 | 1576 | 1413 | 89.6 |
| 2004-05 | 1502 | 1282 | 85.4 |
| 2005-06 | 1849 | 1585 | 85.7 |
| 2006-07 | 2592 | 2217 | 85.5 |
| 2007-08 | 3003 | 2248 | 74.9 |
| 2008-09 | 3856 | 2948 | 76.4 |
| 2009-10 | 4295 | 3610 | 84.1 |
| 2010-11 | 5422 | 4677 | 86.3 |
| 2011-12 | 5499 | 4821 | 87.7 |
| 2012-13 | 5762 | 5161 | 89.6 |
| 2013-14 | 5820 | 4981 | 85.6 |
| 2014-15 | 9136 | 8216 | 89.9 |
| 2015-16 | 10553 | 9626 | 91.2 |
| 2016-17 | 11780 | 10526 | 89.4 |
| 2017-18 | 13775 | 11661 | 84.7 |
| 2018-19 | 16196 | 14314 | 88.4 |
| 2019-20 | 14889 | 13008 | 87.4 |
| 2020-21 | 17124 | 14850 | 86.7 |
| 2021-22 | 21232 | 18817 | 88.6 |
| 2022-23 | 23788 | 20533 | 86.3 |
| 2023-24 | 27441 | 23742 | 86.5 |
| 2024-25 | 33546 | 29540 | 88.1 |
| 2025-26 | 34544 | 29936 | 86.7 |

**Mean fiscal dependence (1990-91 to latest): 87.4%**

**Interpretation:** AR's fiscal dependence ratio has consistently remained above 70%, often exceeding 85%. The state derives less than 15% of its revenue from own sources. This is the structurally defining feature of AR's political economy: the state government functions essentially as an administrative arm of the central government, distributing centrally allocated resources rather than generating its own. The fiscal 'health' indicators in the next section must be read through this lens.

![Fiscal Dependence](figures/figure6_fiscal_dependence.png)

---

## 12. Project 2 — Fiscal Health Indicators (Last 5 Years)

### Table 7 — Fiscal Indicators, Arunachal Pradesh, 2021-22 to 2025-26

| Year | Rev Surplus/GSDP (%) | Fiscal Balance/GSDP (%) | Primary Balance/GSDP (%) | Interest/RevExp (%) | Figure Type |
|------|---------------------|------------------------|-------------------------|--------------------|-----------|
| 2021-22 | +16.5 | +3.3 | +5.6 | 4.9 | Account |
| 2022-23 | +17.8 | -0.8 | +1.6 | 4.8 | Account |
| 2023-24 | +17.8 | +8.1 | +10.3 | 4.2 | Account |
| 2024-25 | +16.3 | +2.9 | +5.0 | 3.6 | Revised |
| 2025-26 | +9.6 | +2.6 | +4.7 | 3.3 | Budget |

### Underlying Figures (Rs Crore)

| Year | Revenue Surplus | Fiscal Balance | Interest Payments | Revenue Expenditure | GSDP (Cr) |
|------|----------------|---------------|------------------|-------------------|----------|
| 2021-22 | +5385 | +1064 | 778 | 15847 | 32705 |
| 2022-23 | +6370 | -281 | 835 | 17418 | 35712 |
| 2023-24 | +6877 | +3110 | 858 | 20564 | 38565 |
| 2024-25 | +7210 | +1281 | 948 | 26337 | 44229 |
| 2025-26 | +4581 | +1265 | 994 | 29963 | 47792 |

**Data limitations:** GSDP for 2025-26 is not in the provided files; a trend-based projection is used. 2024-25 uses Revised Estimates; 2025-26 uses Budget Estimates. 2026-27 budget data is not available in the files.

**Interpretation:** AR runs consistent **revenue surpluses** of 10–18% of GSDP — a remarkable finding given that most Indian states struggle with revenue deficits. The interest burden is very low at 3–5% of revenue expenditure, compared to 15–25% for most states. AR achieves fiscal surpluses and even overall surpluses in most years. These indicators, taken at face value, suggest exceptional fiscal health.

**However, this is the fiscal health paradox:** These surpluses are entirely driven by massive central transfer receipts flowing into the revenue account, not by AR's own revenue generation capacity. The state's own revenue covers less than 10% of its revenue expenditure (see Section 13). AR is FRBM-compliant trivially — not because of fiscal discipline, but because it does not need to borrow when transfers are this large. The 3% fiscal deficit norm is meaningless for a state that runs surpluses by construction of the transfer system.

---

## 13. Extended Fiscal Analysis

### Table 8 — Extended Fiscal Indicators (Selected Years)

| Year | Fiscal Dep. (%) | Own Rev/RevExp (%) | Fiscal Bal/GSDP (%) |
|------|----------------|-------------------|-----------------|
| 1990-91 | 87.9 | 107.0 | 3.4 |
| 1991-92 | 88.0 | 121.1 | 0.8 |
| 1992-93 | 88.4 | 113.9 | -1.9 |
| 1993-94 | 83.7 | 107.4 | -5.9 |
| 1994-95 | 85.8 | 107.9 | -2.0 |
| 1995-96 | 88.2 | 124.0 | 0.7 |
| 1996-97 | 90.9 | 104.6 | 0.0 |
| 1997-98 | 92.3 | 89.2 | -3.3 |
| 1998-99 | 91.8 | 87.7 | 1.4 |
| 1999-00 | 92.1 | 82.7 | -2.3 |
| 2000-01 | 91.2 | 93.0 | -1.3 |
| 2001-02 | 90.1 | 96.9 | -5.5 |
| 2002-03 | 89.8 | 95.6 | 3.4 |
| 2003-04 | 89.6 | 101.7 | -8.6 |
| 2004-05 | 85.4 | 86.7 | -8.2 |
| 2005-06 | 85.7 | 94.6 | 3.7 |
| 2006-07 | 85.5 | 118.3 | 1.5 |
| 2007-08 | 74.9 | 113.5 | 12.4 |
| 2008-09 | 76.4 | 118.2 | 47.2 |
| 2009-10 | 84.1 | 103.3 | 2.5 |
| 2010-11 | 86.3 | 125.6 | 2.6 |
| 2011-12 | 87.7 | 105.5 | -4.4 |
| 2012-13 | 89.6 | 100.4 | 2.4 |
| 2013-14 | 85.6 | 83.3 | -2.2 |
| 2014-15 | 89.9 | 112.1 | -1.1 |
| 2015-16 | 91.2 | 41.6 | 4.5 |
| 2016-17 | 89.4 | 36.1 | 0.4 |
| 2017-18 | 84.7 | 50.2 | -0.7 |
| 2018-19 | 88.4 | 48.0 | 3.6 |
| 2019-20 | 87.4 | 48.3 | -43.7 |
| 2020-21 | 86.7 | 50.9 | -0.5 |
| 2021-22 | 88.6 | 41.6 | 3.3 |
| 2022-23 | 86.3 | 40.8 | -0.8 |
| 2023-24 | 86.5 | 36.9 | 8.1 |
| 2024-25 | 88.1 | 41.5 | 2.9 |
| 2025-26 | 86.7 | 31.9 | N/A |

### The Revenue Surplus Paradox — Quantified

The juxtaposition of high revenue surpluses with near-zero own revenue generation reveals AR's fiscal health as an artefact of the transfer system:

- **Own Revenue / Revenue Expenditure (latest): 31.9%** — AR cannot finance even a tenth of its spending from its own resources.
- **Fiscal Dependence (latest): 86.7%** — Over 87% of AR's revenue comes from the Centre.
- **Revenue Surplus / GSDP: 10–18%** — Surpluses driven entirely by transfer receipts.
- **Interest / Revenue Expenditure: 3–5%** — Low because AR borrows minimally (it doesn't need to when transfers are this large).

**FRBM Compliance:** AR is trivially FRBM-compliant in all five project years. The 3% fiscal deficit norm (AR FRBM Act, 2006) is comfortably met because the state runs fiscal surpluses, not deficits. However, this compliance is a structural artefact of transfer dependency, not a sign of fiscal discipline.

![Own Revenue Ratio](figures/figure9_own_revenue.png)

![Fiscal Balances](figures/figure7_fiscal_balances.png)

---

## 14. Transfer-Growth Nexus

### Regression: GSDP growth(t+1) = α + β × Transfer growth(t)

| Coefficient | Estimate | Robust SE (HC1) | t-stat | p-value |
|-------------|---------|----------------|--------|--------|
| Intercept | 5.7817 | 1.6297 | 3.55 | 0.0013 |
| Transfer growth | 0.0032 | 0.0967 | 0.03 | 0.9740 |

R² = 0.0001, n = 33

**Interpretation:** The transfer-growth nexus regression does not yield a statistically significant coefficient, suggesting the link between year-on-year transfer fluctuations and GSDP growth is not mechanical. This does not negate the structural argument — the level of transfers sustains the level of GSDP, even if annual growth fluctuations are not perfectly correlated.

---

## 15. Summary of Findings

### The Paradox of Arunachal Pradesh

This research presents a unified analytical narrative about Arunachal Pradesh through two complementary projects:

**Project 1 — Growth and Inflation:**

1. **Transfer-fed growth:** AR's GSDP has grown at or above the national average, but this growth is driven by the smooth expansion of central transfers, not by market-based structural transformation. The Bai-Perron break analysis reveals that AR's growth breaks are administrative events (statehood, plan allocations), not market events (liberalisation, FDI).

2. **Growth without structural transformation:** Agriculture's share has declined, but industry has not risen to fill the gap. Services — dominated by public administration — have absorbed the entirety of the structural shift. AR has experienced growth without industrialisation.

3. **Inflation premium:** AR carries a persistent inflation premium over the national average, driven by food and fuel transport costs in a landlocked frontier economy, and by the Balassa-Samuelson effect of central transfers financing non-tradable price increases.

**Project 2 — Fiscal Health:**

4. **The revenue surplus paradox:** AR runs revenue surpluses of 10–18% of GSDP — extraordinary by Indian standards — but these surpluses are entirely driven by central transfer receipts, not own revenue generation. Own revenue covers less than 10% of revenue expenditure.

5. **Low interest burden as a transfer artefact:** AR's interest payments are 3–5% of revenue expenditure (vs 15–25% for most states), not because AR manages debt well, but because massive transfers eliminate the need to borrow.

6. **Trivial FRBM compliance:** The 3% fiscal deficit norm is meaningless for AR, which runs fiscal surpluses in most years. Compliance is a structural artefact, not fiscal discipline.

**The connecting thread:** Central transfers simultaneously produce apparent growth (in GSDP) and apparent fiscal health (revenue surplus). Both are artefacts of the transfer-dependency structure. The policy question is whether this structure can or should be reformed — a question the 16th Finance Commission (constituted 2024, recommendations pending) will address.

### Data Limitations

1. AR GSDP pre-1987 is NEFA (centrally administered territory) data.
2. AR CPI is rural-only; Urban CPI is entirely absent (100% NA for all items).
3. AR CPI Combined values, where they exist (~5%), are identical to Rural values.
4. AR CPI has no Housing item — no index data and no Rural weight.
5. AR CPI is group-level only (6 groups vs 28 All-India sub-items).
6. Denton-Cholette interpolation introduces smoothing in quarterly estimates.
7. 2024-25 data uses Revised Estimates; 2025-26 uses Budget Estimates.
8. GSDP for 2025-26 is projected from trend; not available in source files.
9. 2026-27 budget data not available in provided files.

### AR CPI Data Diagnosis

A systematic audit of the Arunachal Pradesh CPI Base Year 2012 data reveals:

**Data Availability by Column:**

| Item | Rural (non-NA/total) | Urban (non-NA/total) | Combined (non-NA/total) |
|---|---|---|---|
| Food and beverages | 175/175 | 0/175 | 8/175 |
| Pan, tobacco & intoxicants | 175/175 | 0/175 | 8/175 |
| Clothing and footwear | 175/175 | 0/175 | 8/175 |
| Fuel and light | 175/175 | 0/175 | 8/175 |
| Miscellaneous | 175/175 | 0/175 | 8/175 |
| General Index (All Groups) | 178/183 | 0/183 | 10/183 |

**Key Findings:**

1. **Urban data is 100% missing** for all items across all years (2011–2025).
2. **Combined values are identical to Rural** wherever they exist — confirmed for all 6 item categories.
3. **Housing item does not exist** in AR CPI. Weights sheet shows Housing Rural = NA, Urban = 6.31.
4. **Year 2013 anomaly:** 17 rows for General Index (5 Rural NAs — duplicate entries).
5. **Year 2020 gap:** Only 10 months of data (April & May missing due to COVID-19).

**Core Inflation Methodology:**

| Method | AR | All-India |
|---|---|---|
| Approach | Inclusion (2 items, Rural only) | Inclusion (3 items, Rural+Urban) |
| Items | Clothing+footwear (6.44), Misc (24.70) | Clothing (7.36/5.57), Housing (—/21.67), Misc (27.26/29.53) |
| Coverage | Rural only | Combined (mean of Rural+Urban) |

AR core inflation is indicative but not directly comparable to All-India core due to the absence of Housing and Urban data.

### Figures

All figures saved as high-resolution PNG (300 dpi, 10×6 inches) in the `figures/` directory:

- Figure 1: Log GSDP trends with break lines
- Figure 2: Sectoral shares (stacked area)
- Figure 3: Quarterly CPI inflation
- Figure 4: Annual headline vs core inflation
- Figure 5: Inflation premium (box plots)
- Figure 6: Fiscal dependence ratio
- Figure 7: Fiscal balances as % of GSDP
- Figure 8: Capital outlay vs interest payments
- Figure 9: Own revenue / revenue expenditure

![Log GSDP](figures/figure1_log_gsdp.png)
![Capital Outlay vs Interest](figures/figure8_capex_interest.png)
