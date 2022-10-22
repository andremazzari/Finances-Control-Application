-- Select Finances_db
USE finances_db;

-- Set allowed categories in Expenses table
ALTER TABLE Expenses
	ADD CONSTRAINT CHK_ExpenseCategories 
		CHECK (category in 
				('Rent',
                'Supermarket',
                'Restaurant',
                'Gym',
                'Girlfriend',
                'Friends',
                'Books',
                'Courses',
                'House items',
                'Clothes',
                'Gas',
                'Uber',
                'Donations',
                'Other'
                )
			);
            
-- Set allowed categories in Outgoing table
ALTER TABLE Outgoing
	ADD CONSTRAINT CHK_OutgoingCategories 
		CHECK (category in 
				('Rent',
                'Supermarket',
                'Restaurant',
                'Bandeijao',
                'Gym',
                'Rafinha',
                'Friends',
                'Books',
                'Courses',
                'House items',
                'Gas',
                'Uber',
                'Donations',
                'Other'
                )
			);