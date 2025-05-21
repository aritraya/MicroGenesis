-- filepath: tests/resource/data_driven_schema.sql
-- Data-Driven Design Database Schema for Healthcare Analytics System
-- Focused on data models, transformation pipelines, and analytics capabilities

-- Raw Data Layer - Source data in normalized form
CREATE TABLE raw_patient_data (
    id BIGINT PRIMARY KEY,
    source_system VARCHAR(50) NOT NULL,
    patient_external_id VARCHAR(100) NOT NULL,
    record_date TIMESTAMP NOT NULL,
    json_data JSONB NOT NULL,
    processing_status VARCHAR(20) DEFAULT 'NEW',
    processing_date TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    batch_id VARCHAR(50) NOT NULL
);

CREATE INDEX idx_raw_patient_processing_status ON raw_patient_data(processing_status);
CREATE INDEX idx_raw_patient_batch_id ON raw_patient_data(batch_id);

CREATE TABLE raw_clinical_events (
    id BIGINT PRIMARY KEY,
    source_system VARCHAR(50) NOT NULL,
    event_external_id VARCHAR(100) NOT NULL,
    event_type VARCHAR(50) NOT NULL,
    event_date TIMESTAMP NOT NULL,
    patient_external_id VARCHAR(100) NOT NULL,
    json_data JSONB NOT NULL,
    processing_status VARCHAR(20) DEFAULT 'NEW',
    processing_date TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    batch_id VARCHAR(50) NOT NULL
);

CREATE INDEX idx_raw_clinical_processing_status ON raw_clinical_events(processing_status);
CREATE INDEX idx_raw_clinical_patient_id ON raw_clinical_events(patient_external_id);
CREATE INDEX idx_raw_clinical_event_type ON raw_clinical_events(event_type);

