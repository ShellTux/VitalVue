CREATE TABLE employee (
	name		 VARCHAR(512),
	contract_details	 TEXT NOT NULL,
	vital_vue_user_id BIGINT,
	PRIMARY KEY(vital_vue_user_id)
);

CREATE TABLE doctor (
	license			 TEXT NOT NULL,
	employee_vital_vue_user_id BIGINT,
	PRIMARY KEY(employee_vital_vue_user_id)
);

CREATE TABLE nurse (
	category			 TEXT NOT NULL,
	employee_vital_vue_user_id BIGINT,
	PRIMARY KEY(employee_vital_vue_user_id)
);

CREATE TABLE assistant (
	employee_vital_vue_user_id BIGINT,
	PRIMARY KEY(employee_vital_vue_user_id)
);

CREATE TABLE patient (
	name		 VARCHAR(512),
	vital_vue_user_id BIGINT,
	PRIMARY KEY(vital_vue_user_id)
);

CREATE TABLE appointment (
	id					 BIGSERIAL,
	scheduled_date			 DATE NOT NULL,
	start_time				 TIMESTAMP NOT NULL,
	end_time				 TIMESTAMP NOT NULL,
	patient_vital_vue_user_id		 BIGINT NOT NULL,
	assistant_employee_vital_vue_user_id BIGINT,
	bill_id				 BIGINT NOT NULL,
	doctor_employee_vital_vue_user_id	 BIGINT NOT NULL,
	PRIMARY KEY(id)
);

CREATE TABLE surgery (
	id				 BIGSERIAL,
	scheduled_date			 DATE NOT NULL,
	start_time			 TIMESTAMP NOT NULL,
	end_time				 TIMESTAMP NOT NULL,
	patient_vital_vue_user_id	 BIGINT NOT NULL,
	hospitalization_id		 BIGINT NOT NULL,
	doctor_employee_vital_vue_user_id BIGINT NOT NULL,
	PRIMARY KEY(id)
);

CREATE TABLE hospitalization (
	id					 BIGINT,
	patient_vital_vue_user_id		 BIGINT NOT NULL,
	assistant_employee_vital_vue_user_id BIGINT NOT NULL,
	nurse_employee_vital_vue_user_id	 BIGINT NOT NULL,
	PRIMARY KEY(id)
);

CREATE TABLE nurse_role (
	role				 TEXT NOT NULL,
	appointment_id			 BIGINT NOT NULL,
	nurse_employee_vital_vue_user_id BIGINT NOT NULL,
	surgery_id			 BIGINT NOT NULL
);

CREATE TABLE prescription (
	id			 BIGINT,
	validity_date		 DATE NOT NULL,
	patient_vital_vue_user_id BIGINT NOT NULL,
	hospitalization_id	 BIGINT NOT NULL,
	appointment_id		 BIGINT NOT NULL,
	PRIMARY KEY(id)
);

CREATE TABLE medication (
	id	 BIGINT,
	name TEXT,
	PRIMARY KEY(id)
);

CREATE TABLE side_effect (
	effect TEXT,
	PRIMARY KEY(effect)
);

CREATE TABLE med_occ_sev (
	probability	 FLOAT(8) NOT NULL,
	severity		 BIGINT NOT NULL,
	side_effect_effect TEXT,
	medication_id	 BIGINT,
	PRIMARY KEY(side_effect_effect,medication_id)
);

CREATE TABLE specialization (
	field TEXT,
	PRIMARY KEY(field)
);

CREATE TABLE bill (
	id	 BIGINT,
	cost BIGINT NOT NULL,
	paid BOOL,
	PRIMARY KEY(id)
);

CREATE TABLE payment (
	id			 BIGINT,
	pay_date			 DATE NOT NULL,
	amount			 BIGINT NOT NULL,
	patient_vital_vue_user_id BIGINT NOT NULL,
	bill_id			 BIGINT NOT NULL,
	PRIMARY KEY(id)
);

CREATE TABLE medication_dosage (
	dosage		 BIGINT NOT NULL,
	prescription_id BIGINT NOT NULL,
	medication_id	 BIGINT,
	PRIMARY KEY(medication_id)
);

CREATE TABLE vital_vue_user (
	id	 BIGSERIAL,
	username TEXT NOT NULL,
	password TEXT NOT NULL,
	email	 TEXT NOT NULL,
	type	 VARCHAR(512) NOT NULL,
	PRIMARY KEY(id)
);

CREATE TABLE hospitalization_bill (
	hospitalization_id BIGINT,
	bill_id		 BIGINT NOT NULL,
	PRIMARY KEY(hospitalization_id)
);

CREATE TABLE specialization_specialization (
	specialization_field	 TEXT,
	specialization_field1 TEXT NOT NULL,
	PRIMARY KEY(specialization_field)
);

CREATE TABLE doctor_specialization (
	doctor_employee_vital_vue_user_id BIGINT NOT NULL,
	specialization_field		 TEXT,
	PRIMARY KEY(specialization_field)
);

