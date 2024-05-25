-- vim: foldmethod=marker

-- Register Individual {{{

CREATE OR REPLACE PROCEDURE register_patient (
	patient_username vital_vue_user.username%TYPE,
	patient_password vital_vue_user.password%TYPE,
	patient_email vital_vue_user.email%TYPE,
	patient_name patient.name%TYPE
)
LANGUAGE plpgsql
AS $$
BEGIN
	WITH new_user AS (
		INSERT INTO vital_vue_user (username, password, email, type)
		VALUES (
			patient_username,
			patient_password,
			patient_email,
			'patient'
		)
		RETURNING id
	)
	INSERT INTO patient (vital_vue_user_id, name)
	SELECT id, patient_name
	FROM new_user;
	-- TODO: RETURNING vital_vue_user_id;
END;
$$;

CREATE OR REPLACE PROCEDURE register_assistant (
	assistant_username vital_vue_user.username%TYPE,
	assistant_password vital_vue_user.password%TYPE,
	assistant_email vital_vue_user.email%TYPE,
	assistant_name employee.name%TYPE,
	assistant_contract_details employee.contract_details%TYPE
)
LANGUAGE plpgsql
AS $$
BEGIN
	WITH new_user AS (
		INSERT INTO vital_vue_user (username, password, email, type)
		VALUES (
			assistant_username,
			assistant_password,
			assistant_email,
			'assistant'
		)
		RETURNING id
		), new_employee AS (
		INSERT INTO employee (name, contract_details, vital_vue_user_id)
		SELECT assistant_name, assistant_contract_details, id FROM new_user
		RETURNING vital_vue_user_id
	)
	INSERT INTO assistant (employee_vital_vue_user_id)
	SELECT vital_vue_user_id
	FROM new_employee;
	-- TODO: RETURNING employee_vital_vue_user_id;
END;
$$;

CREATE OR REPLACE PROCEDURE register_nurse (
	nurse_username vital_vue_user.username%TYPE,
	nurse_password vital_vue_user.password%TYPE,
	nurse_email vital_vue_user.email%TYPE,
	nurse_name employee.name%TYPE,
	nurse_contract_details employee.contract_details%TYPE,
	nurse_category nurse.category%TYPE
)
LANGUAGE plpgsql
AS $$
BEGIN
	WITH new_user AS (
		INSERT INTO vital_vue_user (username, password, email, type)
		VALUES (nurse_username, nurse_password, nurse_email, 'nurse')
		RETURNING id
		), new_employee AS (
		INSERT INTO employee (name, contract_details, vital_vue_user_id)
		SELECT nurse_name, nurse_contract_details, id FROM new_user
		RETURNING vital_vue_user_id
	)
	INSERT INTO nurse (category, employee_vital_vue_user_id)
	SELECT nurse_category, vital_vue_user_id
	FROM new_employee;
	-- TODO: RETURNING employee_vital_vue_user_id;
END;
$$;

CREATE OR REPLACE PROCEDURE register_doctor (
	doctor_username vital_vue_user.username%TYPE,
	doctor_password vital_vue_user.password%TYPE,
	doctor_email vital_vue_user.email%TYPE,
	doctor_name employee.name%TYPE,
	doctor_contract_details employee.contract_details%TYPE,
	doctor_license doctor.license%TYPE
)
LANGUAGE plpgsql
AS $$
BEGIN
	WITH new_user AS (
		INSERT INTO vital_vue_user (username, password, email, type)
		VALUES (
			doctor_username,
			doctor_password,
			doctor_email,
			'doctor'
		)
		RETURNING id
	), new_employee AS (
		INSERT INTO employee (name, contract_details, vital_vue_user_id)
		SELECT doctor_name, doctor_contract_details, id FROM new_user
		RETURNING vital_vue_user_id
	)
	INSERT INTO doctor (license, employee_vital_vue_user_id)
	SELECT doctor_license, vital_vue_user_id
	FROM new_employee;
	-- TODO: RETURNING employee_vital_vue_user_id;
END;
$$;

--- }}}

CREATE OR REPLACE FUNCTION create_bill_after_insert()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO bill (cost, paid)
    VALUES (NEW.cost, FALSE);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
