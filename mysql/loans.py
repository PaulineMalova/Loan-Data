import xlrd
import mysql.connector
import datetime

data = xlrd.open_workbook("20191128_Data Dump.xlsx")
loans_sheet = data.sheet_by_name("loans")


db = mysql.connector.connect(
    host="localhost",
    user="increasecapital",
    password="password",
    database="loan_db",
)


cursor = db.cursor()

# Creating a database
# cursor.execute("CREATE DATABASE loan_db")

# Creating tables in the database
# cursor.execute(
#     "CREATE TABLE loans (loan_date DATE, due_date DATE, loan_code BIGINT(20), loan_amount BIGINT(20), loan_status VARCHAR(50), customer_id BIGINT(20), customer_station VARCHAR(50))"
# )

# cursor.execute("SHOW TABLES")

# for tb in cursor:
#     print(tb)

# Create the INSERT INTO sql query
query = """INSERT INTO loans (loan_date, due_date, loan_code, loan_amount, loan_status, customer_id, customer_station) VALUES (%s, %s, %s, %s, %s, %s, %s)"""

print (loans_sheet.cell(1, 5).value)

for r in range(1, loans_sheet.nrows):
    loan_date_as_float = loans_sheet.cell(r, 0).value
    loan_date = datetime.datetime(
        *xlrd.xldate_as_tuple(loan_date_as_float, data.datemode)
    )
    due_date_as_float = loans_sheet.cell(r, 1).value
    due_date = datetime.datetime(
        *xlrd.xldate_as_tuple(due_date_as_float, data.datemode)
    )
    loan_code = loans_sheet.cell(r, 2).value
    loan_amount = loans_sheet.cell(r, 3).value
    loan_status = loans_sheet.cell(r, 4).value
    customer_id = loans_sheet.cell(r, 5).value
    customer_station = loans_sheet.cell(r, 6).value

    values = (
        loan_date,
        due_date,
        loan_code,
        loan_amount,
        loan_status,
        customer_id,
        customer_station,
    )

    cursor.execute(query, values)

cursor.close()

db.commit()

db.close()

columns = str(loans_sheet.ncols)
rows = str(loans_sheet.nrows)

print("I just imported {} columns and {} rows").format(columns, rows)
