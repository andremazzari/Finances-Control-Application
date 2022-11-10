#External libraries
import mysql.connector

#Internal files
import CLIFunctions as CLI
import CreditFunctions as Credit

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
    CLI.Confirm_Data(Expense_Data)
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

            #If payment type is credit, ask for credit installments data
            if Expense_Data['payment_type'].lower() == "'credit'":
                confirm_installments, card, number_installments = Credit.Get_Installment_Data()

                if confirm_installments == 'Y':
                    Credit.Create_Credit_Installments(connection, cursor, cursor.lastrowid, int(number_installments), Credit.Get_Card_Info(connection, cursor, card))
        except mysql.connector.Error as e:
            print("\nError in expense insertion.") #Update this for red in the future.
            print("MySQL Error: ", e)


def Insert_Expenses_Mode(connection, cursor):
    print("Insert expenses mode.")
    print("\nEnter any key to insert expense entry, or 'q' or 'quit' to return.")
    command = input("insert_expenses>")
    while not CLI.QuitCommands(command):
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
    while not CLI.QuitCommands(command):
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