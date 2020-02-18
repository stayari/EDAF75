DROP TABLE IF EXISTS accounts; 
CREATE TABLE accounts (
	account_no		INT,
	balance 		DECIMAL(16,2),
	PRIMARY KEY (account_no)
);

DROP TABLE IF EXISTS transfers; 
CREATE TABLE transfers (
	src_account_no	INT,
	dst_account_no	INT,
	amount			DECIMAL(16,2)
);

CREATE TRIGGER update_accounts
BEFORE INSERT ON transfers
BEGIN
	-- Update dst account and then src account
	UPDATE	accounts
	SET		balance = balance + NEW.amount
	WHERE	account_no = NEW.dst_account_no


	UPDATE	accounts
	SET		balance = balance - NEW.amount
	WHERE	account_no = NEW.src_account_no

END; 

INSERT 
INTO	accounts(account_no, balance)
VALUES	(101,1000),
		(102,2000),
		(103,3000);

SELECT "Before anything";

SELECT * 
FROM accounts;

INSERT 
INTO	transfers(src_account_no, dst_account_no, amount)
VALUES (101,102,500);

SELECT "After "






