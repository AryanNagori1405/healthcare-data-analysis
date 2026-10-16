# Healthcare Data Analysis

A reusable Python + SQL project that cleans a real healthcare dataset with pandas, loads it into **MySQL** and **PostgreSQL**, and answers ten analytical questions with SQL. Built with clean functional design (6 documented functions), a full data-cleaning pipeline, 10 SQL reports (including 2 window functions), and 12 pytest tests at **100% coverage**.

**Dataset:** a 55,500-row healthcare admissions dataset (15 columns) from Kaggle — cleaned down to 54,966 rows after removing duplicates.

---

## 1. What it does

```
Raw CSV (55,500 rows)
        │
        ▼
  CSVLoader / load_data          ──► pandas DataFrame
        │
        ▼
  clean_data                     ──► 54,966 rows, types fixed, text standardized
        │
        ▼
  save_cleaned_data              ──► data/healthcare_cleaned.csv
        │
        ▼
  + Duration_Days                ──► data/healthcare_for_db.csv
        │
        ▼
  MySQL  +  PostgreSQL           ──► table `healthcare`
        │
        ▼
  10 SQL reports                 ──► admissions, costs, diagnoses, rankings, running total
```

The whole pipeline is driven by a handful of reusable functions plus a set of SQL scripts. Load the CSV, clean it, import it into either database, and run any of the ten queries.

---

## 2. The six functions (design first)

All cleaning and loading logic lives in `src/data_processing.py` as six small, single-purpose functions.

| Function | One-line responsibility |
|---|---|
| `load_data(filepath)` | Read a CSV into a DataFrame, failing loudly if the file is missing. |
| `check_missing_values(df)` | Return the count of nulls per column. |
| `check_duplicates(df)` | Return the number of duplicate rows. |
| `clean_data(df)` | Standardize text, fix types, and remove duplicates — in the right order. |
| `save_cleaned_data(df, path)` | Write a DataFrame to CSV, creating the folder if needed. |
| `load_and_clean(in, out)` | End-to-end: load → clean → optionally save. |

**Why keep them separate and small?**

- **`load_data`** is the only place that reads from disk and the only place that decides what "missing file" means. Every other function receives an in-memory DataFrame, so they never touch the filesystem — which is what makes them trivial to unit-test.
- **`check_missing_values` / `check_duplicates`** are pure, read-only diagnostics. They are the first thing you run on a new dataset and they never mutate anything, so they are safe to call anywhere.
- **`clean_data`** is the only place that knows the dataset's rules: which columns are text (and should be `strip()` + `title()`-cased), which are dates (`DD-MM-YYYY`), and which are numeric. **Order matters here** — it standardizes text *before* de-duplicating, so that rows which differ only in casing (e.g. `male` vs `MALE`) are correctly recognized as duplicates and removed. Getting this order wrong silently keeps duplicates, which is exactly the kind of bug the tests catch.
- **`save_cleaned_data`** is the only place that knows about output files, and it creates parent directories automatically so nested paths just work.
- **`load_and_clean`** is the convenience wrapper that reads as the pipeline: load, clean, save.

Because every function takes a plain DataFrame (not a connection, not a path), each one is unit-testable in isolation — which is why the whole suite runs with temporary files and no database.

---

## 3. Project structure

```
HealthcareDataAnalysis/
├── data/
│   ├── healthcare_cleaned.csv        # cleaned dataset (54,966 rows)
│   └── healthcare_for_db.csv         # + Duration_Days, ready for the databases
├── notebooks/
│   └── data_exploration.ipynb        # exploratory analysis
├── src/
│   └── data_processing.py            # the 6 functions
├── sql/
│   ├── create_tables.sql             # PostgreSQL schema (SERIAL)
│   ├── create_tables_mysql.sql       # MySQL schema (AUTO_INCREMENT)
│   └── queries.sql                   # the 10 SQL reports
├── tests/
│   ├── __init__.py
│   └── test_data_processing.py       # 12 pytest tests
├── cleaning_analysis.md              # data cleaning report
├── db_import.py                      # database import helper
├── make_report.py                    # generates PROJECT_REPORT.pdf
├── PROJECT_REPORT.pdf                # 14-section project report
└── README.md                         # this file
```

---

## 4. Setup

**Prerequisites:** Python 3.10+ and (for the database section) MySQL 8.x and/or PostgreSQL 14+.

