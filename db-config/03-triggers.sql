CREATE TRIGGER trigger_create_bill_after_insert
AFTER INSERT ON appointment
FOR EACH ROW
EXECUTE PROCEDURE create_bill_after_insert();

CREATE TRIGGER trigger_create_hospitalization_if_needed
BEFORE INSERT ON surgery
FOR EACH ROW
EXECUTE PROCEDURE create_hospitalization_if_needed();

CREATE TRIGGER trigger_associate_patient_with_prescription
BEFORE INSERT ON prescription
FOR EACH ROW
EXECUTE PROCEDURE associate_patient_with_prescription();

CREATE TRIGGER trigger_create_medicine_if_needed
BEFORE INSERT ON med_posology
FOR EACH ROW
EXECUTE PROCEDURE create_medicine_if_needed();