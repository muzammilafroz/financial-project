---
trigger: always_on
---

# Workspace Rules — Arunachal Pradesh Research Project

## Identity and Context
You are working on an economics research project in R. The project involves macroeconomic analysis of Arunachal Pradesh (AR), India. The primary guide document currently present in this workspace is `RESEARCH_AGENT_GUIDE_v2.md`. Read it fully before starting any analysis. The ongoing findings are in `RESEARCH_FINDINGS.md`.

## Notebook Rules

### File Format
- All work happens inside a single Jupyter Notebook file (`.ipynb`) using the **R kernel (IRkernel)**.
- Never create a `.R` script file as a substitute. Never use Python to edit the `.ipynb` programmatically.
- To add or edit cells, use the notebook's native cell API directly within the R kernel session.
- If a cell produces an error, fix it in that cell before moving forward. Do not skip cells.

### Cell Structure — Mandatory Pattern
Every logical unit of work must follow this exact 3-cell pattern:
1. **Markdown cell** — Section heading and one-line description of what the next code does
2. **Code cell** — The R code
3. **Output verification** — After the code runs, the agent must confirm the output looks correct before proceeding. If a data frame was loaded, print `head()`, `dim()`, and `str()` or `glimpse()`. If a regression was run, print `summary()`. If a chart was saved, confirm the file exists.

### Output Visibility — Non-Negotiable
After every single code cell that reads, transforms, or computes data:
- Print the first 6 rows of every data frame created or modified (`head()`)
- Print the dimensions (`dim()` or `nrow()` / `ncol()`)
- Print column names and types for any newly created data frame
- For numeric results (growth rates, inflation, fiscal ratios), print the actual numbers before saving them to the findings file
- For regression outputs, always print the full `summary()` and then separately print the `coeftest()` with robust SEs

This is not optional. If a step does not produce visible output, the agent must add an explicit print statement before moving on.

### Step-by-Step Execution
- Complete one section fully (all cells, verified outputs) before moving to the next.
- Follow the execution sequence in Section 9 of the guide exactly.
- After completing each of the 24 steps, append the results to `RESEARCH_FINDINGS.md` immediately — do not batch all writes to the end.

## Data Reading Rules

### All-India CPI
- Month column is **integer** (1–12). No text-to-number conversion needed.
- After reading, print: unique Month values, shape, and column names to confirm.

### Arunachal Pradesh CPI
- Month column is **text string** (e.g., "January"). Must be mapped to integer before fiscal quarter assignment.
- Urban column = 100% NA. Combined column = identical to Rural for ~8–10 sporadic values only. **Use only the Rural column.** Never use Urban or Combined for any AP CPI analysis.
- After reading, print non-null counts per column for each item to confirm.

### GSDP Files
- Row 3 is the header. Rows 1–2 are title rows. Skip them and assign row 3 as column names.
- Filter data rows using pattern match on Year column: must match `NNNN-NNNN` (four digits, hyphen, four digits).
- After reading and filtering, print: first row, last row, and total row count.

### State Finances
- After reading, confirm the year range: min and max of `Fiscal Year` column.
- When extracting any budget head, always print the resulting subset before computing ratios.

## Computation Rules

### Fiscal Quarter Assignment
- All-India: use numeric month directly — Q1 if month in c(4,5,6), Q2 if in c(7,8,9), Q3 if in c(10,11,12), Q4 if in c(1,2,3).
- AP: convert text month to numeric first using a named vector, then apply the same logic.
- Fiscal year = calendar year if month ≥ 4, else calendar year − 1.
- Always verify the assignment by printing a few rows showing the original month and derived fiscal quarter side-by-side.

### Core Inflation
- AR uses the **inclusion method**: Clothing+footwear (weight 6.44) and Miscellaneous (24.70), denominator 31.14.
- All-India uses the **inclusion method**: Clothing+footwear (rural 7.36, urban 5.57), Housing (urban only 21.67), Miscellaneous (rural 27.26, urban 29.53).
- After computing, print 5 rows of the resulting index alongside the underlying components to verify the weighted average is sensible.

### Structural Breaks
- Always plot BIC vs number of breaks before selecting the optimal model.
- Has 1987-88 came as one of the structural break under any BIC!
- Print the confint() output (95% CI) for all detected breaks.
- State explicitly in the notebook whether 1987-88 was or was not selected — this is a key finding.

### Robust Standard Errors
- All regression tables must use `coeftest()` with `vcovHC(model, type="HC1")`.
- Never report OLS standard errors alone. Always show both or HC1 only.

## Output Rules

### RESEARCH_FINDINGS.md
- Append to this file after each completed section, not at the end.
- Every table must be in GitHub-flavoured markdown format (pipe-separated, header separator row).
- Every figure reference must be in format `![Caption](figures/filename.png)`.
- Every section must include: the table, a one-paragraph interpretation, and any data caveats specific to that section.

### Figures
- Save to `figures/` subdirectory.
- Always 300 dpi, width = 10 inches, height = 6 inches, using `ggsave()`.
- Use `theme_bw()` for all ggplot2 charts.
- After saving, print the file path and confirm it exists with `file.exists()`.

## Error Handling
- If a package is not installed, install it with `install.packages()` before continuing.
- If a budget head is not found in State Finances, print the closest matching heads and stop — do not guess.
- If a CPI item name does not match exactly (semicolons vs commas, case differences), print the actual item names from the data and correct the code before proceeding.
- Never silently drop NA values. Always print how many NAs exist in any column before deciding how to handle them.
