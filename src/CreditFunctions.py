import mysql.connector
from getpass import getpass

DATABASE_NAME = 'finances_db'

def Get_Card_Info(connection, cursor, card):
    card_info = {}
    card_info['card'] = card

    sql_query = "SELECT closing_day, due_day FROM Credit_Cards where card = '" + card + "'"

    cursor.execute(sql_query)
    card_info['closing_day'], card_info['due_day'] = cursor.fetchone()

    card_info['closing_day'] = int(card_info['closing_day'])
    card_info['due_day'] = int(card_info['due_day'])

    return card_info

def Create_Credit_Installments(connection, cursor, expense_id, num_installments, card_info):
    sql_query = 'SELECT expense_date, payment_type, value FROM Expenses where expense_id = ' + str(expense_id)

    cursor.execute(sql_query)
    expense_date, payment_type, value = cursor.fetchone()
    
    if payment_type != 'Credit':
        print("Not a credit expense.")
        return False #UPDATE THIS ACTION IN THE FUTURE

    value_installment = round(value / num_installments, 2)

    if card_info['closing_day'] < card_info['due_day']:
        month_offset = 0
    else:
        month_offset = 1

    year, month, day = str(expense_date).split("-")

    #Get due date of the first installment
    if int(day) >= card_info['closing_day']:
        due_month = str(int(month) + 1 + month_offset)
    else:
        due_month = str(int(month) + month_offset)
    
    if due_month == '13':
        due_month = '01'
        year = str(int(year) + 1)

    due_date = year + '-' + due_month + '-' + str(card_info['due_day'])

    for num_installment in range(1, num_installments + 1):
        sql_query = "INSERT INTO Credit_Installments (due_date, card, expense_id, value, number_installment, total_installments) values ("
        sql_query +=  "'" + due_date + "', "
        sql_query += "'" + card_info['card'] + "', "
        sql_query += str(expense_id) + ", "
        sql_query += str(value_installment) + ", "
        sql_query += str(num_installment) + ", "
        sql_query += str(num_installments) + ")"
        print(sql_query)

        try:
            cursor.execute(sql_query)
            connection.commit()
        except mysql.connector.Error as e:
            print("\nError in credit installment insertion (expense_id: " + str(expense_id) + ", num_installment: " + str(num_installment) + ").") #Update this for red in the future.
            print("MySQL Error: ", e)
            break
        
        #Update due date
        due_month = str(int(due_month) + 1)
        if due_month == '13':
            due_month = '01'
            year = str(int(year) + 1)

        due_date = year + '-' + due_month + '-' + str(card_info['due_day'])

def Get_Installment_Data():
    confirm = input("Complete installments ?(Y/N):")
    while confirm != 'Y' and confirm != 'N':
        print("Please type only 'Y' or 'N'")
        confirm = input("Complete installments ?(Y/N):")

    if confirm == 'Y':
        card = input("Credit card:")
        #FUTURE UPDATE: Verify if the name of the card is valid.
        number_installments = input("Number of installments:")
        #FUTURE UPDATE: verify is number is valid.
    else:
        card = None
        number_installments = None

    return confirm, card, number_installments

def Complete_Credit_Expenses_Without_Installments(connection, cursor):
    sql_query = "SELECT E.expense_id, E.category, E.expense_date, E.value FROM Expenses E LEFT OUTER JOIN credit_installments CI ON E.expense_id = CI.expense_id WHERE CI.expense_id is null;"

    cursor.execute(sql_query)

    for expense_data in cursor.fetchall():
        print("")
        print("Expense id: ", expense_data[0])
        print("Category: ", expense_data[1])
        print("Date: ", expense_data[2])
        print("Value: ", expense_data[3])
        
        confirm, card, number_installments = Get_Installment_Data()

        if confirm == 'Y':
            Create_Credit_Installments(connection, cursor, expense_data[0], int(number_installments), Get_Card_Info(connection, cursor, card))
    



if __name__ == '__main__':
    try:
        with mysql.connector.connect(
            host="localhost",
            user=input("Enter username: "),
            password=getpass("Enter password: "),
            database = DATABASE_NAME
        ) as connection:
            with connection.cursor() as cursor:
                #Create_Credit_Installments(connection, cursor, 2, 1, {'card':'Xt', 'closing_day':1, "due_day":10})
                Complete_Credit_Expenses_Without_Installments(connection, cursor)
    except mysql.connector.Error as e:
        print(e)