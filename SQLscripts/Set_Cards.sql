USE finances_db;

-- Set allowed credit cards in Credit card table
ALTER TABLE Credit_Cards
	ADD CONSTRAINT CHK_CreditCardTable
		CHECK (card IN 
				(
					'Card1',
                    			'Card2'
				));
                
-- Set allowed credit cards in Credit card table
ALTER TABLE Credit_Installments
	ADD CONSTRAINT CHK_CreditInstallmentCards
		CHECK (card IN 
				(
					'Card1',
                    			'Card2'
				));