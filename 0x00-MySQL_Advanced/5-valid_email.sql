-- valid_email.sql
DROP TRIGGER if EXISTS valid;
DELIMITER $$

CREATE TRIGGER valid
BEFORE UPDATE on users
FOR EACH ROW
BEGIN
    if old.email != new.email THEN
        SET NEW.valid_email = 0;
    END IF;
END$$

DELIMITER ;
