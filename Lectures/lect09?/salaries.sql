DROP TABLE IF EXISTS employees; 
CREATE TABLE employees (
	employees_id	TEXT,
	salary			DECIMAL(16,2),
	PRIMARY KEY 	(employees_id),
	CHECK			(salary >= 25000)--Kolla så att vilkoret alltid uppfylls 
);

INSERT
INTO	employees(employees_id, salary)
VALUES	('ALICE', 32000),
		('BOB', 31500),
		('CAROL', 25000);

CREATE TRIGGER union_check
BEFORE UPDATE OF salary ON employees
WHEN NEW.salary < OLD.salary
BEGIN
	SELECT RAISE (ROLLBACK, "Oh no");
END

SELECT * 
FROM	employees; 

UPDATE	employees
SET		salary = salary-100
WHERE	employees_id = 'BOB'

SELECT *
FROM employees; 
