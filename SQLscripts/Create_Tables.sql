-- select finances_db
USE finances_db;

-- Create Income table
CREATE TABLE IF NOT EXISTS Income
	(
		income_id INT NOT NULL AUTO_INCREMENT,
		source VARCHAR(40) NOT NULL,
		income_date DATE NOT NULL,
		value DECIMAL(8,2) NOT NULL,
		description VARCHAR(200),
		PRIMARY KEY (income_id)
	);

-- Create Expenses table
CREATE TABLE IF NOT EXISTS Expenses
	(
		expense_id INT NOT NULL AUTO_INCREMENT,
		category VARCHAR(15) NOT NULL,
		local VARCHAR(20),
		expense_date DATE NOT NULL,
		value DECIMAL(8,2) NOT NULL,
		payment_type VARCHAR(15),
		observation VARCHAR(200),
		PRIMARY KEY (expense_id)
	);

-- Create Expenses Details table
CREATE TABLE IF NOT EXISTS Expenses_Details
	(
		expense_id INT NOT NULL AUTO_INCREMENT,
		item_id INT NOT NULL,
		item_name VARCHAR(30) NOT NULL,
		value DECIMAL(7,2) NOT NULL,
		observation VARCHAR(200),
		PRIMARY KEY (expense_id,item_id),
		FOREIGN KEY (expense_id) REFERENCES Expenses(expense_id)
	);
	
-- Create Credit Installments table (relationship between Expenses and Credit)
CREATE TABLE IF NOT EXISTS Credit_Installments
	(
		due_date DATE NOT NULL,
		card VARCHAR(20) NOT NULL,
		expense_id INT NOT NULL,
		value DECIMAL(8,2) NOT NULL,
		number_installment INT NOT NULL,
		total_installments INT NOT NULL,
		PRIMARY KEY (card, due_date, expense_id),
		FOREIGN KEY (expense_id) REFERENCES Expenses(expense_id)
	);
	
-- Create Investiments table
CREATE TABLE IF NOT EXISTS Investiments
	(
		investiment_id	INT NOT NULL AUTO_INCREMENT,
		investiment_date DATE NOT NULL,
		type VARCHAR(30) NOT NULL,
		broker VARCHAR(40) NOT NULL,
		title VARCHAR(50) NOT NULL,
		value DECIMAL(8,2) NOT NULL,
		observation VARCHAR(200),
		PRIMARY KEY (investiment_id)
	);
    
-- Create Outgoing table
CREATE TABLE IF NOT EXISTS Outgoing
	(
		outgoing_id INT NOT NULL AUTO_INCREMENT,
		outgoing_date DATE NOT NULL,
		category VARCHAR(15) NOT NULL,
		value DECIMAL(8,2) NOT NULL,
		expense_id INT,
		PRIMARY KEY (outgoing_id),
		FOREIGN KEY (expense_id) REFERENCES Expenses(expense_id)
	);
        
-- Credit cards table
CREATE TABLE IF NOT EXISTS Credit_Cards
	(
		card VARCHAR(20) NOT NULL,
        	closing_day VARCHAR(2) NOT NULL,
        	due_day VARCHAR(2) NOT NULL,
        	PRIMARY KEY (card)
	);