CREATE TABLE raw_reference_data (
    id BIGINT PRIMARY KEY,
    code_system VARCHAR(50) NOT NULL,
    code VARCHAR(50) NOT NULL,
    display_text VARCHAR(200) NOT NULL,
    json_data JSONB NOT NULL,
    valid_from DATE NOT NULL,
    valid_to DATE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX idx_raw_reference_unique ON raw_reference_data(code_system, code, valid_from);

-- Staging Layer - Cleaned and transformed data
CREATE TABLE staging_patients (
    patient_id VARCHAR(50) PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    birth_date DATE,
    gender VARCHAR(10),
    ethnicity VARCHAR(50),
    zip_code VARCHAR(10),
    insurance_provider VARCHAR(100),
    insurance_id VARCHAR(50),
    processed_timestamp TIMESTAMP NOT NULL,
    source_system VARCHAR(50) NOT NULL,
    source_record_id BIGINT NOT NULL,
    status VARCHAR(20) DEFAULT 'STAGED'
);

CREATE TABLE staging_encounters (
    encounter_id VARCHAR(50) PRIMARY KEY,
    patient_id VARCHAR(50) NOT NULL,
    encounter_date TIMESTAMP NOT NULL,
    encounter_type VARCHAR(50) NOT NULL,
    facility_id VARCHAR(50) NOT NULL,
    provider_id VARCHAR(50),
    admission_date TIMESTAMP,
    discharge_date TIMESTAMP,
    chief_complaint TEXT,
    processed_timestamp TIMESTAMP NOT NULL,
    source_system VARCHAR(50) NOT NULL,
    source_record_id BIGINT NOT NULL,
    status VARCHAR(20) DEFAULT 'STAGED',
    CONSTRAINT fk_staging_patient FOREIGN KEY (patient_id) REFERENCES staging_patients(patient_id)
);

CREATE INDEX idx_staging_encounter_patient ON staging_encounters(patient_id);

CREATE TABLE staging_diagnoses (
    id BIGSERIAL PRIMARY KEY,
    encounter_id VARCHAR(50) NOT NULL,
    patient_id VARCHAR(50) NOT NULL,
    diagnosis_code VARCHAR(20) NOT NULL,
    diagnosis_system VARCHAR(20) NOT NULL,
    diagnosis_description VARCHAR(200) NOT NULL,
    diagnosis_date TIMESTAMP,
    diagnosis_type VARCHAR(50),
    is_primary BOOLEAN DEFAULT FALSE,
    processed_timestamp TIMESTAMP NOT NULL,
    source_system VARCHAR(50) NOT NULL,
    source_record_id BIGINT NOT NULL,
    status VARCHAR(20) DEFAULT 'STAGED',
    CONSTRAINT fk_staging_encounter_diagnosis FOREIGN KEY (encounter_id) REFERENCES staging_encounters(encounter_id),
    CONSTRAINT fk_staging_patient_diagnosis FOREIGN KEY (patient_id) REFERENCES staging_patients(patient_id)
);

CREATE INDEX idx_staging_diagnosis_patient ON staging_diagnoses(patient_id);
CREATE INDEX idx_staging_diagnosis_code ON staging_diagnoses(diagnosis_code);

CREATE TABLE staging_procedures (
    id BIGSERIAL PRIMARY KEY,
    encounter_id VARCHAR(50) NOT NULL,
    patient_id VARCHAR(50) NOT NULL,
    procedure_code VARCHAR(20) NOT NULL,
    procedure_system VARCHAR(20) NOT NULL,
    procedure_description VARCHAR(200) NOT NULL,
    procedure_date TIMESTAMP NOT NULL,
    provider_id VARCHAR(50),
    processed_timestamp TIMESTAMP NOT NULL,
    source_system VARCHAR(50) NOT NULL,
    source_record_id BIGINT NOT NULL,
    status VARCHAR(20) DEFAULT 'STAGED',
    CONSTRAINT fk_staging_encounter_procedure FOREIGN KEY (encounter_id) REFERENCES staging_encounters(encounter_id),
    CONSTRAINT fk_staging_patient_procedure FOREIGN KEY (patient_id) REFERENCES staging_patients(patient_id)
);

CREATE INDEX idx_staging_procedure_patient ON staging_procedures(patient_id);
CREATE INDEX idx_staging_procedure_code ON staging_procedures(procedure_code);

-- Core Data Layer - Clean, integrated data model
CREATE TABLE dim_patients (
    patient_key SERIAL PRIMARY KEY,
    patient_id VARCHAR(50) UNIQUE NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    birth_date DATE NOT NULL,
    gender VARCHAR(10) NOT NULL,
    ethnicity VARCHAR(50),
    current_zip_code VARCHAR(10),
    is_active BOOLEAN DEFAULT TRUE,
    created_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_dim_patient_id ON dim_patients(patient_id);

CREATE TABLE dim_facilities (
    facility_key SERIAL PRIMARY KEY,
    facility_id VARCHAR(50) UNIQUE NOT NULL,
    facility_name VARCHAR(100) NOT NULL,
    facility_type VARCHAR(50) NOT NULL,
    address_line1 VARCHAR(100),
    address_line2 VARCHAR(100),
    city VARCHAR(50),
    state VARCHAR(20),
    zip_code VARCHAR(10),
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6),
    is_active BOOLEAN DEFAULT TRUE,
    created_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE dim_providers (
    provider_key SERIAL PRIMARY KEY,
    provider_id VARCHAR(50) UNIQUE NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    specialty VARCHAR(100),
    npi VARCHAR(20),
    is_active BOOLEAN DEFAULT TRUE,
    created_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE dim_dates (
    date_key INT PRIMARY KEY,  -- YYYYMMDD format
    full_date DATE UNIQUE NOT NULL,
    day_of_week INT NOT NULL,
    day_name VARCHAR(10) NOT NULL,
    day_of_month INT NOT NULL,
    day_of_year INT NOT NULL,
    week_of_year INT NOT NULL,
    month INT NOT NULL,
    month_name VARCHAR(10) NOT NULL,
    quarter INT NOT NULL,
    year INT NOT NULL,
    is_weekday BOOLEAN NOT NULL,
    is_holiday BOOLEAN DEFAULT FALSE
);

CREATE TABLE fact_encounters (
    encounter_key BIGSERIAL PRIMARY KEY,
    encounter_id VARCHAR(50) UNIQUE NOT NULL,
    patient_key INT NOT NULL,
    facility_key INT NOT NULL,
    provider_key INT,
    admission_date_key INT,
    discharge_date_key INT,
    encounter_type VARCHAR(50) NOT NULL,
    los_days INT,
    emergency_admission BOOLEAN DEFAULT FALSE,
    icu_stay BOOLEAN DEFAULT FALSE,
    total_charges DECIMAL(12,2),
    created_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_fact_encounters_patient FOREIGN KEY (patient_key) REFERENCES dim_patients(patient_key),
    CONSTRAINT fk_fact_encounters_facility FOREIGN KEY (facility_key) REFERENCES dim_facilities(facility_key),
    CONSTRAINT fk_fact_encounters_provider FOREIGN KEY (provider_key) REFERENCES dim_providers(provider_key),
    CONSTRAINT fk_fact_encounters_admit_date FOREIGN KEY (admission_date_key) REFERENCES dim_dates(date_key),
    CONSTRAINT fk_fact_encounters_discharge_date FOREIGN KEY (discharge_date_key) REFERENCES dim_dates(date_key)
);

CREATE INDEX idx_fact_encounters_patient ON fact_encounters(patient_key);
CREATE INDEX idx_fact_encounters_dates ON fact_encounters(admission_date_key, discharge_date_key);

CREATE TABLE fact_diagnoses (
    diagnosis_key BIGSERIAL PRIMARY KEY,
    encounter_key BIGINT NOT NULL,
    patient_key INT NOT NULL,
    diagnosis_date_key INT NOT NULL,
    diagnosis_code VARCHAR(20) NOT NULL,
    diagnosis_system VARCHAR(20) NOT NULL,
    diagnosis_description VARCHAR(200) NOT NULL,
    is_primary BOOLEAN DEFAULT FALSE,
    is_admission_diagnosis BOOLEAN DEFAULT FALSE,
    is_discharge_diagnosis BOOLEAN DEFAULT FALSE,
    created_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_fact_diagnoses_encounter FOREIGN KEY (encounter_key) REFERENCES fact_encounters(encounter_key),
    CONSTRAINT fk_fact_diagnoses_patient FOREIGN KEY (patient_key) REFERENCES dim_patients(patient_key),
    CONSTRAINT fk_fact_diagnoses_date FOREIGN KEY (diagnosis_date_key) REFERENCES dim_dates(date_key)
);

CREATE INDEX idx_fact_diagnoses_patient ON fact_diagnoses(patient_key);
CREATE INDEX idx_fact_diagnoses_code ON fact_diagnoses(diagnosis_code);

CREATE TABLE fact_procedures (
    procedure_key BIGSERIAL PRIMARY KEY,
    encounter_key BIGINT NOT NULL,
    patient_key INT NOT NULL,
    procedure_date_key INT NOT NULL,
    provider_key INT,
    procedure_code VARCHAR(20) NOT NULL,
    procedure_system VARCHAR(20) NOT NULL,
    procedure_description VARCHAR(200) NOT NULL,
    procedure_cost DECIMAL(12,2),
    created_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_fact_procedures_encounter FOREIGN KEY (encounter_key) REFERENCES fact_encounters(encounter_key),
    CONSTRAINT fk_fact_procedures_patient FOREIGN KEY (patient_key) REFERENCES dim_patients(patient_key),
    CONSTRAINT fk_fact_procedures_date FOREIGN KEY (procedure_date_key) REFERENCES dim_dates(date_key),
    CONSTRAINT fk_fact_procedures_provider FOREIGN KEY (provider_key) REFERENCES dim_providers(provider_key)
);

CREATE INDEX idx_fact_procedures_patient ON fact_procedures(patient_key);
CREATE INDEX idx_fact_procedures_code ON fact_procedures(procedure_code);

CREATE TABLE fact_vitals (
    vital_key BIGSERIAL PRIMARY KEY,
    encounter_key BIGINT NOT NULL,
    patient_key INT NOT NULL,
    measurement_date_key INT NOT NULL,
    measurement_datetime TIMESTAMP NOT NULL,
    vital_type VARCHAR(50) NOT NULL,
    vital_value DECIMAL(10,4) NOT NULL,
    vital_unit VARCHAR(20) NOT NULL,
    created_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_fact_vitals_encounter FOREIGN KEY (encounter_key) REFERENCES fact_encounters(encounter_key),
    CONSTRAINT fk_fact_vitals_patient FOREIGN KEY (patient_key) REFERENCES dim_patients(patient_key),
    CONSTRAINT fk_fact_vitals_date FOREIGN KEY (measurement_date_key) REFERENCES dim_dates(date_key)
);

CREATE INDEX idx_fact_vitals_patient ON fact_vitals(patient_key);
CREATE INDEX idx_fact_vitals_type ON fact_vitals(vital_type);

-- Analytics Layer - Pre-computed aggregates and metrics
CREATE TABLE agg_patient_metrics (
    patient_key INT PRIMARY KEY,
    total_encounters INT NOT NULL DEFAULT 0,
    total_emergency_visits INT NOT NULL DEFAULT 0,
    total_inpatient_admissions INT NOT NULL DEFAULT 0,
    total_procedures INT NOT NULL DEFAULT 0,
    avg_los DECIMAL(5,2),
    readmission_30day_count INT NOT NULL DEFAULT 0,
    readmission_30day_rate DECIMAL(5,4),
    comorbidity_count INT NOT NULL DEFAULT 0,
    risk_score DECIMAL(5,2),
    last_calculated_date TIMESTAMP NOT NULL,
    CONSTRAINT fk_agg_patient_metrics_patient FOREIGN KEY (patient_key) REFERENCES dim_patients(patient_key)
);

CREATE TABLE agg_facility_metrics (
    facility_key INT PRIMARY KEY,
    calculation_period VARCHAR(20) NOT NULL, -- 'CURRENT_MONTH', 'PREVIOUS_MONTH', 'CURRENT_YEAR'
    total_encounters INT NOT NULL DEFAULT 0,
    avg_daily_census DECIMAL(5,2),
    avg_los DECIMAL(5,2),
    readmission_30day_rate DECIMAL(5,4),
    mortality_rate DECIMAL(5,4),
    er_wait_time_avg_minutes DECIMAL(6,2),
    bed_utilization_rate DECIMAL(5,4),
    last_calculated_date TIMESTAMP NOT NULL,
    CONSTRAINT fk_agg_facility_metrics_facility FOREIGN KEY (facility_key) REFERENCES dim_facilities(facility_key)
);

CREATE TABLE agg_population_health (
    population_segment_id VARCHAR(50) PRIMARY KEY,
    segment_name VARCHAR(100) NOT NULL,
    segment_criteria JSONB NOT NULL,
    patient_count INT NOT NULL DEFAULT 0,
    age_avg DECIMAL(5,2),
    gender_distribution JSONB,
    top_diagnoses JSONB,
    risk_score_avg DECIMAL(5,2),
    utilization_metrics JSONB,
    cost_metrics JSONB,
    outcome_metrics JSONB,
    last_calculated_date TIMESTAMP NOT NULL
);

-- Data Pipeline Control Tables
CREATE TABLE pipeline_jobs (
    job_id VARCHAR(50) PRIMARY KEY,
    job_name VARCHAR(100) NOT NULL,
    job_type VARCHAR(50) NOT NULL,
    parameters JSONB NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'PENDING',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    error_message TEXT,
    records_processed INT DEFAULT 0,
    created_by VARCHAR(50) NOT NULL
);

CREATE TABLE pipeline_job_steps (
    step_id BIGSERIAL PRIMARY KEY,
    job_id VARCHAR(50) NOT NULL,
    step_name VARCHAR(100) NOT NULL,
    step_order INT NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'PENDING',
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    records_processed INT DEFAULT 0,
    error_message TEXT,
    CONSTRAINT fk_pipeline_job_steps_job FOREIGN KEY (job_id) REFERENCES pipeline_jobs(job_id)
);

CREATE INDEX idx_pipeline_job_steps_job ON pipeline_job_steps(job_id);

-- Views for Analysis
CREATE VIEW vw_patient_encounter_summary AS
SELECT 
    dp.patient_key,
    dp.patient_id,
    dp.birth_date,
    dp.gender,
    dp.ethnicity,
    dp.current_zip_code,
    COUNT(fe.encounter_key) AS total_encounters,
    SUM(CASE WHEN fe.encounter_type = 'INPATIENT' THEN 1 ELSE 0 END) AS inpatient_encounters,
    SUM(CASE WHEN fe.encounter_type = 'EMERGENCY' THEN 1 ELSE 0 END) AS emergency_encounters,
    SUM(CASE WHEN fe.encounter_type = 'OUTPATIENT' THEN 1 ELSE 0 END) AS outpatient_encounters,
    AVG(fe.los_days) AS avg_length_of_stay,
    MIN(dd_admit.full_date) AS first_encounter_date,
    MAX(dd_admit.full_date) AS last_encounter_date
FROM 
    dim_patients dp
LEFT JOIN 
    fact_encounters fe ON dp.patient_key = fe.patient_key
LEFT JOIN 
    dim_dates dd_admit ON fe.admission_date_key = dd_admit.date_key
GROUP BY
    dp.patient_key, dp.patient_id, dp.birth_date, dp.gender, dp.ethnicity, dp.current_zip_code;

CREATE VIEW vw_diagnosis_prevalence AS
SELECT 
    fd.diagnosis_code,
    fd.diagnosis_description,
    COUNT(DISTINCT fd.patient_key) AS affected_patients,
    COUNT(fd.diagnosis_key) AS total_diagnoses,
    COUNT(DISTINCT fd.patient_key) * 100.0 / (SELECT COUNT(*) FROM dim_patients) AS prevalence_percentage
FROM 
    fact_diagnoses fd
GROUP BY 
    fd.diagnosis_code, fd.diagnosis_description
ORDER BY 
    affected_patients DESC;

CREATE VIEW vw_readmission_analysis AS
WITH patient_admissions AS (
    SELECT 
        fe.patient_key,
        fe.encounter_key,
        fe.encounter_id,
        dd_admit.full_date AS admission_date,
        dd_discharge.full_date AS discharge_date,
        fe.encounter_type,
        LEAD(dd_admit.full_date) OVER (
            PARTITION BY fe.patient_key 
            ORDER BY dd_admit.full_date
        ) AS next_admission_date
    FROM 
        fact_encounters fe
    JOIN 
        dim_dates dd_admit ON fe.admission_date_key = dd_admit.date_key
    LEFT JOIN 
        dim_dates dd_discharge ON fe.discharge_date_key = dd_discharge.date_key
    WHERE 
        fe.encounter_type = 'INPATIENT'
)
SELECT
    pa.patient_key,
    pa.encounter_key,
    pa.encounter_id,
    pa.admission_date,
    pa.discharge_date,
    pa.next_admission_date,
    CASE 
        WHEN pa.next_admission_date IS NOT NULL AND 
             pa.next_admission_date <= (pa.discharge_date + INTERVAL '30 days') 
        THEN TRUE 
        ELSE FALSE 
    END AS is_30day_readmission
FROM 
    patient_admissions pa;

-- Materialized view for operational analytics
CREATE MATERIALIZED VIEW mvw_monthly_facility_metrics AS
SELECT
    df.facility_key,
    df.facility_id,
    df.facility_name,
    dd.year,
    dd.month,
    dd.month_name,
    COUNT(DISTINCT fe.encounter_key) AS total_encounters,
    COUNT(DISTINCT fe.patient_key) AS unique_patients,
    ROUND(AVG(fe.los_days), 2) AS avg_length_of_stay,
    SUM(CASE WHEN fe.emergency_admission THEN 1 ELSE 0 END) AS emergency_admissions,
    SUM(CASE WHEN fe.icu_stay THEN 1 ELSE 0 END) AS icu_admissions,
    SUM(fe.total_charges) AS total_charges,
    ROUND(AVG(fe.total_charges), 2) AS avg_charges
FROM
    fact_encounters fe
JOIN
    dim_facilities df ON fe.facility_key = df.facility_key
JOIN
    dim_dates dd ON fe.admission_date_key = dd.date_key
GROUP BY
    df.facility_key, df.facility_id, df.facility_name, dd.year, dd.month, dd.month_name
WITH DATA;

CREATE UNIQUE INDEX idx_mvw_monthly_facility_metrics ON mvw_monthly_facility_metrics (facility_key, year, month);

-- Functions for pipeline operations
CREATE OR REPLACE FUNCTION update_patient_metrics(p_batch_size INT DEFAULT 1000)
RETURNS INT AS $$
DECLARE
    v_count INT := 0;
    v_last_patient_key INT := 0;
BEGIN
    LOOP
        -- Process batch of patients
        WITH patient_batch AS (
            SELECT patient_key 
            FROM dim_patients 
            WHERE patient_key > v_last_patient_key
            ORDER BY patient_key
            LIMIT p_batch_size
        ),
        patient_metrics AS (
            SELECT
                pb.patient_key,
                COUNT(fe.encounter_key) AS total_encounters,
                SUM(CASE WHEN fe.encounter_type = 'EMERGENCY' THEN 1 ELSE 0 END) AS total_emergency_visits,
                SUM(CASE WHEN fe.encounter_type = 'INPATIENT' THEN 1 ELSE 0 END) AS total_inpatient_admissions,
                COUNT(fp.procedure_key) AS total_procedures,
                AVG(fe.los_days) AS avg_los,
                COUNT(DISTINCT CASE 
                    WHEN vra.is_30day_readmission THEN vra.encounter_key 
                    ELSE NULL 
                END) AS readmission_30day_count,
                CASE 
                    WHEN SUM(CASE WHEN fe.encounter_type = 'INPATIENT' THEN 1 ELSE 0 END) > 0 
                    THEN CAST(COUNT(DISTINCT CASE WHEN vra.is_30day_readmission THEN vra.encounter_key ELSE NULL END) AS DECIMAL) / 
                         SUM(CASE WHEN fe.encounter_type = 'INPATIENT' THEN 1 ELSE 0 END)
                    ELSE 0 
                END AS readmission_30day_rate,
                COUNT(DISTINCT fd.diagnosis_code) AS comorbidity_count,
                -- Simple risk score calculation based on age, encounters, and comorbidities
                (
                    CAST(EXTRACT(YEAR FROM CURRENT_DATE) - EXTRACT(YEAR FROM dp.birth_date) AS DECIMAL) * 0.05 +
                    COUNT(fe.encounter_key) * 0.2 +
                    COUNT(DISTINCT fd.diagnosis_code) * 0.3 +
                    COUNT(DISTINCT CASE WHEN vra.is_30day_readmission THEN vra.encounter_key ELSE NULL END) * 2.0
                ) AS risk_score
            FROM
                patient_batch pb
            JOIN
                dim_patients dp ON pb.patient_key = dp.patient_key
            LEFT JOIN
                fact_encounters fe ON pb.patient_key = fe.patient_key
            LEFT JOIN
                vw_readmission_analysis vra ON fe.encounter_key = vra.encounter_key
            LEFT JOIN
                fact_diagnoses fd ON pb.patient_key = fd.patient_key
            LEFT JOIN
                fact_procedures fp ON pb.patient_key = fp.patient_key
            GROUP BY
                pb.patient_key, dp.birth_date
        )
        INSERT INTO agg_patient_metrics (
            patient_key, total_encounters, total_emergency_visits, 
            total_inpatient_admissions, total_procedures, avg_los,
            readmission_30day_count, readmission_30day_rate, 
            comorbidity_count, risk_score, last_calculated_date
        )
        SELECT 
            pm.patient_key, pm.total_encounters, pm.total_emergency_visits,
            pm.total_inpatient_admissions, pm.total_procedures, pm.avg_los,
            pm.readmission_30day_count, pm.readmission_30day_rate,
            pm.comorbidity_count, pm.risk_score, CURRENT_TIMESTAMP
        FROM 
            patient_metrics pm
        ON CONFLICT (patient_key) DO UPDATE SET
            total_encounters = EXCLUDED.total_encounters,
            total_emergency_visits = EXCLUDED.total_emergency_visits,
            total_inpatient_admissions = EXCLUDED.total_inpatient_admissions,
            total_procedures = EXCLUDED.total_procedures,
            avg_los = EXCLUDED.avg_los,
            readmission_30day_count = EXCLUDED.readmission_30day_count,
            readmission_30day_rate = EXCLUDED.readmission_30day_rate,
            comorbidity_count = EXCLUDED.comorbidity_count,
            risk_score = EXCLUDED.risk_score,
            last_calculated_date = CURRENT_TIMESTAMP;
            
        -- Get count and last patient key for next iteration
        GET DIAGNOSTICS v_count = ROW_COUNT;
        
        IF v_count = 0 THEN
            -- No more patients to process
            EXIT;
        END IF;
        
        -- Get the last processed patient_key
        SELECT MAX(patient_key) INTO v_last_patient_key
        FROM patient_batch;
        
        -- Exit if we processed less than the batch size (reached the end)
        EXIT WHEN v_count < p_batch_size;
    END LOOP;
    
    RETURN v_last_patient_key;
END;
$$ LANGUAGE plpgsql;

-- Triggers for data quality checks
CREATE OR REPLACE FUNCTION check_date_consistency()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.discharge_date_key IS NOT NULL AND NEW.admission_date_key > NEW.discharge_date_key THEN
        RAISE EXCEPTION 'Invalid dates: discharge date cannot be earlier than admission date';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_check_encounter_dates
BEFORE INSERT OR UPDATE ON fact_encounters
FOR EACH ROW
EXECUTE FUNCTION check_date_consistency();
