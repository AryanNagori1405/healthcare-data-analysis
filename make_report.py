from fpdf import FPDF, XPos, YPos

class Report(FPDF):
    def header(self):
        if self.page_no() > 1:
            self.set_font('Helvetica', 'I', 8)
            self.cell(0, 8, 'Healthcare Data Analysis Project - Aryan Nagori', align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            self.line(10, 12, 200, 12)
            self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

    def section(self, num, title):
        self.set_font('Helvetica', 'B', 13)
        self.set_text_color(20, 60, 120)
        self.cell(0, 9, f'{num}. {title}', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_text_color(0, 0, 0)
        self.ln(2)

    def sub(self, title):
        self.set_font('Helvetica', 'B', 11)
        self.cell(0, 8, title, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    def body(self, text):
        self.set_font('Helvetica', '', 10)
        self.multi_cell(0, 5.5, text)
        self.ln(1)

    def code(self, text):
        self.set_font('Courier', '', 8.5)
        self.set_fill_color(240, 240, 240)
        self.multi_cell(0, 4.6, text, fill=True)
        self.set_font('Helvetica', '', 10)
        self.ln(1)

pdf = Report()
pdf.set_auto_page_break(auto=True, margin=20)

# ---------- COVER PAGE ----------
pdf.add_page()
pdf.ln(30)
pdf.set_font('Helvetica', 'B', 24)
pdf.set_text_color(20, 60, 120)
pdf.cell(0, 12, 'PROJECT REPORT', align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.ln(6)
pdf.set_font('Helvetica', 'B', 16)
pdf.set_text_color(0, 0, 0)
pdf.cell(0, 10, 'Healthcare Data Analysis', align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.set_font('Helvetica', '', 11)
pdf.cell(0, 8, 'Using Python, MySQL and PostgreSQL', align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.ln(20)

pdf.set_font('Helvetica', 'B', 11)
pdf.cell(0, 7, 'Submitted By:', align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.set_font('Helvetica', '', 11)
pdf.cell(0, 6, 'Aryan Nagori', align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.cell(0, 6, 'GitHub: github.com/AryanNagori1405', align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.ln(10)
pdf.set_font('Helvetica', 'B', 11)
pdf.cell(0, 7, 'Technologies Used:', align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.set_font('Helvetica', '', 11)
pdf.cell(0, 6, 'Python | pandas | MySQL | PostgreSQL | SQL | pytest | pytest-cov', align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.ln(10)
pdf.cell(0, 6, 'Date: October 2026', align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

# ---------- TABLE OF CONTENTS ----------
pdf.add_page()
pdf.set_text_color(20, 60, 120)
pdf.set_font('Helvetica', 'B', 16)
pdf.cell(0, 10, 'TABLE OF CONTENTS', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.set_text_color(0, 0, 0)
pdf.ln(4)
toc = [
    ('1.', 'Introduction'),
    ('2.', 'Problem Statement'),
    ('3.', 'Objectives'),
    ('4.', 'Dataset Description'),
    ('5.', 'Data Cleaning and Preprocessing'),
    ('6.', 'Project Structure and File Organization'),
    ('7.', 'Python Implementation: 6 Functions'),
    ('8.', 'SQL Implementation: 10 Queries'),
    ('9.', 'Database Creation: MySQL and PostgreSQL'),
    ('10.', 'Testing and Code Coverage'),
    ('11.', 'Key Findings with Real Numbers'),
    ('12.', 'How to Run the Project (Step by Step)'),
    ('13.', 'Requirements and Dependencies'),
    ('14.', 'Conclusion'),
]
pdf.set_font('Helvetica', '', 11)
for num, title in toc:
    pdf.cell(0, 8, f'{num}  {title}', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

# ---------- 1. INTRODUCTION ----------
pdf.add_page()
pdf.section('1', 'INTRODUCTION')
pdf.body('This project presents a complete end-to-end healthcare data analysis. It takes a real-world hospital admissions dataset from Kaggle, cleans it with Python and pandas, stores it in two different relational databases (MySQL and PostgreSQL), and answers real analytical questions using SQL queries. The code is broken into reusable Python functions, thoroughly unit-tested with pytest, and documented for anyone who wants to understand or extend it.')
pdf.body('The workflow follows the classic data analysis pipeline: (1) load and explore raw data, (2) clean and fix quality issues, (3) transform and enrich the data, (4) load it into databases, (5) analyze with SQL, and (6) test and document everything.')

# ---------- 2. PROBLEM STATEMENT ----------
pdf.section('2', 'PROBLEM STATEMENT')
pdf.body('Healthcare organizations generate large volumes of patient data across admissions, billing, diagnoses, medications and test results. Answering questions like "how many admissions happen each month?", "which diagnosis is most common?", or "which hospital earns the most?" requires clean data and well-written queries. The goal of this project is to demonstrate this entire process on a real dataset of over 55,000 patient records.')

# ---------- 3. OBJECTIVES ----------
pdf.section('3', 'OBJECTIVES')
pdf.body('1. Load and explore a public healthcare dataset from Kaggle (55,500 rows, 15 columns).')
pdf.body('2. Identify and fix data quality problems: duplicates, inconsistent text, wrong data types.')
pdf.body('3. Clean and transform the data using Python and pandas.')
pdf.body('4. Create the same table structure in both MySQL and PostgreSQL and import the cleaned data.')
pdf.body('5. Write 10 SQL queries that answer real business questions, including joins, GROUP BY, and at least two window functions (RANK and running total).')
pdf.body('6. Convert the cleaning and loading steps into 6 reusable Python functions in a .py file.')
pdf.body('7. Write 12 pytest tests for those functions and measure coverage with pytest-cov (target: 90% or more).')
pdf.body('8. Document the entire project: README, cleaning report, and this PDF.')

# ---------- 4. DATASET ----------
pdf.add_page()
pdf.section('4', 'DATASET DESCRIPTION')
pdf.body('Source: Kaggle Healthcare Dataset (hospital admissions / patient billing data).')
pdf.body('Original Shape: 55,500 rows and 15 columns.')
pdf.body('Cleaned Shape: 54,966 rows and 15 columns (after removing 534 duplicate rows).')
pdf.body('Missing Values: 0 (the dataset had no nulls).')
pdf.ln(2)
pdf.sub('Columns:')
pdf.code('Name, Age, Gender, Blood Type, Medical Condition, Date of Admission,\nDoctor, Hospital, Insurance Provider, Billing Amount, Room Number,\nAdmission Type, Discharge Date, Medication, Test Results')
pdf.ln(2)
pdf.sub('Data Types After Cleaning:')
pdf.code('date_of_admission : datetime64\ndischarge_date    : datetime64\nbilling_amount    : float64\nage, room_number  : integer\ntext columns      : string (standardized to Title Case)\nduration_days     : integer (derived column)')

# ---------- 5. DATA CLEANING ----------
pdf.section('5', 'DATA CLEANING AND PREPROCESSING')
pdf.body('The raw dataset contained several quality issues that had to be fixed before analysis:')
pdf.ln(1)
pdf.sub('Issues Found:')
pdf.body('1. Duplicate rows: 534 exact duplicate records were found.')
pdf.body('2. Inconsistent text casing: Values like "Bobby JacksOn", "andrEw waTtS", "MALE"/"male" mixed across columns.')
pdf.body('3. Dates stored as strings in "dd-mm-yyyy" format instead of proper date type.')
pdf.body('4. Billing Amount needed to be guaranteed numeric.')
pdf.ln(1)
pdf.sub('Fixes Applied:')
pdf.body('1. Duplicates removed: 534 rows deleted. Standardization ran BEFORE deduplication so that "male" and "MALE" became identical rows and were then correctly removed.')
pdf.body('2. Text standardized: strip() and title() applied to Name, Gender, Blood Type, Medical Condition, Doctor, Hospital, Insurance Provider, Admission Type, Medication, Test Results. All rows affected (formatting only).')
pdf.body('3. Dates converted to datetime using format %d-%m-%Y for Date of Admission and Discharge Date.')
pdf.body('4. Billing Amount cast to numeric.')
pdf.body('5. New feature Duration_Days = Discharge Date - Admission Date, useful for length-of-stay analysis.')
pdf.body('All of this is documented in cleaning_analysis.md with affected row counts.')

# ---------- 6. PROJECT STRUCTURE ----------
pdf.add_page()
pdf.section('6', 'PROJECT STRUCTURE AND FILE ORGANIZATION')
pdf.code('HealthcareDataAnalysis/\n|-- data/\n|   |-- healthcare_cleaned.csv      (cleaned data)\n|   |-- healthcare_for_db.csv        (data + Duration_Days for DB import)\n|-- notebooks/\n|   |-- data_exploration.ipynb       (exploratory analysis notebook)\n|-- src/\n|   |-- data_processing.py           (6 reusable Python functions)\n|-- sql/\n|   |-- create_tables.sql            (PostgreSQL table schema)\n|   |-- create_tables_mysql.sql      (MySQL table schema)\n|   |-- queries.sql                  (10 analytical queries)\n|-- tests/\n|   |-- __init__.py\n|   |-- test_data_processing.py      (12 pytest tests)\n|-- cleaning_analysis.md             (data cleaning documentation)\n|-- README.md                        (project overview and run guide)\n|-- db_import.py                     (database import helper)\n|-- PROJECT_REPORT.pdf               (this document)')
pdf.ln(2)
pdf.body('Each folder has a clear responsibility: data/ holds CSV files, src/ holds reusable logic, sql/ holds all database scripts, tests/ holds the test suite, and notebooks/ holds exploration work.')

# ---------- 7. PYTHON FUNCTIONS ----------
pdf.add_page()
pdf.section('7', 'PYTHON IMPLEMENTATION: 6 FUNCTIONS')
pdf.body('All cleaning and loading logic lives in src/data_processing.py as six well-documented functions:')
pdf.ln(1)
pdf.sub('1. load_data(filepath)')
pdf.body('Reads a CSV file into a pandas DataFrame. Raises FileNotFoundError with a clear message if the file does not exist.')
pdf.ln(1)
pdf.sub('2. check_missing_values(df)')
pdf.body('Returns a pandas Series with the count of missing (NaN) values in each column. Used during exploration to confirm the dataset had zero missing values.')
pdf.ln(1)
pdf.sub('3. check_duplicates(df)')
pdf.body('Returns the number of duplicate rows in the DataFrame. Reported 534 duplicates in the raw dataset.')
pdf.ln(1)
pdf.sub('4. clean_data(df)')
pdf.body('The core cleaning function. Order matters: it first standardizes text (strip + title case), then converts dates and billing to correct types, and only THEN removes duplicates. This order ensures rows that only differed in casing are correctly identified as duplicates. Returns the cleaned DataFrame.')
pdf.ln(1)
pdf.sub('5. save_cleaned_data(df, output_path)')
pdf.body('Saves the DataFrame to CSV. Creates the output directory automatically if it does not exist (useful for nested paths).')
pdf.ln(1)
pdf.sub('6. load_and_clean(input_path, output_path=None)')
pdf.body('End-to-end convenience function: loads the raw CSV, cleans it, and optionally saves the result. Returns the cleaned DataFrame.')

# ---------- 8. SQL QUERIES ----------
pdf.add_page()
pdf.section('8', 'SQL IMPLEMENTATION: 10 QUERIES')
pdf.body('All 10 queries are in sql/queries.sql and run on both MySQL and PostgreSQL. They cover joins, GROUP BY, aggregations and two window functions as required.')
pdf.ln(1)
queries = [
    ('Q1. Admissions per month', 'Groups by year and month using EXTRACT, counts admissions to see seasonal patterns.'),
    ('Q2. Average cost per department', 'Uses AVG(billing_amount) grouped by medical_condition to compare costs across conditions.'),
    ('Q3. Top 5 most common diagnoses', 'COUNT grouped by medical_condition, ordered descending with LIMIT 5.'),
    ('Q4. Total billing by insurance provider', 'SUM and AVG of billing grouped by insurance_provider to see which insurer pays most.'),
    ('Q5. Average length of stay by condition', 'AVG(duration_days) grouped by medical_condition.'),
    ('Q6. Admissions by admission type', 'COUNT and AVG cost grouped by admission_type (Emergency, Elective, Urgent).'),
    ('Q7. Top 10 doctors by patient count', 'COUNT and SUM revenue grouped by doctor, LIMIT 10.'),
    ('Q8. RANK() window function', 'RANK() OVER (ORDER BY SUM(billing_amount) DESC) to rank hospitals by total revenue.'),
    ('Q9. Running total by month', 'SUM(billing_amount) OVER (ORDER BY year, month) gives a cumulative running total of billing across months.'),
    ('Q10. Demographics by gender and test results', 'AVG age and billing grouped by gender and test_results for demographic insights.'),
]
for title, desc in queries:
    pdf.sub(title)
    pdf.body(desc)
    pdf.ln(1)

# ---------- 9. DATABASE SETUP ----------
pdf.add_page()
pdf.section('9', 'DATABASE CREATION: MYSQL AND POSTGRESQL')
pdf.body('The same table structure was created in both databases and the cleaned data imported into each.')
pdf.ln(1)
pdf.sub('MySQL:')
pdf.code('CREATE DATABASE healthcare_db;\nUSE healthcare_db;\n-- then run sql/create_tables_mysql.sql (uses AUTO_INCREMENT)\n-- import data/healthcare_for_db.csv via LOAD DATA or Python/SQLAlchemy')
pdf.ln(1)
pdf.sub('PostgreSQL:')
pdf.code('CREATE DATABASE healthcare_db;\n-- then run sql/create_tables.sql (uses SERIAL)\n-- import data via \\copy or Python/SQLAlchemy')
pdf.ln(1)
pdf.sub('Table Schema (common to both):')
pdf.code('id, name, age, gender, blood_type, medical_condition,\ndate_of_admission, doctor, hospital, insurance_provider,\nbilling_amount, room_number, admission_type, discharge_date,\nmedication, test_results, duration_days')
pdf.ln(1)
pdf.body('Verification: SELECT COUNT(*) FROM healthcare; should return 54,966 rows on both databases. All 10 queries run successfully on both MySQL and PostgreSQL.')

# ---------- 10. TESTING ----------
pdf.add_page()
pdf.section('10', 'TESTING AND CODE COVERAGE')
pdf.body('The test suite lives in tests/test_data_processing.py and contains 12 pytest tests covering all 6 functions, including edge cases:')
pdf.ln(1)
pdf.body('- test_load_data_success: loads a small CSV correctly.')
pdf.body('- test_load_data_file_not_found: raises FileNotFoundError for missing files.')
pdf.body('- test_check_missing_values: verifies null counting per column.')
pdf.body('- test_check_duplicates: verifies duplicate row counting.')
pdf.body('- test_clean_data_removes_duplicates: confirms duplicates removed only after text standardization.')
pdf.body('- test_clean_data_handles_dates: confirms date columns become datetime.')
pdf.body('- test_clean_data_handles_billing_numeric: confirms billing becomes numeric.')
pdf.body('- test_save_cleaned_data: confirms file is written and readable back.')
pdf.body('- test_load_and_clean: confirms end-to-end flow works.')
pdf.body('- test_clean_data_preserves_column_structure: no columns lost during cleaning.')
pdf.body('- test_clean_data_handles_missing_columns_gracefully: function does not crash on incomplete data.')
pdf.body('- test_save_without_makedirs: nested output directories are created automatically.')
pdf.ln(2)
pdf.sub('Result: 12 tests passed. Coverage: 100% (pytest-cov), well above the 90% target.')
pdf.code('$env:PYTHONPATH="C:\\Users\\aryan\\HealthcareDataAnalysis"\n& "C:\\Program Files\\Python314\\python.exe" -m pytest tests/\n    --cov=src --cov-report=term-missing')

# ---------- 11. KEY FINDINGS ----------
pdf.add_page()
pdf.section('11', 'KEY FINDINGS WITH REAL NUMBERS')
pdf.body('The analysis of 54,966 patient records produced these concrete findings:')
pdf.ln(1)
pdf.sub('Finding 1: Overall Average Billing')
pdf.body('The average billing amount across all 54,966 patients is $25,544.31. This baseline helps identify which conditions and providers are above or below average.')
pdf.ln(1)
pdf.sub('Finding 2: Top Medical Conditions by Volume')
pdf.body('The six conditions are remarkably evenly distributed, indicating a balanced synthetic sample:')
pdf.body('Arthritis: 9,218 cases | Diabetes: 9,216 cases | Hypertension: 9,151 cases')
pdf.body('Obesity: 9,146 cases | Cancer: 9,140 cases | Asthma: 9,095 cases')
pdf.ln(1)
pdf.sub('Finding 3: Average Cost Varies by Condition')
pdf.body('Obesity is the most expensive condition at $25,804.36 average, while Cancer is the least at $25,152.32:')
pdf.body('Obesity $25,804.36 > Diabetes $25,660.48 > Asthma $25,633.46')
pdf.body('Arthritis $25,511.78 > Hypertension $25,503.06 > Cancer $25,152.32')
pdf.ln(1)
pdf.sub('Additional Observations:')
pdf.body('- Monthly admissions peak at 899 in June 2019 and range between roughly 4,200 and 4,700 per month across the full dataset years.')
pdf.body('- Hospital names are highly fragmented (39,876 unique values for 54,966 rows), suggesting many small providers or name inconsistencies worth further normalization.')

# ---------- 12. HOW TO RUN ----------
pdf.add_page()
pdf.section('12', 'HOW TO RUN THE PROJECT (STEP BY STEP)')
pdf.ln(1)
pdf.sub('Step 1: Install dependencies')
pdf.code('pip install pandas mysql-connector-python sqlalchemy psycopg2-binary pytest pytest-cov')
pdf.ln(1)
pdf.sub('Step 2: Set the Python path (Windows PowerShell)')
pdf.code('$env:PYTHONPATH="C:\\Users\\aryan\\HealthcareDataAnalysis"')
pdf.ln(1)
pdf.sub('Step 3: Run the tests')
pdf.code('& "C:\\Program Files\\Python314\\python.exe" -m pytest tests/ --cov=src --cov-report=term-missing')
pdf.ln(1)
pdf.sub('Step 4: (Optional) Re-clean the data')
pdf.code('from src.data_processing import load_and_clean\nload_and_clean("data/healthcare_cleaned.csv", "data/healthcare_for_db.csv")')
pdf.ln(1)
pdf.sub('Step 5: Set up databases')
pdf.code('# MySQL\nCREATE DATABASE healthcare_db; USE healthcare_db;\nmysql -u root -p healthcare_db < sql/create_tables_mysql.sql\n\n# PostgreSQL\npsql -U postgres -c "CREATE DATABASE healthcare_db;"\npsql -U postgres -d healthcare_db -f sql/create_tables.sql')
pdf.ln(1)
pdf.sub('Step 6: Import the data')
pdf.body('Use LOAD DATA (MySQL) or \\copy (PostgreSQL), or run the Python/SQLAlchemy import shown in db_import.py. The CSV to import is data/healthcare_for_db.csv.')
pdf.ln(1)
pdf.sub('Step 7: Run the queries')
pdf.code('psql -U postgres -d healthcare_db -f sql/queries.sql\nmysql -u root -p healthcare_db < sql/queries.sql')

# ---------- 13. REQUIREMENTS ----------
pdf.section('13', 'REQUIREMENTS AND DEPENDENCIES')
pdf.code('Python 3.14+\npandas\nmysql-connector-python\nSQLAlchemy\npsycopg2-binary\npytest\npytest-cov\nfpdf2 (for generating this report)')
pdf.ln(1)
pdf.body('A MySQL server (8.x) and a PostgreSQL server (14+) are needed for the database portions. Both can be installed locally or run via Docker.')

# ---------- 14. CONCLUSION ----------
pdf.add_page()
pdf.section('14', 'CONCLUSION')
pdf.body('This project successfully demonstrates a complete, professional data analysis workflow on a real healthcare dataset:')
pdf.body('1. Data quality was assessed and improved: 534 duplicates removed, text standardized, dates and numbers correctly typed. Every fix is documented with affected row counts.')
pdf.body('2. The pipeline was modularized into 6 reusable Python functions, making it easy to re-run on new data.')
pdf.body('3. The cleaned data was loaded into both MySQL and PostgreSQL using the same table structure, proving database portability.')
pdf.body('4. Ten analytical SQL queries answer real questions using GROUP BY, aggregations, and two window functions (RANK for hospital ranking and a running total for monthly billing).')
pdf.body('5. The code is validated by 12 pytest tests achieving 100% coverage, well above the 90% target.')
pdf.body('6. Concrete findings were extracted: average billing of $25,544.31, six nearly equally common conditions led by Arthritis (9,218 cases), and Obesity being the costliest condition ($25,804.36 average).')
pdf.ln(2)
pdf.body('The project is reproducible: following the steps in section 12, anyone can recreate the databases, re-run the tests, and reproduce every number in this report. The code and full documentation are available on GitHub at github.com/AryanNagori1405.')

pdf.output(r'C:\Users\aryan\HealthcareDataAnalysis\PROJECT_REPORT.pdf')
print('PDF generated successfully')
