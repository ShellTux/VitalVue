% VitalVue
% João Alves, Luís Góis, Marco Silva
% \today

---

# Entity Relation Diagram

![Entity Relation Diagram](/assets/er-diagram.png)

---

# Postgres Setup

db-config:

::: incremental

1. `01-setup.sql`
2. `02-functions.sql`
3. `03-triggers.sql`

:::

---

# Add Patient, Doctor, Nurse, and Assistant.

---

# User Authentication.

---

# Schedule Appointment.

```sql
INSERT INTO 
    appointment (
        doctor_employee_vital_vue_user_id,
        scheduled_date,
        start_time,
        end_time,
        cost,
        patient_vital_vue_user_id
    )
VALUES (
    %s, %s, %s, %s, %s, %s
)
RETURNING 
    id;
```

---

# See Appointments.

```sql
SELECT 
    ap.id,
    ap.doctor_employee_vital_vue_user_id,
    ap.scheduled_date
FROM 
    appointment AS ap
WHERE 
    ap.patient_vital_vue_user_id = %s
```

---

# Schedule Surgery.

## Schedule Surgery - SQL Part 1

```sql
WITH new_surgery AS (
    INSERT INTO surgery (
        {hosp_id_column}
        patient_vital_vue_user_id,
        doctor_employee_vital_vue_user_id,
        scheduled_date,
        start_time,
        end_time
    )
    VALUES (
        {surgery_params}
    )
    RETURNING
        hospitalization_id,
        id,
        patient_vital_vue_user_id,
        doctor_employee_vital_vue_user_id,
        scheduled_date
)
```

---

## Schedule Surgery - SQL Part 2

```sql
, new_nurses AS (
    INSERT INTO nurse_role (
        surgery_id,
        nurse_employee_vital_vue_user_id,
        role
    )
    SELECT
        ns.id,
        nurse_employee_vital_vue_user_id,
        role
    FROM 
        new_surgery ns,
        (VALUES {nurse_params}) AS nurse_role (
            nurse_employee_vital_vue_user_id, 
            role
        )
)
```

---

## Schedule Surgery - SQL Part 3

```sql
SELECT 
    hospitalization_id,
    id,
    patient_vital_vue_user_id,
    doctor_employee_vital_vue_user_id,
    scheduled_date
FROM
    new_surgery;
```

---

# Get Prescriptions.

```sql
SELECT 
    p.id, 
    p.validity_date,
    mp.dose,
    mp.frequency,
    mp.medication_name
FROM 
    prescription AS p
LEFT JOIN
    med_posology AS mp
ON
    p.id = mp.prescription_id
WHERE 
    p.patient_vital_vue_user_id = %s;
```

---

# Add Prescriptions.

```sql
WITH new_prescription AS (
    INSERT INTO prescription ({event_id_column}, validity_date)
    VALUES (%s, %s)
    RETURNING id
), new_posology AS (
    INSERT INTO med_posology (prescription_id, medication_name, dose, frequency)
    SELECT np.id, mp.medication_name, mp.dose, mp.frequency
    FROM new_prescription np,
        (VALUES {med_pos_params}) AS mp (medication_name, dose, frequency)
)
SELECT id
FROM new_prescription;
```

---

# Execute Payment.

---

# List Top 3 patients.

---

# Daily Summary.

```sql
SELECT
    SUM(payment.amount) AS "Amount Spent",
    COUNT(surgery.id) AS "Surgeries",
    COUNT(prescription.id) AS Prescriptions
FROM hospitalization
LEFT JOIN
    hospitalization_bill ON hospitalization.id = hospitalization_bill.hospitalization_id
LEFT JOIN
    bill ON hospitalization_bill.bill_id = bill.id
LEFT JOIN
    payment ON bill.id = payment.bill_id
LEFT JOIN
    surgery ON hospitalization.id = surgery.hospitalization_id
LEFT JOIN
    prescription ON hospitalization.id = prescription.hospitalization_id
WHERE
    hospitalization.assistant_employee_vital_vue_user_id IN (SELECT employee_vital_vue_user_id FROM assistant)
GROUP BY
    date(scheduled_date);
```

---

# Generate a monthly report.

```sql
SELECT
    EXTRACT(MONTH FROM s.scheduled_date) AS Mês,
    e.name as "Nome do Doctor",
    COUNT(s.scheduled_date) as "Total de cirurgias"
FROM
    employee e
JOIN
    doctor d ON e.vital_vue_user_id = d.employee_vital_vue_user_id
JOIN
    surgery s ON d.employee_vital_vue_user_id = s.doctor_employee_vital_vue_user_id
WHERE
    s.scheduled_date >= DATE_TRUNC('month', NOW() - INTERVAL '12 months')
GROUP BY
    e.name, EXTRACT(MONTH FROM s.scheduled_date)
ORDER BY
    "Total de cirurgias" DESC;
```

---

# Conclusion

Thanks for your attention
