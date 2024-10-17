-- 4-store.sql
DROP TRIGGER IF EXISTS update_quantity;
DELIMITER $$

CREATE TRIGGER update_quantity
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
  UPDATE items
  SET quantity = quantity - NEW.number
  WHERE name = NEW.item_name;
END $$

DELIMITER ;