ALTER TABLE employee ADD CONSTRAINT employee_fk1 FOREIGN KEY (vital_vue_user_id) REFERENCES vital_vue_user(id);
ALTER TABLE doctor ADD CONSTRAINT doctor_fk1 FOREIGN KEY (employee_vital_vue_user_id) REFERENCES employee(vital_vue_user_id);
ALTER TABLE nurse ADD CONSTRAINT nurse_fk1 FOREIGN KEY (employee_vital_vue_user_id) REFERENCES employee(vital_vue_user_id);
ALTER TABLE assistant ADD CONSTRAINT assistant_fk1 FOREIGN KEY (employee_vital_vue_user_id) REFERENCES employee(vital_vue_user_id);
ALTER TABLE patient ADD CONSTRAINT patient_fk1 FOREIGN KEY (vital_vue_user_id) REFERENCES vital_vue_user(id);
ALTER TABLE appointment ADD UNIQUE (bill_id);
ALTER TABLE appointment ADD CONSTRAINT appointment_fk1 FOREIGN KEY (patient_vital_vue_user_id) REFERENCES patient(vital_vue_user_id);
ALTER TABLE appointment ADD CONSTRAINT appointment_fk2 FOREIGN KEY (assistant_employee_vital_vue_user_id) REFERENCES assistant(employee_vital_vue_user_id);
ALTER TABLE appointment ADD CONSTRAINT appointment_fk3 FOREIGN KEY (bill_id) REFERENCES bill(id);
ALTER TABLE appointment ADD CONSTRAINT appointment_fk4 FOREIGN KEY (doctor_employee_vital_vue_user_id) REFERENCES doctor(employee_vital_vue_user_id);
ALTER TABLE surgery ADD CONSTRAINT surgery_fk1 FOREIGN KEY (patient_vital_vue_user_id) REFERENCES patient(vital_vue_user_id);
ALTER TABLE surgery ADD CONSTRAINT surgery_fk2 FOREIGN KEY (hospitalization_id) REFERENCES hospitalization(id);
ALTER TABLE surgery ADD CONSTRAINT surgery_fk3 FOREIGN KEY (doctor_employee_vital_vue_user_id) REFERENCES doctor(employee_vital_vue_user_id);
ALTER TABLE hospitalization ADD CONSTRAINT hospitalization_fk1 FOREIGN KEY (patient_vital_vue_user_id) REFERENCES patient(vital_vue_user_id);
ALTER TABLE hospitalization ADD CONSTRAINT hospitalization_fk2 FOREIGN KEY (assistant_employee_vital_vue_user_id) REFERENCES assistant(employee_vital_vue_user_id);
ALTER TABLE hospitalization ADD CONSTRAINT hospitalization_fk3 FOREIGN KEY (nurse_employee_vital_vue_user_id) REFERENCES nurse(employee_vital_vue_user_id);
ALTER TABLE nurse_role ADD CONSTRAINT nurse_role_fk1 FOREIGN KEY (appointment_id) REFERENCES appointment(id);
ALTER TABLE nurse_role ADD CONSTRAINT nurse_role_fk2 FOREIGN KEY (nurse_employee_vital_vue_user_id) REFERENCES nurse(employee_vital_vue_user_id);
ALTER TABLE nurse_role ADD CONSTRAINT nurse_role_fk3 FOREIGN KEY (surgery_id) REFERENCES surgery(id);
ALTER TABLE prescription ADD CONSTRAINT prescription_fk1 FOREIGN KEY (patient_vital_vue_user_id) REFERENCES patient(vital_vue_user_id);
ALTER TABLE prescription ADD CONSTRAINT prescription_fk2 FOREIGN KEY (hospitalization_id) REFERENCES hospitalization(id);
ALTER TABLE prescription ADD CONSTRAINT prescription_fk3 FOREIGN KEY (appointment_id) REFERENCES appointment(id);
ALTER TABLE med_occ_sev ADD CONSTRAINT med_occ_sev_fk1 FOREIGN KEY (side_effect_effect) REFERENCES side_effect(effect);
ALTER TABLE med_occ_sev ADD CONSTRAINT med_occ_sev_fk2 FOREIGN KEY (medication_id) REFERENCES medication(id);
ALTER TABLE payment ADD CONSTRAINT payment_fk1 FOREIGN KEY (patient_vital_vue_user_id) REFERENCES patient(vital_vue_user_id);
ALTER TABLE payment ADD CONSTRAINT payment_fk2 FOREIGN KEY (bill_id) REFERENCES bill(id);
ALTER TABLE medication_dosage ADD CONSTRAINT medication_dosage_fk1 FOREIGN KEY (prescription_id) REFERENCES prescription(id);
ALTER TABLE medication_dosage ADD CONSTRAINT medication_dosage_fk2 FOREIGN KEY (medication_id) REFERENCES medication(id);
ALTER TABLE vital_vue_user ADD UNIQUE (username, email);
ALTER TABLE hospitalization_bill ADD UNIQUE (bill_id);
ALTER TABLE hospitalization_bill ADD CONSTRAINT hospitalization_bill_fk1 FOREIGN KEY (hospitalization_id) REFERENCES hospitalization(id);
ALTER TABLE hospitalization_bill ADD CONSTRAINT hospitalization_bill_fk2 FOREIGN KEY (bill_id) REFERENCES bill(id);
ALTER TABLE specialization_specialization ADD CONSTRAINT specialization_specialization_fk1 FOREIGN KEY (specialization_field) REFERENCES specialization(field);
ALTER TABLE specialization_specialization ADD CONSTRAINT specialization_specialization_fk2 FOREIGN KEY (specialization_field1) REFERENCES specialization(field);
ALTER TABLE doctor_specialization ADD CONSTRAINT doctor_specialization_fk1 FOREIGN KEY (doctor_employee_vital_vue_user_id) REFERENCES doctor(employee_vital_vue_user_id);
ALTER TABLE doctor_specialization ADD CONSTRAINT doctor_specialization_fk2 FOREIGN KEY (specialization_field) REFERENCES specialization(field);

