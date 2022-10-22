import mysql.connector
from getpass import getpass

#Global variables
DATABASE_NAME = 'finances_db'

def Help_Menu():
    print('Available commands:\n')

    print('insert_expenses: enter insert expense mode.')
    print('view_expense: view expense data for a specific month.')
    print('insert_income: enter insert income mode.')
    print('view_income: view income data for a specific month.')
    print('summary: view montly summary data.')
    print('quit: leave finances app.')

def Confirm_Data(data_dict):
    for key, value in data_dict.items():
        print(str(key) + ": " + str(value))


#EXPENSES FUNCTIONS

'''Get_Expense_Data_CL
Description: Get expense data from command line.
Input: None
Output: Dictionary with expense data

FUTURE UPDATES: Implement validation of the entries
'''
def Get_Expense_Data_CL():
    #Save expense data in a dictionary
    Expense_Data = {}

    Expense_Data['category'] = "'" + input("Category: ") + "'"

    Expense_Data['local'] = input('Local: ')
    if Expense_Data['local'] == '':
        Expense_Data['local'] = 'NULL'
    else:
        Expense_Data['local'] = "'" + Expense_Data['local'] + "'"
    
    Expense_Data['date'] = "'" +  input('Date (YYYY-MM-DD): ') + "'"

    Expense_Data['value'] = input('Value: ')

    Expense_Data['payment_type'] = input('Payment type: ')
    if Expense_Data['payment_type'] == '':
        Expense_Data['payment_type'] = 'NULL'
    else:
        Expense_Data['payment_type'] = "'" + Expense_Data['payment_type'] + "'"

    Expense_Data['observation'] = input('Observation: ')
    if Expense_Data['observation'] == '':
        Expense_Data['observation'] = 'NULL'
    else:
        Expense_Data['observation'] = "'" + Expense_Data['observation'] + "'"

    return Expense_Data


def Insert_Expense(connection, cursor):
    Expense_Data = Get_Expense_Data_CL()

    print('\nExpense data: \n')
    Confirm_Data(Expense_Data)
    confirm = input("Confirm expense insertion ?(Y/N):")
    while confirm != 'Y' and confirm != 'N':
        print("Please type only 'Y' or 'N'")
        confirm = input("Confirm expense insertion ?(Y/N):")

    if confirm == 'Y':
        sql_query = "INSERT INTO Expenses (category, local, expense_date, value, payment_type, observation) VALUES (" + ', '.join(Expense_Data.values()) + ");"
        
        #execute and commit query
        try:
            cursor.execute(sql_query)
            connection.commit()
        except mysql.connector.Error as e:
            print("\nError in expense insertion.") #Update this for red in the future.
            print("MySQL Error: ", e)  


def Insert_Expenses_Mode(connection, cursor):
    print("Insert expenses mode.")
    print("\nEnter any key to insert expense entry, or 'q' or 'quit' to return.")
    command = input("insert_expenses>")
    while command != 'q' and command != 'quit':
        Insert_Expense(connection, cursor)
        print("\nEnter any key to insert expense entry, or 'q' or 'quit' to return.")
        command = input("insert_expenses>")


def View_Total_Expense(connection, cursor, Expense_Data, Categories = False):
    year, month = Expense_Data['expense_date'].split("-")

    if Categories:
        if Expense_Data['category'] == None: #No category specified, show all categories
            sql_query = 'SELECT category, SUM(value) FROM Expenses WHERE EXTRACT(YEAR_MONTH from expense_date) = "' + year + month + '" GROUP BY category;'
        #FUTURE UPDATE: include specific categories
    else:
        sql_query = 'SELECT SUM(value) FROM Expenses WHERE EXTRACT(YEAR_MONTH from expense_date) = "' + year + month + '";'

    cursor.execute(sql_query)
    return cursor.fetchall()

def View_Expense_Items(connection, cursor, Expense_Data):
    year, month = Expense_Data['expense_date'].split("-")
    sql_query = 'SELECT expense_id, category, expense_date, value FROM Expenses WHERE EXTRACT(YEAR_MONTH from expense_date) = "' + year + month + '" ORDER BY expense_date;'

    cursor.execute(sql_query)

    print("Expense items for date: " + Expense_Data['expense_date'])

    print('\n' + 'id' + (' ' * 4) + 'category' + (' ' * 12) + 'date' + (' ' * 10) + 'value\n')
    for item in cursor.fetchall():
        item_string = str(item[0]) + (' ' * (6 - len(str(item[0]))))
        item_string += str(item[1]) + (' ' * (20 - len(str(item[1]))))
        item_string += str(item[2]) + (' ' * (14 - len(str(item[2]))))
        item_string += str(item[3])

        print(item_string)

