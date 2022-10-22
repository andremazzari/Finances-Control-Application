#External libraries
import mysql.connector
from getpass import getpass

#Internal files
import ExpenseFunctions as Expenses
import IncomeFunctions as Income
import CLIFunctions as CLI

#Global variables
DATABASE_NAME = 'finances_db'

def Help_Menu():
    print('Available commands:\n')

    print('insert_expenses: enter insert expense mode.')
    print('view_expenses: view expense data for a specific month.')
    print('insert_income: enter insert income mode.')
    print('view_income: view income data for a specific month.')
    print('summary: view montly summary data.')
    print('quit: leave finances app.')



#AGGREGATED DATA

def Print_Montly_Summary_Data(connection, cursor, date):
    total_income = Income.View_Total_Income(connection, cursor, {'income_date': date})[0]
    total_expense = Expenses.View_Total_Expense(connection, cursor, {'expense_date': date})[0][0]

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

        total_income = Income.View_Total_Income(connection, cursor, {'income_date': date})[0]
        total_expense = Expenses.View_Total_Expense(connection, cursor, {'expense_date': date})[0][0]
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
            Print_Montly_Summary_Data(connection, cursor, command[0])

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
                while not (CLI.QuitCommands(command)):
                    if command == 'help':
                        Help_Menu()
                    elif command == 'insert_expenses':
                        Expenses.Insert_Expenses_Mode(connection, cursor)
                    elif command == 'view_expenses':
                        Expenses.View_Expenses_Mode(connection, cursor)
                    elif command == 'insert_income':
                        Income.Insert_Income_Mode(connection, cursor)
                    elif command == 'view_income':
                        Income.View_Income_Mode(connection, cursor)
                    elif command == 'summary':
                        Summary_Data_Mode(connection, cursor)
                    else:
                        print("Command not found")
                    
                    command = input(">")


    except mysql.connector.Error as e:
        print(e)