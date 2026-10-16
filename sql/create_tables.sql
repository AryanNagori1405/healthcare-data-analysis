-- PostgreSQL table schema for healthcare data

CREATE TABLE IF NOT EXISTS healthcare (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    age INT,
    gender VARCHAR(20),
    blood_type VARCHAR(10),
    medical_condition VARCHAR(100),
    date_of_admission DATE,
    doctor VARCHAR(255),
    hospital VARCHAR(255),
    insurance_provider VARCHAR(100),
    billing_amount DECIMAL(12,2),
    room_number INT,
    admission_type VARCHAR(50),
    discharge_date DATE,
    medication VARCHAR(100),
    test_results VARCHAR(50),
    duration_days INT
);