Run these from the project root. On Windows, always call tools through the interpreter (`python -m pip`, `python -m pytest`) to avoid broken `pip.exe` shims.

**Step 1 — install dependencies**

```bash
python -m pip install pandas mysql-connector-python sqlalchemy psycopg2-binary pytest pytest-cov
```

**Step 2 — (optional) re-clean the data from the raw CSV**

```python
from src.data_processing import load_and_clean
load_and_clean("path/to/healthcare_dataset.csv", "data/healthcare_cleaned.csv")
```

**Step 3 — create the databases and tables**

```sql
-- MySQL
CREATE DATABASE healthcare_db;
USE healthcare_db;
-- then run sql/create_tables_mysql.sql

-- PostgreSQL
CREATE DATABASE healthcare_db;
-- then run sql/create_tables.sql
```

**Step 4 — import the cleaned data**

Load `data/healthcare_for_db.csv` into the `healthcare` table using `LOAD DATA` (MySQL), `\copy` (PostgreSQL), or the helper in `db_import.py`. Verify with:

```sql
SELECT COUNT(*) FROM healthcare;   -- expect 54,966
```

**Step 5 — run the reports**

```bash
mysql -u root -p healthcare_db < sql/queries.sql
# or
psql -U postgres -d healthcare_db -f sql/queries.sql
```

### Windows troubleshooting

- **`Fatal error in launcher: Unable to create process ... pip.exe`** — the pip shim points at the wrong Python. Use `python -m pip install ...` instead.
- **`ModuleNotFoundError: No module named 'src'`** — set the project root on the path: `$env:PYTHONPATH="C:\Users\aryan\HealthcareDataAnalysis"`.

---

## 5. Data cleaning

The raw dataset had three real quality problems. Each fix is documented in `cleaning_analysis.md` with the number of rows affected.

| Issue | Fix | Rows affected |
|---|---|---|
| 534 duplicate rows | `drop_duplicates()` (applied *after* text cleanup) | 534 removed |
| Inconsistent text casing (`Bobby JacksOn`, `MALE`, …) | `str.strip().str.title()` on 10 text columns | all rows (formatting only) |
| Dates stored as strings, billing as generic objects | `pd.to_datetime(..., '%d-%m-%Y')`, `pd.to_numeric(...)` | all rows |

A derived column, `Duration_Days = Discharge Date − Date of Admission`, is added when producing the database file, enabling length-of-stay analysis.

**Result:** 55,500 → **54,966 rows**, all 15 columns correctly typed, zero missing values.

---

## 6. The ten SQL reports

All ten queries live in `sql/queries.sql` and run on both MySQL and PostgreSQL. Together they cover joins, `GROUP BY`, aggregation, and the two required window functions (`RANK()` and a running total).

| # | Report | What it answers |
|---|---|---|
| 1 | Admissions per month | Billing total + admission count per `YYYY-MM`. |
| 2 | Average cost per condition | `AVG(billing_amount)` and case count per medical condition. |
| 3 | Top 5 most common diagnoses | The five conditions with the most cases. |
| 4 | Billing by insurance provider | Claims, total and average billing per insurer. |
| 5 | Average length of stay by condition | `AVG(duration_days)` per condition. |
| 6 | Admissions by admission type | Counts + average cost for Elective / Emergency / Urgent. |
| 7 | Top 10 doctors | Busiest doctors by patient count and revenue. |
| 8 | Hospital revenue **`RANK()`** | Hospitals ranked by total revenue (window function). |
| 9 | Monthly **running total** | Cumulative billing across months (`SUM() OVER`). |
| 10 | Demographics by gender & test result | Average age and billing, split by gender and result. |

Example (report 1):

```sql
SELECT EXTRACT(YEAR  FROM date_of_admission) AS year,
       EXTRACT(MONTH FROM date_of_admission) AS month,
       COUNT(*)                              AS total_admissions
FROM healthcare
GROUP BY year, month
ORDER BY year, month;
```

---

## 7. Sample output (54,966-row run)

**Monthly totals** (report 1 — 61 months, first rows):

| month | admissions | total_billing |
|---|---|---|
| 2019-05 | 677 | 17,403,451.24 |
| 2019-06 | 899 | 23,613,799.97 |
| 2019-07 | 951 | 24,632,284.83 |

**Average cost + length of stay by condition** (reports 2 & 5):

