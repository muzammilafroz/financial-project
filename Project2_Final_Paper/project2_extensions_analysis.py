from __future__ import annotations

import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import adfuller, coint


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "Data"
TABLES = ROOT / "tables"
FIGURES = ROOT / "figures"

STATE_FIN_AR = DATA / "State Finances - Arunachal.XLSX"
STATE_FIN_ALL = DATA / "ALL STATES FINANCE DATABASE.XLSX"
GSDP_PANEL = DATA / "GSDP_NSDP_India_1960_2025_BackSeries.xlsx"
TOPUP = DATA / "Project2_Budget_Documents" / "project2_budget_reference_values.csv"

HEAD_TOTAL_REVENUE = "Total: TOTAL REVENUE (I+II)"
HEAD_OWN_TAX = "I.A: State's Own Tax Revenue (1 to 3)"
HEAD_OWN_NONTAX = "II.C: State's Own Non-Tax Revenue (1 to 6)"
HEAD_CENTRAL_TAXES = "I.B: Share in Central Taxes (i to ix)"
HEAD_GRANTS = "II.D: Grants from the Centre (1 to 7)"
HEAD_CSS_GRANTS = "II.D.3: Centrally Sponsored Schemes"
HEAD_FC_GRANTS = "II.D.5: Finance Commission Grants"
HEAD_ARTICLE_275_GRANTS = "II.D.6: Grants under proviso to Article 275(1) of the Constitution"
HEAD_OTHER_GRANTS = "II.D.7: Other Grants"
HEAD_REV_EXP = "Total: TOTAL EXPENDITURE (I+II+III)"
HEAD_INTEREST_EXP = "II.C.2: Interest Payments (i to iv)"
HEAD_CAP_OUTLAY = "I: Total Capital Outlay (1 + 2)"
HEAD_CAP_NET = "Total$: TOTAL CAPITAL DISBURSEMENTS (Excluding Public Accounts)"

COMPARATOR_STATES = [
    "Arunachal Pradesh",
    "Assam",
    "Sikkim",
    "Himachal Pradesh",
    "Tripura",
    "Meghalaya",
]

STATE_ABBR = {
    "Arunachal Pradesh": "AR",
    "Assam": "AS",
    "Sikkim": "SK",
    "Himachal Pradesh": "HP",
    "Tripura": "TR",
    "Meghalaya": "MG",
}

PRS_AR_BUDGET = DATA / "Project2_Budget_Documents" / "PRS_Arunachal_Budget_Analysis_2026_27.html"
PRS_16FC = DATA / "Project2_Budget_Documents" / "PRS_16th_Finance_Commission_Summary_2026_31.html"


def fiscal_start(series: pd.Series) -> pd.Series:
    return series.astype(str).str.slice(0, 4).astype(int)


def extract_head(
    df: pd.DataFrame,
    state_col: str,
    head: str,
    appendix: str | None = None,
    value_col: str = "Account",
    state: str | None = None,
) -> pd.DataFrame:
    mask = df["Budget Head"].eq(head)
    if appendix is not None:
        mask &= df["Appendix"].eq(appendix)
    if state is not None:
        mask &= df[state_col].eq(state)
    out = df.loc[mask, [state_col, "Fiscal Year", value_col]].copy()
    out["NumYear"] = fiscal_start(out["Fiscal Year"])
    out = out.rename(columns={value_col: head})
    return out


def ols_hc1(y: np.ndarray, x: np.ndarray) -> dict[str, float]:
    X = np.column_stack([np.ones(len(x)), x])
    beta = np.linalg.inv(X.T @ X) @ (X.T @ y)
    resid = y - X @ beta
    n, k = X.shape
    xtx_inv = np.linalg.inv(X.T @ X)
    meat = X.T @ np.diag(resid**2) @ X * n / (n - k)
    vcov = xtx_inv @ meat @ xtx_inv
    se = np.sqrt(np.diag(vcov))
    tstat = beta / se
    pval = 2 * (1 - 0.5 * (1 + np.vectorize(math.erf)(np.abs(tstat) / math.sqrt(2))))
    r2 = 1 - (resid @ resid) / ((y - y.mean()) @ (y - y.mean()))
    return {
        "intercept": beta[0],
        "slope": beta[1],
        "intercept_se_hc1": se[0],
        "slope_se_hc1": se[1],
        "intercept_t": tstat[0],
        "slope_t": tstat[1],
        "intercept_p_norm": pval[0],
        "slope_p_norm": pval[1],
        "r2": r2,
        "n": n,
    }


def load_gsdp_current() -> pd.DataFrame:
    gsdp = pd.read_excel(GSDP_PANEL, sheet_name="GSDP Curr (Rs Lakh)")
    long = gsdp.melt(id_vars="Year", var_name="State", value_name="GSDP_RsLakh")
    long = long.dropna(subset=["GSDP_RsLakh"]).copy()
    long["NumYear"] = fiscal_start(long["Year"])
    long["GSDP_Cr"] = long["GSDP_RsLakh"] / 100
    return long[["State", "Year", "NumYear", "GSDP_Cr"]]


