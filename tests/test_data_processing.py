import os
import tempfile
import pandas as pd
import pytest
from src.data_processing import (
    load_data,
    check_missing_values,
    check_duplicates,
    clean_data,
    save_cleaned_data,
    load_and_clean,
)


def test_load_data_success():
    # Create a small test CSV
    df_test = pd.DataFrame({
        'Name': ['John Doe', 'Jane Smith'],
        'Age': [30, 40],
        'Billing Amount': [100.5, 200.0]
    })
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        df_test.to_csv(f.name, index=False)
        filepath = f.name
    try:
        loaded = load_data(filepath)
        assert len(loaded) == 2
        assert list(loaded.columns) == list(df_test.columns)
    finally:
        os.unlink(filepath)


def test_load_data_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_data('nonexistent_file.csv')


def test_check_missing_values():
    df = pd.DataFrame({'A': [1, None, 3], 'B': [None, None, None], 'C': [1, 2, 3]})
    result = check_missing_values(df)
    assert result['A'] == 1
    assert result['B'] == 3
    assert result['C'] == 0


def test_check_duplicates():
    df = pd.DataFrame({'A': [1, 2, 1], 'B': [10, 20, 10]})
    result = check_duplicates(df)
    assert result == 1


def test_clean_data_removes_duplicates():
    df = pd.DataFrame({
        'Name': ['John Doe', 'John Doe', 'Jane Smith'],
        'Age': [30, 30, 40],
        'Gender': ['male', 'MALE', 'female'],
        'Blood Type': ['A+', 'A+', 'B-'],
        'Medical Condition': ['diabetes', 'diabetes', 'cancer'],
        'Date of Admission': ['15-01-2024', '15-01-2024', '20-02-2024'],
        'Doctor': ['dr smith', 'dr smith', 'dr jones'],
        'Hospital': ['city hospital', 'city hospital', 'general hospital'],
        'Insurance Provider': ['aetna', 'aetna', 'blue cross'],
        'Billing Amount': ['100.5', '100.5', '200.0'],
        'Room Number': [101, 101, 102],
        'Admission Type': ['emergency', 'emergency', 'elective'],
        'Discharge Date': ['20-01-2024', '20-01-2024', '25-02-2024'],
        'Medication': ['aspirin', 'aspirin', 'ibuprofen'],
        'Test Results': ['normal', 'normal', 'abnormal']
    })
    cleaned = clean_data(df)
    assert len(cleaned) == 2
    # Check standardization
    assert cleaned.iloc[0]['Name'] == 'John Doe'
    assert cleaned.iloc[0]['Gender'] == 'Male'
    assert cleaned.iloc[1]['Gender'] == 'Female'


def test_clean_data_handles_dates():
    df = pd.DataFrame({
        'Name': ['John Doe'],
        'Age': [30],
        'Gender': ['Male'],
        'Blood Type': ['A+'],
        'Medical Condition': ['Diabetes'],
        'Date of Admission': ['15-01-2024'],
        'Doctor': ['Dr Smith'],
        'Hospital': ['City Hospital'],
        'Insurance Provider': ['Aetna'],
        'Billing Amount': ['100.5'],
        'Room Number': [101],
        'Admission Type': ['Emergency'],
        'Discharge Date': ['20-01-2024'],
        'Medication': ['Aspirin'],
        'Test Results': ['Normal']
    })
    cleaned = clean_data(df)
    assert pd.api.types.is_datetime64_any_dtype(cleaned['Date of Admission'])
    assert pd.api.types.is_datetime64_any_dtype(cleaned['Discharge Date'])


def test_clean_data_handles_billing_numeric():
    df = pd.DataFrame({
        'Name': ['John Doe', 'Jane Smith'],
        'Age': [30, 40],
        'Gender': ['Male', 'Female'],
        'Blood Type': ['A+', 'B-'],
        'Medical Condition': ['Diabetes', 'Cancer'],
        'Date of Admission': ['15-01-2024', '20-02-2024'],
        'Doctor': ['Dr Smith', 'Dr Jones'],
        'Hospital': ['City Hospital', 'General Hospital'],
        'Insurance Provider': ['Aetna', 'Blue Cross'],
        'Billing Amount': ['100.5', '200.75'],
        'Room Number': [101, 102],
        'Admission Type': ['Emergency', 'Elective'],
        'Discharge Date': ['20-01-2024', '25-02-2024'],
        'Medication': ['Aspirin', 'Ibuprofen'],
        'Test Results': ['Normal', 'Abnormal']
    })
    cleaned = clean_data(df)
    assert pd.api.types.is_numeric_dtype(cleaned['Billing Amount'])


def test_save_cleaned_data():
    df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = os.path.join(tmpdir, 'test_output.csv')
        result = save_cleaned_data(df, output_path)
        assert os.path.exists(result)
        # Load back and verify
        loaded = pd.read_csv(result)
        assert len(loaded) == 2


def test_load_and_clean():
    df_test = pd.DataFrame({
        'Name': ['John Doe', 'John Doe'],
        'Age': [30, 30],
        'Gender': ['male', 'male'],
        'Blood Type': ['A+', 'A+'],
        'Medical Condition': ['diabetes', 'diabetes'],
        'Date of Admission': ['15-01-2024', '15-01-2024'],
        'Doctor': ['dr smith', 'dr smith'],
        'Hospital': ['city hospital', 'city hospital'],
        'Insurance Provider': ['aetna', 'aetna'],
        'Billing Amount': ['100.5', '100.5'],
        'Room Number': [101, 101],
        'Admission Type': ['emergency', 'emergency'],
        'Discharge Date': ['20-01-2024', '20-01-2024'],
        'Medication': ['aspirin', 'aspirin'],
        'Test Results': ['normal', 'normal']
    })
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        df_test.to_csv(f.name, index=False)
        input_path = f.name
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = os.path.join(tmpdir, 'cleaned.csv')
        try:
            cleaned = load_and_clean(input_path, output_path)
            assert len(cleaned) == 1
            assert os.path.exists(output_path)
        finally:
            os.unlink(input_path)


def test_clean_data_preserves_column_structure():
    df = pd.DataFrame({
        'Name': ['John Doe'],
        'Age': [30],
        'Gender': ['male'],
        'Blood Type': ['A+'],
        'Medical Condition': ['diabetes'],
        'Date of Admission': ['15-01-2024'],
        'Doctor': ['dr smith'],
        'Hospital': ['city hospital'],
        'Insurance Provider': ['aetna'],
        'Billing Amount': ['100.5'],
        'Room Number': [101],
        'Admission Type': ['emergency'],
        'Discharge Date': ['20-01-2024'],
        'Medication': ['aspirin'],
        'Test Results': ['normal']
    })
    cleaned = clean_data(df)
    assert set(cleaned.columns) == set(df.columns)


def test_clean_data_handles_missing_columns_gracefully():
    df = pd.DataFrame({'Name': ['John'], 'Age': [30]})
    cleaned = clean_data(df)
    assert len(cleaned) == 1
    assert 'Name' in cleaned.columns


def test_save_without_makedirs():
    df = pd.DataFrame({'A': [1]})
    with tempfile.TemporaryDirectory() as tmpdir:
        nested = os.path.join(tmpdir, 'subdir', 'nested', 'file.csv')
        save_cleaned_data(df, nested)
        assert os.path.exists(nested)
