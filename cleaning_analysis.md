# Data Cleaning Report

## Initial Dataset
- Original shape: 55500 rows, 15 columns
- Source: Kaggle Healthcare Dataset

## Issues Identified
1. Duplicates: 534 duplicate rows found
2. Text inconsistencies: Inconsistent casing in Name, Gender, Blood Type, Medical Condition, Doctor, Hospital, Insurance Provider, Admission Type, Medication, Test Results
3. Data types: Date columns stored as strings, Billing Amount numeric

## Fixes Applied
1. Removed duplicates: Dropped 534 duplicate rows (rows affected: 534)
2. Standardized text: Applied strip() and title() casing to categorical text columns (rows affected: all)
3. Converted dates: Parsed Date of Admission and Discharge Date to datetime (format: %d-%m-%Y)
4. Ensured numeric type: Converted Billing Amount to numeric

## Final Dataset
- Cleaned shape: 54966 rows, 15 columns
- No missing values
