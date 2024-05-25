CREATE TRIGGER trigger_create_bill_after_insert
AFTER INSERT ON appointment
FOR EACH ROW
EXECUTE PROCEDURE create_bill_after_insert();
