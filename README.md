# Healthcare Data Analysis Project

## Problem Statement
This project aims to analyze a healthcare dataset using Python and SQL to answer real-world questions about hospital admissions, patient billing, diagnoses, and other healthcare metrics.

## Dataset
- **Source**: Kaggle Healthcare Dataset
- **Location**: `C:\Users\aryan\Downloads\Healthcare Dataset\healthcare_dataset.csv`
- **Original Size**: 55,500 rows, 15 columns
- **Cleaned Size**: 54,966 rows, 15 columns (after removing 534 duplicates)
- **Features**: Name, Age, Gender, Blood Type, Medical Condition, Date of Admission, Doctor, Hospital, Insurance Provider, Billing Amount, Room Number, Admission Type, Discharge Date, Medication, Test Results

## Data Cleaning
Performed in `src/data_processing.py`:
1. Removed 534 duplicate rows
2. Standardized text fields (strip and title case)
3. Converted dates to datetime format
4. Ensured Billing Amount is numeric
5. Added `Duration_Days` calculated as (Discharge Date - Date of Admission)

## Project Structure
```
HealthcareDataAnalysis/
├── data/
│   ├── healthcare_cleaned.csv
│   └── healthcare_for_db.csv
├── notebooks/
│   └── data_exploration.ipynb
├── src/
│   └── data_processing.py
├── sql/
│   ├── create_tables.sql
│   └── queries.sql
├── tests/
│   ├── __init__.py
│   └── test_data_processing.py
├── cleaning_analysis.md
├── db_import.py
├── README.md
└── requirements.txt (if needed)
```

## Key Findings (with real numbers)
1. **Average Billing Amount**: $25,544.31 across all patients
2. **Top Medical Conditions by Volume**: Arthritis (9,218 cases), Diabetes (9,216), Hypertension (9,151), Obesity (9,146), Cancer (9,140), Asthma (9,095)
3. **Average Cost by Medical Condition**: Obesity ($25,804.36), Diabetes ($25,660.48), Asthma ($25,633.46), Arthritis ($25,511.78), Hypertension ($25,503.06), Cancer ($25,152.32)

## SQL Queries (10 total)
All queries are in `sql/queries.sql` and include:
- Aggregations (GROUP BY, COUNT, SUM, AVG)
- JOINs (conceptually), GROUP BY
- Window functions: RANK() and running total (SUM() OVER)

## Python Functions (6 functions)
In `src/data_processing.py`:
1. `load_data(filepath)` - Load CSV data
2. `check_missing_values(df)` - Check for missing values
3. `check_duplicates(df)` - Count duplicate rows
4. `clean_data(df)` - Clean and transform data
5. `save_cleaned_data(df, output_path)` - Save cleaned data
6. `load_and_clean(input_path, output_path=None)` - End-to-end processing

## Testing
- 12 pytest tests covering all 6 functions
- Coverage: 100% (measured with pytest-cov)
- Run with: `$env:PYTHONPATH="C:\Users\aryan\HealthcareDataAnalysis"; & "C:\Program Files\Python314\python.exe" -m pytest tests/test_data_processing.py --cov=src`

## How to Run

### 1. Set up environment
```powershell
$env:PYTHONPATH="C:\Users\aryan\HealthcareDataAnalysis"
& "C:\Program Files\Python314\python.exe" -m pip install pandas mysql-connector-python sqlalchemy pytest pytest-cov psycopg2-binary
```

### 2. Run data cleaning
```powershell
$env:PYTHONPATH="C:\Users\aryan\HealthcareDataAnalysis"
& "C:\Program Files\Python314\python.exe" -c "from src.data_processing import load_and_clean; load_and_clean('data/healthcare_cleaned.csv', 'data/healthcare_for_db.csv')"
```

### 3. Run tests
```powershell
$env:PYTHONPATH="C:\Users\aryan\HealthcareDataAnalysis"
& "C:\Program Files\Python314\python.exe" -m pytest tests/test_data_processing.py --cov=src --cov-report=term-missing
```

### 4. Database Setup
1. Create table using `sql/create_tables.sql` in MySQL and PostgreSQL
2. Import `data/healthcare_for_db.csv` using appropriate DB tools or connectors
3. Run queries from `sql/queries.sql` on both databases

## Requirements
- Python 3.14
- pandas
- mysql-connector-python
- sqlalchemy
- psycopg2-binary
- pytest
- pytest-cov
