# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# from .models import Loans
# from .models import Loans, LoanStatus, CustomerStations

import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="increasecapital",
    password="password",
    database="loan_db",
)

cursor = db.cursor()


def customer_data(request):
    customer_details = []
    if request.method == "GET":
        query = "SELECT lo.`customer_id`, lo.`customer_station`, cs.`station_name`  FROM `loans` AS lo INNER JOIN `customer_stations` AS cs ON lo.`customer_station` = cs.`station_id`;"
        cursor.execute(query)
        customer_data = cursor.fetchall()
        for row in customer_data:
            customer_details.append(row)

    return render(
        request, "customer_data.html", {"customer_details": customer_details}
    )

def loan_data(request):
    loan_details = []
    if request.method == "GET":
        query = "SELECT lo.`customer_id`, lo.`loan_date`, lo.`due_date`, lo.`loan_code`, lo.`loan_amount` FROM `loans` AS lo;"
        cursor.execute(query)
        loan_data = cursor.fetchall()
        for row in loan_data:
            loan_details.append(row)

    return render(request, "loan_data.html", {"loan_details":loan_details})        


def repayment_data(request):
    repayment_details = []
    if request.method == "GET":  
        query = "SELECT lo.`loan_status`, ls.`loan_status`, lo.`customer_id`, lo.`loan_date`, lo.`due_date`, lo.`loan_code`, lo.`loan_amount` FROM `loans` AS lo INNER JOIN `loan_status` AS ls ON lo.`loan_status` = ls.`status_id`;"
        cursor.execute(query)
        repayment_data = cursor.fetchall()
        for row in repayment_data:
            repayment_details.append(row)  

    return render(request, "repayment_data.html", {"repayment_details":repayment_details}) 
