import xlrd
import mysql.connector

data = xlrd.open_workbook("20191128_Data Dump.xlsx")
loan_status_sheet = data.sheet_by_name("loan_status")

db = mysql.connector.connect(
    host="localhost",
    user="increasecapital",
    password="password",
    database="loan_db",
)

cursor = db.cursor()

# Creating tables in the database
# cursor.execute(
#     "CREATE TABLE loan_status (status_id VARCHAR(50), loan_status VARCHAR(50))"
# )

query = """INSERT INTO loan_status (status_id, loan_status) VALUES (%s, %s)"""

for r in range(1, loan_status_sheet.nrows):
    status_id = loan_status_sheet.cell(r, 0).value
    loan_status = loan_status_sheet.cell(r, 1).value

    values = (status_id, loan_status)

    cursor.execute(query, values)

cursor.close()

db.commit()

db.close()

columns = str(loan_status_sheet.ncols)
rows = str(loan_status_sheet.nrows)

print("I just imported {} columns and {} rows").format(columns, rows)
