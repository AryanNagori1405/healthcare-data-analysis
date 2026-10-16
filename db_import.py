import pandas as pd
import sys
sys.path.append('C:\\Users\\aryan\\HealthcareDataAnalysis')

# This is a template script for importing data
# Modify connection strings as needed

if __name__ == '__main__':
    df = pd.read_csv('data/healthcare_for_db.csv')
    print(f'Data ready for import: {len(df)} rows')
    print('Columns:', df.columns.tolist())
