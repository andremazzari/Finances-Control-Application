#Internal files
import CLIFunctions as CLI

def Get_Income_Data_CL():
    #Save expense data in a dictionary
    Income_Data = {}

    Income_Data['source'] = "'" + input("Source: ") + "'"
    
    Income_Data['income_date'] = "'" +  input('Date (YYYY-MM-DD): ') + "'"

    Income_Data['value'] = input('Value: ')

    Income_Data['description'] = input('Description: ')
    if Income_Data['description'] == '':
        Income_Data['description'] = 'NULL'
    else:
        Income_Data['description'] = "'" + Income_Data['description'] + "'"

    return Income_Data

def Insert_Income(connection, cursor):
    Income_Data = Get_Income_Data_CL()

    print('\nIncome data: \n')
    CLI.Confirm_Data(Income_Data)
    confirm = input("Confirm income insertion ?(Y/N):")
    while confirm != 'Y' and confirm != 'N':
        print("Please type only 'Y' or 'N'")
        confirm = input("Confirm income insertion ?(Y/N):")

    if confirm == 'Y':
        sql_query = "INSERT INTO Income (source, income_date, value, description) VALUES (" + ', '.join(Income_Data.values()) + ");"
        
        #execute and commit query
        try:
            cursor.execute(sql_query)
            connection.commit()
        except mysql.connector.Error as e:
            print("\nError in income insertion.") #Update this for red in the future.
            print("MySQL Error: ", e)  

def Insert_Income_Mode(connection, cursor):
    print("Insert income mode.")
    print("\nEnter any key to insert income entry, or 'q' or 'quit' to return.")
    command = input("insert_income>")
    while not CLI.QuitCommands(command):
        Insert_Income(connection, cursor)
        print("\nEnter any key to insert income entry, or 'q' or 'quit' to return.")
        command = input("insert_income>")

def View_Total_Income(connection, cursor, Income_Data):
    year, month = Income_Data['income_date'].split("-")
    sql_query = 'SELECT SUM(value) FROM Income WHERE EXTRACT(YEAR_MONTH from income_date) = "' + year + month + '";'

    cursor.execute(sql_query)

    #print("Total income")
    #for value in cursor.fetchall():
    #    print(Income_Data['income_date'] + ": " + str(value[0]))
    return cursor.fetchone()

def View_Income_Items(connection, cursor, Income_Data):
    year, month = Income_Data['income_date'].split("-")
    sql_query = 'SELECT income_id, source, income_date, value FROM Income WHERE EXTRACT(YEAR_MONTH from income_date) = "' + year + month + '" ORDER BY income_date;'

    cursor.execute(sql_query)

    print("Income items for date: " + Income_Data['income_date'])

    print('\n' + 'id' + (' ' * 4) + 'source' + (' ' * 9) + 'date' + (' ' * 10) + 'value\n')
    for item in cursor.fetchall():
        item_string = str(item[0]) + (' ' * (6 - len(str(item[0]))))
        item_string += str(item[1]) + (' ' * (15 - len(str(item[1]))))
        item_string += str(item[2]) + (' ' * (14 - len(str(item[2]))))
        item_string += str(item[3])

        print(item_string)

def View_Income_Mode(connection, cursor):
    print("View income mode.")
    print("\nEnter 'help' to see command menu, or 'q' or 'quit' to return.")
    command = input("view_income>")
    while not CLI.QuitCommands(command):
        command = command.strip().split(" ")

        #FUTURE UPDATE: validate entry format

        #Separate date info
        Income_Data = {}
        Income_Data['income_date'] = command[1]

        if command[0] == 'total':
            value = View_Total_Income(connection, cursor, Income_Data)

            print("Total income")
            print(Income_Data['income_date'] + ": " + str(value[0]))
        elif command[0] == 'items':
            View_Income_Items(connection, cursor, Income_Data)
        else:
            print("Command not found")

        command = input("view_income>")