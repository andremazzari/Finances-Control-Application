USE finances_db;

-- Set allowed sources in Income table.
ALTER TABLE Income
	ADD CONSTRAINT CHK_IncomeSource
		CHECK (source IN 
			(
				'Source1',
                'Source2',
                'Source3',
                'Other'
			));
        