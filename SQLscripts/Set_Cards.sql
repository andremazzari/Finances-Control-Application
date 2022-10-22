USE finances_db;

-- Set allowed credit cards in Credit table
ALTER TABLE Credit
	ADD CONSTRAINT CHK_CreditCard
		CHECK (card IN 
				(
					'Card1',
                    'Card2'
				));