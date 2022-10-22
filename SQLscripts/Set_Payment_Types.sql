-- Use finances database
USE finances_db;

-- Set allowed payment types in Expenses table
ALTER TABLE Expenses
	ADD CONSTRAINT CHK_PaymentTypes
		CHECK (payment_type IN 
			('Credit',
            'Cash',
            'Debit',
            'Bank slip'
            ));
			