def View_Expenses_Mode(connection, cursor):
    print("View expenses mode.")
    print("\nEnter 'help' to see command menu, or 'q' or 'quit' to return.")
    command = input("view_expenses>")
    while command != 'q' and command != 'quit':
        command = command.strip().split(" ")

        #FUTURE UPDATE: validate entry format

        #Separate date and category info
        Expense_Data = {}
        Expense_Data['expense_date'] = command[1]
        Expense_Data['category'] = None #FUTURE UPDATE: include category filtering.

        if command[0] == 'total':
            if len(command) > 2:
                if command[2] != 'category':
                    print("Unknown option " + command[2])
                    command = input("view_expenses>")
                    continue
                #FUTURE UPDATE: include specific categories
                Categories = True
            else:
                Categories = False

            value = View_Total_Expense(connection, cursor, Expense_Data, Categories)

            print("Total expenses")
            if Categories:
                print('\n' + 'Category' + (' ' * 12) + 'Value\n')
                for category_expense in value:
                    category_string = str(category_expense[0]) + (' ' * (20 - len(str(category_expense[0]))))
                    category_string += str(category_expense[1])
                    print(category_string)
            else:
                print(Expense_Data['expense_date'] + ": " + str(value[0][0]))
        elif command[0] == 'items':
            View_Expense_Items(connection, cursor, Expense_Data)
        else:
            print("Command not found")

        command = input("view_expenses>")

#INCOME FUNCTIONS

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
    Confirm_Data(Income_Data)
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
    while command != 'q' and command != 'quit':
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
    while command != 'q' and command != 'quit':
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

#AGGREGATED DATA

def Print_Montly_Summary_Data(connection, cursor, date):
    total_income = View_Total_Income(connection, cursor, {'income_date': date})[0]
    total_expense = View_Total_Expense(connection, cursor, {'expense_date': date})[0][0]

    print('Summary data for: ' + str(date) +'\n')
    print('Total income: ' + str(total_income))
    print('Total expense: ' + str(total_expense))
    print('Difference: ' + str(total_income - total_expense))

def Print_Range_Summary_Data(connection, cursor, date):
    #date[0]:lower date; date[1]:upper date
    year, month = date[0].split("-")
    upper_year, upper_month = date[1].split("-")

    year = int(year)
    month = int(month)
    upper_year = int(upper_year)
    upper_month = int(upper_month)

    print('\n' + 'Total income' + (' ' * 8) + 'Total expense' + (' ' * 7) + 'Difference\n')
    while year < upper_year or month <= upper_month:
        date = str(year) + '-' + str(month)

        total_income = View_Total_Income(connection, cursor, {'income_date': date})[0]
        total_expense = View_Total_Expense(connection, cursor, {'expense_date': date})[0][0]
        if total_income == None or total_expense == None:
            difference = None
        else:
            difference =  total_income - total_expense

        summary_string = str(total_income) + (' ' * (20 - len(str(total_income))))
        summary_string += str(total_expense) + (' ' * (20 - len(str(total_expense))))
        summary_string += str(difference)
        print(summary_string)

        #update date
        if month == 12:
            month = 1
            year += 1
        else:
            month += 1



def Summary_Data_Mode(connection, cursor):
    print("Summary data mode.")
    print("\nEnter 'help' to see command menu, or 'q' or 'quit' to return.")
    print("Type date 'YYYY-MM' to see sumary data")

    command = input('summary>')
    while command != 'q' and command != 'quit':
        command = command.strip().split(" ")
        if command[0] == 'range':
            if len(command) != 3:
                print("Incorrect format for 'range' command.")
                print("Format: range YYYY-MM YYYY-MM")
            else:
                #FUTURE UPDATE: validate dates format
                Print_Range_Summary_Data(connection, cursor, [command[1], command[2]])
        else:
            #FUTURE UPDATE: validate command
            Print_Montly_Summary_Data(connection, cursor, command)

        command = input('summary>')
        

if __name__ == '__main__':
    try:
        with mysql.connector.connect(
            host="localhost",
            user=input("Enter username: "),
            password=getpass("Enter password: "),
            database = DATABASE_NAME
        ) as connection:
            with connection.cursor() as cursor:
                command = input(">")
                while command != 'quit':
                    if command == 'help':
                        Help_Menu()
                    elif command == 'insert_expenses':
                        Insert_Expenses_Mode(connection, cursor)
                    elif command == 'view_expenses':
                        View_Expenses_Mode(connection, cursor)
                    elif command == 'insert_income':
                        Insert_Income_Mode(connection, cursor)
                    elif command == 'view_income':
                        View_Income_Mode(connection, cursor)
                    elif command == 'summary':
                        Summary_Data_Mode(connection, cursor)
                    else:
                        print("Command not found")
                    
                    command = input(">")


    except mysql.connector.Error as e:
        print(e)