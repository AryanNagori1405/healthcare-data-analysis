-- 10 SQL Queries for Healthcare Data Analysis

-- 1. Admissions per month
SELECT 
  EXTRACT(YEAR FROM date_of_admission) AS year,
  EXTRACT(MONTH FROM date_of_admission) AS month,
  COUNT(*) AS total_admissions
FROM healthcare
GROUP BY year, month
ORDER BY year, month;

-- 2. Average cost per department (medical condition)
SELECT 
  medical_condition,
  ROUND(AVG(billing_amount), 2) AS avg_cost,
  COUNT(*) AS patient_count
FROM healthcare
GROUP BY medical_condition
ORDER BY avg_cost DESC;

-- 3. Top 5 most common diagnoses
SELECT 
  medical_condition,
  COUNT(*) AS diagnosis_count
FROM healthcare
GROUP BY medical_condition
ORDER BY diagnosis_count DESC
LIMIT 5;

-- 4. Total billing by insurance provider
SELECT 
  insurance_provider,
  ROUND(SUM(billing_amount), 2) AS total_billing,
  ROUND(AVG(billing_amount), 2) AS avg_billing,
  COUNT(*) AS claims
FROM healthcare
GROUP BY insurance_provider
ORDER BY total_billing DESC;

-- 5. Average length of stay by medical condition
SELECT 
  medical_condition,
  ROUND(AVG(duration_days), 2) AS avg_stay_days,
  COUNT(*) AS cases
FROM healthcare
GROUP BY medical_condition
ORDER BY avg_stay_days DESC;

-- 6. Admissions by admission type
SELECT 
  admission_type,
  COUNT(*) AS count,
  ROUND(AVG(billing_amount), 2) AS avg_cost
FROM healthcare
GROUP BY admission_type
ORDER BY count DESC;

-- 7. Top 10 doctors by number of patients
SELECT 
  doctor,
  COUNT(*) AS patient_count,
  ROUND(SUM(billing_amount), 2) AS total_revenue
FROM healthcare
GROUP BY doctor
ORDER BY patient_count DESC
LIMIT 10;

-- 8. Window function: Rank hospitals by total revenue
SELECT 
  hospital,
  ROUND(SUM(billing_amount), 2) AS total_revenue,
  COUNT(*) AS admissions,
  RANK() OVER (ORDER BY SUM(billing_amount) DESC) AS revenue_rank
FROM healthcare
GROUP BY hospital
ORDER BY revenue_rank
LIMIT 20;

-- 9. Window function: Running total of billing by month
SELECT 
  EXTRACT(YEAR FROM date_of_admission) AS year,
  EXTRACT(MONTH FROM date_of_admission) AS month,
  ROUND(SUM(billing_amount), 2) AS monthly_billing,
  ROUND(SUM(SUM(billing_amount)) OVER (
    ORDER BY EXTRACT(YEAR FROM date_of_admission), EXTRACT(MONTH FROM date_of_admission)
  ), 2) AS running_total
FROM healthcare
GROUP BY year, month
ORDER BY year, month;

-- 10. Average age and billing by gender and test results
SELECT 
  gender,
  test_results,
  ROUND(AVG(age), 2) AS avg_age,
  ROUND(AVG(billing_amount), 2) AS avg_billing,
  COUNT(*) AS count
FROM healthcare
GROUP BY gender, test_results
ORDER BY count DESC;