| medical_condition | cases | avg_cost | avg_stay |
|---|---|---|---|
| Obesity | 9,146 | 25,804.36 | 15.45 |
| Diabetes | 9,216 | 25,660.48 | 15.43 |
| Asthma | 9,095 | 25,633.46 | 15.68 |
| Arthritis | 9,218 | 25,511.78 | 15.50 |
| Hypertension | 9,151 | 25,503.06 | 15.44 |
| Cancer | 9,140 | 25,152.32 | 15.50 |

**Billing by insurance provider** (report 4):

| insurance_provider | claims | total_billing | avg_billing |
|---|---|---|---|
| Cigna | 11,139 | 284,334,096.09 | 25,526.00 |
| Medicare | 11,039 | 282,911,036.99 | 25,628.32 |
| Blue Cross | 10,952 | 280,409,076.16 | 25,603.46 |

**Hospital revenue ranking** (report 8 — window function):

| rank | hospital | total_revenue | admissions |
|---|---|---|---|
| 1 | Johnson Plc | 1,081,477.31 | 37 |
| 2 | Llc Smith | 1,030,189.87 | 44 |
| 3 | Smith Plc | 1,029,424.45 | 36 |

**Monthly running total** (report 9 — `SUM() OVER`):

| month | monthly_billing | running_total |
|---|---|---|
| 2019-05 | 17,403,451.24 | 17,403,451.24 |
| 2019-06 | 23,613,799.97 | 41,017,251.21 |
| 2019-07 | 24,632,284.83 | 65,649,536.04 |

---

## 8. Tests

```bash
python -m pytest tests/ --cov=src --cov-report=term-missing
```

**12 tests, all passing — 100% statement coverage. No database required** (tests use tiny in-memory DataFrames and temporary files).

| Test | Covers |
|---|---|
| `test_load_data_success` | Loading a valid CSV. |
| `test_load_data_file_not_found` | `FileNotFoundError` on a missing path. |
| `test_check_missing_values` | Per-column null counts. |
| `test_check_duplicates` | Duplicate row counting. |
| `test_clean_data_removes_duplicates` | De-dup *after* text standardization. |
| `test_clean_data_handles_dates` | Dates become `datetime64`. |
| `test_clean_data_handles_billing_numeric` | Billing becomes numeric. |
| `test_save_cleaned_data` | File written and readable back. |
| `test_load_and_clean` | Full end-to-end flow. |
| `test_clean_data_preserves_column_structure` | No columns lost. |
| `test_clean_data_handles_missing_columns_gracefully` | Partial DataFrames don't crash. |
| `test_save_without_makedirs` | Nested output dirs auto-created. |

```
Name                          Stmts   Miss  Cover
---------------------------------------------------
src/data_processing.py           35      0   100%
---------------------------------------------------
TOTAL                            35      0   100%
```

---

## 9. Design notes / lessons

- **Standardize before de-duplicating.** Cleaning text *first* turns casing-only differences into true duplicates, so `drop_duplicates()` removes them. Reverse the order and you silently keep ~500 junk rows. The test `test_clean_data_removes_duplicates` locks this behaviour in.
- **Functions take DataFrames, not connections or paths.** Keeping I/O at the edges (`load_data`, `save_cleaned_data`) is what lets every other function be tested without touching disk or a database.
- **Two table schemas, one shape.** `create_tables.sql` (PostgreSQL `SERIAL`) and `create_tables_mysql.sql` (MySQL `AUTO_INCREMENT`) define the identical 16-column table, so the same queries run unchanged on either engine.
- **Derived columns belong in the pipeline, not the source.** `Duration_Days` is computed during preparation rather than stored in the raw CSV, keeping the raw data immutable.
- **Document the "why", not just the "what".** Every fix in `cleaning_analysis.md` records how many rows it touched, so the cleaning is auditable.

---

## 10. Key findings

1. **Average billing:** $25,544.31 across all 54,966 patients.
2. **Most common diagnosis:** Arthritis (9,218 cases), followed closely by Diabetes, Hypertension, Obesity, and Cancer — the six conditions are almost evenly distributed.
3. **Costliest condition:** Obesity, at $25,804.36 average per case — about $650 more than the cheapest (Cancer, $25,152.32).

---

## 11. Requirements

- Python 3.10+ (developed on 3.14)
- pandas
- mysql-connector-python
- SQLAlchemy
- psycopg2-binary
- pytest, pytest-cov
- MySQL 8.x and/or PostgreSQL 14+