def route1_tax_buoyancy(sf_ar: pd.DataFrame, gsdp_long: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    own_tax = extract_head(
        sf_ar,
        state_col="State",
        head=HEAD_OWN_TAX,
        appendix="Appendix-1",
        value_col="Account",
        state="Arunachal Pradesh",
    )
    own_tax = own_tax.rename(columns={HEAD_OWN_TAX: "OwnTax_Cr"})
    ar_gsdp = gsdp_long.loc[gsdp_long["State"].eq("Arunachal Pradesh"), ["NumYear", "Year", "GSDP_Cr"]]
    reg = own_tax.merge(ar_gsdp, on="NumYear", how="inner")
    reg = reg.loc[(reg["OwnTax_Cr"] > 0) & (reg["GSDP_Cr"] > 0) & (reg["NumYear"] <= 2023)].copy()
    reg["FiscalYear"] = reg["NumYear"].astype(str) + "-" + (reg["NumYear"] + 1).astype(str).str[-2:]
    reg["LogOwnTax"] = np.log(reg["OwnTax_Cr"])
    reg["LogGSDP"] = np.log(reg["GSDP_Cr"])
    reg["OwnTax_GSDP"] = reg["OwnTax_Cr"] / reg["GSDP_Cr"] * 100

    fit = ols_hc1(reg["LogOwnTax"].to_numpy(), reg["LogGSDP"].to_numpy())
    table = pd.DataFrame(
        [
            {
                "Variable": "log(GSDP)",
                "Coefficient": fit["slope"],
                "HC1_SE": fit["slope_se_hc1"],
                "t_stat": fit["slope_t"],
                "p_value_norm": fit["slope_p_norm"],
                "N": fit["n"],
                "R2": fit["r2"],
                "Sample": f"{reg['FiscalYear'].iloc[0]} to {reg['FiscalYear'].iloc[-1]}",
            },
            {
                "Variable": "Intercept",
                "Coefficient": fit["intercept"],
                "HC1_SE": fit["intercept_se_hc1"],
                "t_stat": fit["intercept_t"],
                "p_value_norm": fit["intercept_p_norm"],
                "N": fit["n"],
                "R2": fit["r2"],
                "Sample": f"{reg['FiscalYear'].iloc[0]} to {reg['FiscalYear'].iloc[-1]}",
            },
        ]
    )

    x_line = np.linspace(reg["LogGSDP"].min(), reg["LogGSDP"].max(), 100)
    y_line = fit["intercept"] + fit["slope"] * x_line
    plt.figure(figsize=(10, 6))
    plt.scatter(reg["LogGSDP"], reg["LogOwnTax"], color="#2f6f73", s=36)
    plt.plot(x_line, y_line, color="#b3432f", linewidth=2)
    plt.title("Own-tax buoyancy in Arunachal Pradesh")
    plt.xlabel("log current-price GSDP")
    plt.ylabel("log own tax revenue")
    plt.grid(True, alpha=0.25)
    plt.tight_layout()
    plt.savefig(FIGURES / "fig19_project2_tax_buoyancy.png", dpi=300)
    plt.close()
    return table, reg


def route2_fc_simulation() -> pd.DataFrame:
    top = pd.read_csv(TOPUP)
    base = top.loc[top["NumYear"].eq(2026)].iloc[0]
    central_taxes_after = 20665.0
    share_before = 1.76
    share_after = 1.35
    central_taxes_before = central_taxes_after * (share_before / share_after)
    full_loss = central_taxes_before - central_taxes_after

    rows = []
    for label, shock_frac in [
        ("No share cut: 15th FC share retained", 0.00),
        ("Half of share-loss shock", 0.50),
        ("Full 16th FC share-loss shock", 1.00),
        ("Stress: 125 percent of share-loss shock", 1.25),
    ]:
        loss = full_loss * shock_frac
        central_taxes = central_taxes_before - loss
        revenue_receipts = base["RevenueReceiptsCr"] + (central_taxes - central_taxes_after)
        revenue_balance = revenue_receipts - base["RevenueExpenditureCr"]
        broad_deficit = base["BroadFiscalDeficitCr"] + loss - full_loss
        official_deficit = base["OfficialFiscalDeficitCr"] + loss - full_loss
        rows.append(
            {
                "Scenario": label,
                "DevolutionSharePct": share_before - (share_before - share_after) * shock_frac,
                "CentralTaxDevolutionCr": central_taxes,
                "RevenueReceiptsCr": revenue_receipts,
                "RevenueBalanceCr": revenue_balance,
                "RevenueBalance_GSDP": revenue_balance / base["OfficialBudgetGSDPCr"] * 100,
                "OfficialFiscalDeficitCr": official_deficit,
                "OfficialFiscalDeficit_GSDP": official_deficit / base["OfficialBudgetGSDPCr"] * 100,
                "BroadFiscalDeficitCr": broad_deficit,
                "BroadFiscalDeficit_GSDP": broad_deficit / base["OfficialBudgetGSDPCr"] * 100,
                "RevenueLossVsNoCutCr": loss,
            }
        )
    sim = pd.DataFrame(rows)

    plot_df = sim.loc[sim["Scenario"].isin(["No share cut: 15th FC share retained", "Full 16th FC share-loss shock"])].copy()
    x = np.arange(len(plot_df))
    width = 0.36
    plt.figure(figsize=(10, 6))
    plt.bar(x - width / 2, plot_df["RevenueBalance_GSDP"], width, label="Revenue balance / GSDP", color="#2f6f73")
    plt.bar(x + width / 2, plot_df["OfficialFiscalDeficit_GSDP"], width, label="Official fiscal deficit / GSDP", color="#b3432f")
    plt.xticks(x, ["15th FC share retained", "16th FC share"], rotation=0)
    plt.ylabel("Percent of GSDP")
    plt.title("Fiscal effect of Arunachal Pradesh's devolution-share reduction")
    plt.axhline(0, color="black", linewidth=0.8)
    plt.legend()
    plt.grid(axis="y", alpha=0.25)
    plt.tight_layout()
    plt.savefig(FIGURES / "fig20_project2_transfer_shock.png", dpi=300)
    plt.close()
    return sim


def route3_cross_state(all_fin: pd.DataFrame, gsdp_long: pd.DataFrame) -> pd.DataFrame:
    frames = []
    for head, name, appendix in [
        (HEAD_TOTAL_REVENUE, "TotalRevenueCr", "Appendix-1"),
        (HEAD_CENTRAL_TAXES, "CentralTaxesCr", "Appendix-1"),
        (HEAD_GRANTS, "GrantsCr", "Appendix-1"),
        (HEAD_OWN_TAX, "OwnTaxCr", "Appendix-1"),
        (HEAD_OWN_NONTAX, "NonTaxCr", "Appendix-1"),
        (HEAD_REV_EXP, "RevenueExpenditureCr", "Appendix-2"),
        (HEAD_CAP_OUTLAY, "CapitalOutlayCr", "Appendix-4"),
        (HEAD_CAP_NET, "NetCapitalExpenditureCr", "Appendix-4"),
    ]:
        tmp = extract_head(all_fin, "State/UT", head, appendix=appendix, value_col="Account")
        tmp = tmp.rename(columns={"State/UT": "State", head: name})
        frames.append(tmp[["State", "Fiscal Year", "NumYear", name]])
    comp = frames[0]
    for tmp in frames[1:]:
        comp = comp.merge(tmp, on=["State", "Fiscal Year", "NumYear"], how="outer")
    comp = comp.loc[comp["State"].isin(COMPARATOR_STATES) & comp["NumYear"].eq(2023)].copy()
    comp["CentralTransfersCr"] = comp["CentralTaxesCr"] + comp["GrantsCr"]
    comp["OwnRevenueCr"] = comp["OwnTaxCr"] + comp["NonTaxCr"]
    comp["RevenueBalanceCr"] = comp["TotalRevenueCr"] - comp["RevenueExpenditureCr"]
    comp["FiscalDependenceRatio"] = comp["CentralTransfersCr"] / comp["TotalRevenueCr"] * 100
    comp["OwnRevenue_RevExp"] = comp["OwnRevenueCr"] / comp["RevenueExpenditureCr"] * 100
    comp["CapitalOutlayRatio"] = comp["CapitalOutlayCr"] / (comp["RevenueExpenditureCr"] + comp["NetCapitalExpenditureCr"]) * 100

    g = gsdp_long.loc[gsdp_long["NumYear"].eq(2023), ["State", "GSDP_Cr"]]
    comp = comp.merge(g, on="State", how="left")
    comp["RevenueBalance_GSDP"] = comp["RevenueBalanceCr"] / comp["GSDP_Cr"] * 100
    comp["StateCode"] = comp["State"].map(STATE_ABBR)
    comp["FiscalDependenceRank_desc"] = comp["FiscalDependenceRatio"].rank(ascending=False, method="min").astype(int)
    comp = comp.sort_values("FiscalDependenceRatio", ascending=False)

    x = np.arange(len(comp))
    width = 0.36
    plt.figure(figsize=(10, 6))
    plt.bar(x - width / 2, comp["FiscalDependenceRatio"], width, label="Central transfers / revenue", color="#2f6f73")
    plt.bar(x + width / 2, comp["OwnRevenue_RevExp"], width, label="Own revenue / revenue exp.", color="#b3432f")
    plt.xticks(x, comp["StateCode"])
    plt.ylabel("Percent")
    plt.title("Fiscal autonomy across comparator states, 2023-24 accounts")
    plt.legend()
    plt.grid(axis="y", alpha=0.25)
    plt.tight_layout()
    plt.savefig(FIGURES / "fig21_project2_cross_state_comparison.png", dpi=300)
    plt.close()
    return comp


def route4_longrun_core_indicators(sf_ar: pd.DataFrame, gsdp_long: pd.DataFrame) -> pd.DataFrame:
    frames = []
    for head, name, appendix in [
        (HEAD_TOTAL_REVENUE, "RevenueReceiptsCr", "Appendix-1"),
        (HEAD_REV_EXP, "RevenueExpenditureCr", "Appendix-2"),
        (HEAD_CAP_NET, "NetCapitalExpenditureCr", "Appendix-4"),
        (HEAD_INTEREST_EXP, "InterestPaymentsCr", "Appendix-2"),
    ]:
        tmp = extract_head(
            sf_ar,
            state_col="State",
            head=head,
            appendix=appendix,
            value_col="Account",
            state="Arunachal Pradesh",
        )
        tmp = tmp.rename(columns={head: name})
        frames.append(tmp[["Fiscal Year", "NumYear", name]])
    core = frames[0]
    for tmp in frames[1:]:
        core = core.merge(tmp, on=["Fiscal Year", "NumYear"], how="outer")
    core = core.loc[core["NumYear"] <= 2023].copy()
    ar_gsdp = gsdp_long.loc[gsdp_long["State"].eq("Arunachal Pradesh"), ["NumYear", "Year", "GSDP_Cr"]]
    core = core.merge(ar_gsdp, on="NumYear", how="inner")
    core["FY_label"] = core["NumYear"].astype(str) + "-" + (core["NumYear"] + 1).astype(str).str[-2:]
    core["SourceDoc"] = "RBI State Finances database and current-price GSDP workbook"
    core["RevenueBalanceCr"] = core["RevenueReceiptsCr"] - core["RevenueExpenditureCr"]
    core["BroadFiscalBalanceCr"] = core["RevenueReceiptsCr"] - (
        core["RevenueExpenditureCr"] + core["NetCapitalExpenditureCr"]
    )
    core["BroadPrimaryBalanceCr"] = core["BroadFiscalBalanceCr"] + core["InterestPaymentsCr"]

    top = pd.read_csv(TOPUP).loc[lambda d: d["NumYear"] >= 2024].copy()
    top = top.rename(columns={"OfficialBudgetGSDPCr": "GSDP_Cr"})
    top["SourceDoc"] = "Official Arunachal 2026-27 budget packet and PRS reconciliation"
    top_core = pd.DataFrame(
        {
            "Fiscal Year": top["FY_label"],
            "NumYear": top["NumYear"],
            "RevenueReceiptsCr": top["RevenueReceiptsCr"],
            "RevenueExpenditureCr": top["RevenueExpenditureCr"],
            "NetCapitalExpenditureCr": top["NetCapitalExpenditureCr"],
            "InterestPaymentsCr": top["InterestPaymentsCr"],
            "GSDP_Cr": top["GSDP_Cr"],
            "FY_label": top["FY_label"],
            "SourceDoc": top["SourceDoc"],
            "RevenueBalanceCr": top["RevenueBalanceCr"],
            "BroadFiscalBalanceCr": -top["BroadFiscalDeficitCr"],
            "BroadPrimaryBalanceCr": -top["BroadFiscalDeficitCr"] + top["InterestPaymentsCr"],
        }
    )
    core = pd.concat([core, top_core], ignore_index=True, sort=False).sort_values("NumYear")
    core["RevenueBalance_GSDP"] = core["RevenueBalanceCr"] / core["GSDP_Cr"] * 100
    core["BroadFiscalBalance_GSDP"] = core["BroadFiscalBalanceCr"] / core["GSDP_Cr"] * 100
    core["BroadPrimaryBalance_GSDP"] = core["BroadPrimaryBalanceCr"] / core["GSDP_Cr"] * 100
    core["Interest_RevExp"] = core["InterestPaymentsCr"] / core["RevenueExpenditureCr"] * 100

    plot_specs = [
        ("RevenueBalance_GSDP", "Revenue balance / GSDP"),
        ("BroadFiscalBalance_GSDP", "Broad fiscal balance / GSDP"),
        ("BroadPrimaryBalance_GSDP", "Broad primary balance / GSDP"),
        ("Interest_RevExp", "Interest / revenue expenditure"),
    ]
    fig, axes = plt.subplots(2, 2, figsize=(12, 8), sharex=True)
    for ax, (col, title) in zip(axes.ravel(), plot_specs):
        ax.plot(core["NumYear"], core[col], color="#2f6f73", linewidth=2)
        ax.axhline(0, color="black", linewidth=0.8, alpha=0.65)
        ax.set_title(title)
        ax.set_ylabel("Percent")
        ax.grid(True, alpha=0.25)
    axes[1, 0].set_xlabel("Fiscal year start")
    axes[1, 1].set_xlabel("Fiscal year start")
    fig.suptitle("Long-run fiscal structure of Arunachal Pradesh, 1990-91 to 2026-27", y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(FIGURES / "fig22_project2_longrun_core_indicators.png", dpi=300)
    plt.close()
    return core[
        [
            "FY_label",
            "NumYear",
            "SourceDoc",
            "GSDP_Cr",
            "RevenueBalance_GSDP",
            "BroadFiscalBalance_GSDP",
            "BroadPrimaryBalance_GSDP",
            "Interest_RevExp",
            "RevenueReceiptsCr",
            "RevenueExpenditureCr",
            "InterestPaymentsCr",
        ]
    ]


def route5_buoyancy_time_series_tests(reg_data: pd.DataFrame) -> pd.DataFrame:
    def adf_row(label: str, values: pd.Series, regression: str) -> dict[str, object]:
        stat, pvalue, used_lag, nobs, crit, _ = adfuller(values.dropna(), regression=regression, autolag="AIC")
        return {
            "Test": "ADF",
            "Series": label,
            "DeterministicTerms": regression,
            "TestStatistic": stat,
            "PValue": pvalue,
            "UsedLag": used_lag,
            "Nobs": nobs,
            "Critical_1pct": crit.get("1%"),
            "Critical_5pct": crit.get("5%"),
            "Critical_10pct": crit.get("10%"),
            "RejectAt5Pct": bool(stat < crit.get("5%")),
            "Interpretation": "Reject unit root at 5%" if stat < crit.get("5%") else "Do not reject unit root at 5%",
        }

    rows = [
        adf_row("log own tax revenue", reg_data["LogOwnTax"], "ct"),
        adf_row("log GSDP", reg_data["LogGSDP"], "ct"),
        adf_row("d.log own tax revenue", reg_data["LogOwnTax"].diff().dropna(), "c"),
        adf_row("d.log GSDP", reg_data["LogGSDP"].diff().dropna(), "c"),
    ]

    X = np.column_stack([np.ones(len(reg_data)), reg_data["LogGSDP"].to_numpy()])
    beta = np.linalg.inv(X.T @ X) @ (X.T @ reg_data["LogOwnTax"].to_numpy())
    resid = reg_data["LogOwnTax"].to_numpy() - X @ beta
    rows.append(adf_row("OLS residual from log own tax on log GSDP", pd.Series(resid), "n"))

    eg_stat, eg_pvalue, eg_crit = coint(
        reg_data["LogOwnTax"].to_numpy(),
        reg_data["LogGSDP"].to_numpy(),
        trend="c",
        autolag="aic",
    )
    rows.append(
        {
            "Test": "Engle-Granger",
            "Series": "log own tax revenue and log GSDP",
            "DeterministicTerms": "c",
            "TestStatistic": eg_stat,
            "PValue": eg_pvalue,
            "UsedLag": np.nan,
            "Nobs": len(reg_data),
            "Critical_1pct": eg_crit[0],
            "Critical_5pct": eg_crit[1],
            "Critical_10pct": eg_crit[2],
            "RejectAt5Pct": bool(eg_stat < eg_crit[1]),
            "Interpretation": "Reject no cointegration at 5%" if eg_stat < eg_crit[1] else "Do not reject no cointegration at 5%",
        }
    )
    return pd.DataFrame(rows)


def _budget_prs_table(index: int) -> pd.DataFrame:
    table = pd.read_html(PRS_AR_BUDGET)[index].copy()
    table.columns = table.iloc[0]
    return table.iloc[1:].reset_index(drop=True)


def _num(value: object) -> float:
    if pd.isna(value):
        return np.nan
    text = str(value).replace(",", "").replace("%", "").strip()
    if text in {"", "-", "NA", "nan"}:
        return np.nan
    return float(text)


def route6_committed_expenditure_trajectory() -> pd.DataFrame:
    committed = _budget_prs_table(5)
    receipts = _budget_prs_table(7)
    columns = ["2024-25 Actuals", "2025-26 Budgeted", "2025-26 Revised", "2026-27 Budgeted"]
    labels = ["2024-25 A", "2025-26 BE", "2025-26 RE", "2026-27 BE"]

    rows = []
    for col, label in zip(columns, labels):
        values = {
            str(row["Items"]): _num(row[col])
            for _, row in committed.iterrows()
            if str(row.get("Items", "")).strip()
        }
        rev_receipts = _num(receipts.loc[receipts["Items"].eq("Revenue Receipts"), col].iloc[0])
        row = {
            "Period": label,
            "SourceDoc": "PRS Arunachal Pradesh Budget Analysis 2026-27",
            "RevenueReceiptsCr": rev_receipts,
            "SalaryCr": values["Salaries"],
            "PensionCr": values["Pension"],
            "InterestCr": values["Interest payment"],
            "TotalCommittedCr": values["Total"],
        }
        row["Salary_RevReceipt"] = row["SalaryCr"] / rev_receipts * 100
        row["Pension_RevReceipt"] = row["PensionCr"] / rev_receipts * 100
        row["Interest_RevReceipt"] = row["InterestCr"] / rev_receipts * 100
        row["TotalCommitted_RevReceipt"] = row["TotalCommittedCr"] / rev_receipts * 100
        rows.append(row)
    out = pd.DataFrame(rows)

    x = np.arange(len(out))
    plt.figure(figsize=(10, 6))
    bottom = np.zeros(len(out))
    for col, label, color in [
        ("Salary_RevReceipt", "Salaries", "#2f6f73"),
        ("Pension_RevReceipt", "Pensions", "#b3432f"),
        ("Interest_RevReceipt", "Interest", "#6b6f8a"),
    ]:
        plt.bar(x, out[col], bottom=bottom, label=label, color=color)
        bottom += out[col].to_numpy()
    plt.plot(x, out["TotalCommitted_RevReceipt"], color="black", marker="o", linewidth=1.6, label="Total")
    plt.xticks(x, out["Period"])
    plt.ylabel("Percent of revenue receipts")
    plt.title("Committed expenditure pressure in Arunachal Pradesh")
    plt.legend()
    plt.grid(axis="y", alpha=0.25)
    plt.tight_layout()
    plt.savefig(FIGURES / "fig23_project2_committed_expenditure_trajectory.png", dpi=300)
    plt.close()
    return out


def route7_transfer_breakdown(sf_ar: pd.DataFrame) -> pd.DataFrame:
    def extract_optional(head: str, name: str, appendix: str = "Appendix-1") -> pd.DataFrame:
        if not sf_ar["Budget Head"].eq(head).any():
            return pd.DataFrame(columns=["NumYear", name])
        tmp = extract_head(
            sf_ar,
            state_col="State",
            head=head,
            appendix=appendix,
            value_col="Account",
            state="Arunachal Pradesh",
        )
        return tmp.rename(columns={head: name})[["NumYear", name]]

    heads = [
        (HEAD_TOTAL_REVENUE, "TotalRev", "Appendix-1"),
        (HEAD_CENTRAL_TAXES, "CentralTaxes", "Appendix-1"),
        (HEAD_GRANTS, "Grants", "Appendix-1"),
        (HEAD_OWN_TAX, "OwnTax", "Appendix-1"),
        (HEAD_OWN_NONTAX, "NonTax", "Appendix-1"),
        (HEAD_REV_EXP, "RevExp", "Appendix-2"),
        (HEAD_CSS_GRANTS, "CSSGrants", "Appendix-1"),
        (HEAD_FC_GRANTS, "FinanceCommissionGrants", "Appendix-1"),
        (HEAD_ARTICLE_275_GRANTS, "Article275Grants", "Appendix-1"),
        (HEAD_OTHER_GRANTS, "OtherGrants", "Appendix-1"),
    ]
    parts = [extract_optional(head, name, appendix) for head, name, appendix in heads]
    out = parts[0]
    for part in parts[1:]:
        out = out.merge(part, on="NumYear", how="outer")
    out = out.loc[out["NumYear"].isin([2022, 2023])].copy()
    out["SourceDoc"] = "RBI State Finances database accounts"

    official_rows = pd.DataFrame(
        [
            {
                "NumYear": 2024,
                "TotalRev": 30306.8496,
                "CentralTaxes": 22610.55,
                "Grants": 3828.6108,
                "OwnTax": 2820.0,
                "NonTax": 1048.0,
                "RevExp": 21710.0822,
                "CSSGrants": 3050.6081,
                "FinanceCommissionGrants": 408.5727,
                "Article275Grants": 100.3,
                "OtherGrants": 269.13,
                "SourceDoc": "Annual Financial Statement 2026-27 and PRS Budget Analysis",
            },
            {
                "NumYear": 2025,
                "TotalRev": 34124.88,
                "CentralTaxes": 24475.0,
                "Grants": 4971.97,
                "OwnTax": 3249.0,
                "NonTax": 1429.0,
                "RevExp": 27133.4891,
                "CSSGrants": 4027.97,
                "FinanceCommissionGrants": 644.0,
                "Article275Grants": 0.0,
                "OtherGrants": 300.0,
                "SourceDoc": "Annual Financial Statement 2026-27 and PRS Budget Analysis",
            },
            {
                "NumYear": 2026,
                "TotalRev": 30733.46,
                "CentralTaxes": 20665.0,
                "Grants": 4859.6,
                "OwnTax": 3634.0,
                "NonTax": 1574.0,
                "RevExp": 27061.6596,
                "CSSGrants": 4200.0,
                "FinanceCommissionGrants": 359.6,
                "Article275Grants": 0.0,
                "OtherGrants": 300.0,
                "SourceDoc": "Annual Financial Statement 2026-27 and PRS Budget Analysis",
            },
        ]
    )
    out = pd.concat([out, official_rows], ignore_index=True, sort=False).sort_values("NumYear")
    out[["Article275Grants", "OtherGrants", "CSSGrants", "FinanceCommissionGrants"]] = out[
        ["Article275Grants", "OtherGrants", "CSSGrants", "FinanceCommissionGrants"]
    ].fillna(0)
    out["OwnRev"] = out["OwnTax"] + out["NonTax"]
    out["OtherCentralGrants"] = out["Grants"] - out["CSSGrants"] - out["FinanceCommissionGrants"]
    out["OtherCentralGrants"] = out["OtherCentralGrants"].clip(lower=0)
    out["CentralTransfers"] = out["CentralTaxes"] + out["Grants"]
    out["FiscalDependenceRatio"] = out["CentralTransfers"] / out["TotalRev"] * 100
    out["OwnRev_RevReceipt"] = out["OwnRev"] / out["TotalRev"] * 100
    out["OwnRev_RevExp"] = out["OwnRev"] / out["RevExp"] * 100
    out["OwnTax_OwnRev"] = out["OwnTax"] / out["OwnRev"] * 100
    out["FY_label"] = out["NumYear"].astype(str) + "-" + (out["NumYear"] + 1).astype(str).str[-2:]

    x = np.arange(len(out))
    plt.figure(figsize=(11, 6))
    bottom = np.zeros(len(out))
    for col, label, color in [
        ("CentralTaxes", "Tax devolution", "#2f6f73"),
        ("CSSGrants", "CSS grants", "#b3432f"),
        ("FinanceCommissionGrants", "Finance Commission grants", "#6b6f8a"),
        ("OtherCentralGrants", "Other grants", "#c9a646"),
        ("OwnRev", "Own revenue", "#7b9e87"),
    ]:
        plt.bar(x, out[col], bottom=bottom, label=label, color=color)
        bottom += out[col].to_numpy()
    plt.xticks(x, out["FY_label"])
    plt.ylabel("Rs crore")
    plt.title("Composition of revenue receipts and central transfers")
    plt.legend(ncol=2)
    plt.grid(axis="y", alpha=0.25)
    plt.tight_layout()
    plt.savefig(FIGURES / "fig24_project2_transfer_breakdown.png", dpi=300)
    plt.close()
    return out


def route8_fc_transfer_trajectory() -> pd.DataFrame:
    shares = pd.read_html(PRS_16FC)[3].copy()
    shares.columns = shares.iloc[0]
    shares = shares.iloc[1:].reset_index(drop=True)
    ar_share = shares.loc[shares["State"].eq("Arunachal Pradesh")].iloc[0]

    grants = pd.read_html(PRS_16FC)[5].copy()
    ar_grants = grants.loc[grants.iloc[:, 0].eq("Arunachal Pradesh")].iloc[0]
    rural = sum(_num(ar_grants.iloc[i]) for i in [1, 2, 3])
    urban = sum(_num(ar_grants.iloc[i]) for i in [4, 5, 6])
    disaster = _num(ar_grants.iloc[7])
    total_grants_2026_31 = rural + urban + disaster
    annual_fc_grant = total_grants_2026_31 / 5

    top = pd.read_csv(TOPUP)
    base = top.loc[top["NumYear"].eq(2026)].iloc[0]
    base_non_fc_grants = 4859.6 - 359.6
    base_own_rev = 3634.0 + 1574.0
    base_rev_exp = base["RevenueExpenditureCr"]
    base_gsdp = base["OfficialBudgetGSDPCr"]
    nominal_devolution_growth = 0.08
    nominal_gsdp_growth = 0.08

    rows = []
    for i, year in enumerate(range(2026, 2031)):
        central_taxes = 20665.0 * ((1 + nominal_devolution_growth) ** i)
        own_rev = base_own_rev * ((1 + nominal_devolution_growth) ** i)
        non_fc_grants = base_non_fc_grants
        revenue_receipts = own_rev + central_taxes + non_fc_grants + annual_fc_grant
        revenue_exp = base_rev_exp * ((1 + nominal_devolution_growth) ** i)
        gsdp = base_gsdp * ((1 + nominal_gsdp_growth) ** i)
        rows.append(
            {
                "FY_label": f"{year}-{str(year + 1)[-2:]}",
                "NumYear": year,
                "Scenario": "Illustrative 8 pct nominal devolution and expenditure growth",
                "DevolutionShare_15FC": _num(ar_share["15th FC (2021-26)"]),
                "DevolutionShare_16FC": _num(ar_share["16th FC (2026-31)"]),
                "TaxDevolutionCr": central_taxes,
                "AnnualFCGrantCr": annual_fc_grant,
                "NonFCGrantsHeldAt2026Cr": non_fc_grants,
                "OwnRevenueCr": own_rev,
                "RevenueReceiptsCr": revenue_receipts,
                "RevenueExpenditureCr": revenue_exp,
                "RevenueBalanceCr": revenue_receipts - revenue_exp,
                "RevenueBalance_GSDP": (revenue_receipts - revenue_exp) / gsdp * 100,
                "FCGrantTotal2026_31Cr": total_grants_2026_31,
                "RuralLocalBodyGrant2026_31Cr": rural,
                "UrbanLocalBodyGrant2026_31Cr": urban,
                "DisasterGrant2026_31Cr": disaster,
            }
        )
    out = pd.DataFrame(rows)

    x = np.arange(len(out))
    width = 0.36
    plt.figure(figsize=(10, 6))
    plt.bar(x - width / 2, out["TaxDevolutionCr"], width, label="Tax devolution", color="#2f6f73")
    plt.bar(x + width / 2, out["AnnualFCGrantCr"], width, label="FC local/disaster grants", color="#b3432f")
    plt.plot(x, out["RevenueBalanceCr"], color="black", marker="o", linewidth=1.6, label="Revenue balance")
    plt.xticks(x, out["FY_label"])
    plt.ylabel("Rs crore")
    plt.title("Illustrative 16th Finance Commission transfer path")
    plt.legend()
    plt.grid(axis="y", alpha=0.25)
    plt.tight_layout()
    plt.savefig(FIGURES / "fig25_project2_16fc_transfer_trajectory.png", dpi=300)
    plt.close()
    return out


def diagnostics(sf_ar: pd.DataFrame, all_fin: pd.DataFrame, gsdp_long: pd.DataFrame) -> pd.DataFrame:
    checks = []
    account_years_ar = sf_ar.groupby("Fiscal Year")["Account"].apply(lambda s: s.notna().any())
    checks.append(
        {
            "Check": "Arunachal RBI account coverage",
            "Result": f"{account_years_ar[account_years_ar].index.min()} to {account_years_ar[account_years_ar].index.max()}",
            "Status": "PASS",
        }
    )
    for head in [HEAD_TOTAL_REVENUE, HEAD_OWN_TAX, HEAD_CENTRAL_TAXES, HEAD_GRANTS, HEAD_REV_EXP, HEAD_CAP_OUTLAY, HEAD_CAP_NET]:
        exists_ar = bool(sf_ar["Budget Head"].eq(head).any())
        exists_all = bool(all_fin["Budget Head"].eq(head).any())
        checks.append(
            {
                "Check": f"Budget head available: {head}",
                "Result": f"AR={exists_ar}; all-state={exists_all}",
                "Status": "PASS" if exists_ar and exists_all else "FAIL",
            }
        )
    top = pd.read_csv(TOPUP)
    g2026 = float(top.loc[top["NumYear"].eq(2026), "OfficialBudgetGSDPCr"].iloc[0])
    checks.append(
        {
            "Check": "2026-27 GSDP denominator",
            "Result": f"{g2026:.0f} crore; cross-checked against Budget at a Glance text value 41,314 crore",
            "Status": "PASS" if abs(g2026 - 41314) < 1e-6 else "REVIEW",
        }
    )
    gstates = set(gsdp_long.loc[gsdp_long["NumYear"].eq(2023), "State"])
    missing = [s for s in COMPARATOR_STATES if s not in gstates]
    checks.append(
        {
            "Check": "Comparator GSDP coverage for 2023-24",
            "Result": "missing=" + ",".join(missing) if missing else "all six states available",
            "Status": "PASS" if not missing else "FAIL",
        }
    )
    return pd.DataFrame(checks)


def main() -> None:
    TABLES.mkdir(exist_ok=True)
    FIGURES.mkdir(exist_ok=True)
    sf_ar = pd.read_excel(STATE_FIN_AR, sheet_name="Arunachal")
    all_fin = pd.read_excel(STATE_FIN_ALL, sheet_name="Data")
    gsdp_long = load_gsdp_current()

    reg_table, reg_data = route1_tax_buoyancy(sf_ar, gsdp_long)
    sim_table = route2_fc_simulation()
    cross_table = route3_cross_state(all_fin, gsdp_long)
    longrun_table = route4_longrun_core_indicators(sf_ar, gsdp_long)
    ts_tests_table = route5_buoyancy_time_series_tests(reg_data)
    committed_table = route6_committed_expenditure_trajectory()
    transfer_table = route7_transfer_breakdown(sf_ar)
    fc_path_table = route8_fc_transfer_trajectory()
    diag_table = diagnostics(sf_ar, all_fin, gsdp_long)

    reg_table.to_csv(TABLES / "table23_project2_tax_buoyancy_regression.csv", index=False)
    reg_data.to_csv(TABLES / "table23a_project2_tax_buoyancy_data.csv", index=False)
    sim_table.to_csv(TABLES / "table24_project2_16fc_simulation.csv", index=False)
    cross_table.to_csv(TABLES / "table25_project2_cross_state_comparison.csv", index=False)
    diag_table.to_csv(TABLES / "table26_project2_extension_diagnostics.csv", index=False)
    ts_tests_table.to_csv(TABLES / "table27_project2_buoyancy_time_series_tests.csv", index=False)
    longrun_table.to_csv(TABLES / "table28_project2_longrun_core_indicators.csv", index=False)
    committed_table.to_csv(TABLES / "table29_project2_committed_expenditure_trajectory.csv", index=False)
    transfer_table.to_csv(TABLES / "table30_project2_transfer_breakdown.csv", index=False)
    fc_path_table.to_csv(TABLES / "table31_project2_16fc_transfer_trajectory.csv", index=False)

    print("Saved extension tables and figures.")
    print(reg_table.to_string(index=False))
    print(ts_tests_table.to_string(index=False))
    print(sim_table.to_string(index=False))
    print(fc_path_table[["FY_label", "TaxDevolutionCr", "AnnualFCGrantCr", "RevenueBalanceCr", "RevenueBalance_GSDP"]].to_string(index=False))
    print(transfer_table[["FY_label", "FiscalDependenceRatio", "OwnRev_RevExp", "OwnTax_OwnRev", "CSSGrants", "FinanceCommissionGrants", "OtherCentralGrants"]].to_string(index=False))
    print(committed_table[["Period", "TotalCommitted_RevReceipt", "Salary_RevReceipt", "Pension_RevReceipt", "Interest_RevReceipt"]].to_string(index=False))
    print(cross_table[["StateCode", "State", "FiscalDependenceRatio", "OwnRevenue_RevExp", "RevenueBalance_GSDP", "CapitalOutlayRatio"]].to_string(index=False))
    print(diag_table.to_string(index=False))


if __name__ == "__main__":
    main()
