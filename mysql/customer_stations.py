import xlrd
import mysql.connector
import datetime

data = xlrd.open_workbook("20191128_Data Dump.xlsx")
stations_sheet = data.sheet_by_name("unit_station_names")


db = mysql.connector.connect(
    host="localhost",
    user="increasecapital",
    password="password",
    database="loan_db",
)

cursor = db.cursor()

# Creating tables in the database
# cursor.execute(
#     "CREATE TABLE customer_stations (station_id VARCHAR(50), station_name VARCHAR(110), daily_target VARCHAR(50), monthly_target VARCHAR(50))"
# )

query = """INSERT INTO customer_stations (station_id, station_name, daily_target, monthly_target) VALUES (%s, %s, %s, %s)"""

for r in range(1, stations_sheet.nrows):
    station_id = stations_sheet.cell(r, 0).value
    station_name = stations_sheet.cell(r, 1).value
    daily_target = stations_sheet.cell(r, 2).value
    monthly_target = stations_sheet.cell(r, 3).value

    values = (station_id, station_name, daily_target, monthly_target)

    cursor.execute(query, values)

cursor.close()

db.commit()

db.close()

columns = str(stations_sheet.ncols)
rows = str(stations_sheet.nrows)

print("I just imported {} columns and {} rows").format(columns, rows)
