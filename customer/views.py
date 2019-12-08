# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import View
from render import Render

import mysql.connector


def customer_data(request):
    db = mysql.connector.connect(
        host="localhost",
        user="increasecapital",
        password="password",
        database="loan_db",
    )

    cursor = db.cursor()
    customer_details = []
    if request.method == "GET":
        query = "SELECT lo.`customer_id`, lo.`customer_station`, cs.`station_name`  FROM `loans` AS lo INNER JOIN `customer_stations` AS cs ON lo.`customer_station` = cs.`station_id`;"
        cursor.execute(query)
        customer_data = cursor.fetchall()

        for row in customer_data:
            customer_details.append(row)

        q = request.GET.get("q", None)
        if q:
            search_results(customer_data, q)

        cursor.close()

    db.commit()

    db.close()

    return render(
        request, "customer_data.html", {"customer_details": customer_details}
    )


def search_results(values, q):
    search_results = []
    for row in values:
        if q in row:
            search_results.append(row)
        else:
            return "Record does not exist"
    return render(request, "search.html", {"search_results": search_results})


def loan_data(request):
    db = mysql.connector.connect(
        host="localhost",
        user="increasecapital",
        password="password",
        database="loan_db",
    )

    cursor = db.cursor()
    loan_details = []
    if request.method == "GET":
        loan_query = "SELECT lo.`customer_id`, lo.`loan_date`, lo.`due_date`, lo.`loan_code`, lo.`loan_amount` FROM `loans` AS lo;"
        cursor.execute(loan_query)
        loan_data = cursor.fetchall()
        for row in loan_data:
            loan_details.append(row)

        cursor.close()

    db.commit()

    db.close()

    return render(request, "loan_data.html", {"loan_details": loan_details})


def repayment_data(request):
    db = mysql.connector.connect(
        host="localhost",
        user="increasecapital",
        password="password",
        database="loan_db",
    )

    cursor = db.cursor()
    repayment_details = []
    if request.method == "GET":
        repayment_query = "SELECT lo.`loan_status`, ls.`loan_status`, lo.`customer_id`, lo.`loan_date`, lo.`due_date`, lo.`loan_code`, lo.`loan_amount` FROM `loans` AS lo INNER JOIN `loan_status` AS ls ON lo.`loan_status` = ls.`status_id`;"
        cursor.execute(repayment_query)
        repayment_data = cursor.fetchall()
        for row in repayment_data:
            repayment_details.append(row)

        cursor.close()

    db.commit()

    db.close()

    return render(
        request,
        "repayment_data.html",
        {"repayment_details": repayment_details},
    )


def process_customers_report(request):
    if request.method == "GET":
        rangefrom = request.GET.get("rangefrom", None)
        rangeto = request.GET.get("rangeto", None)
        if rangefrom and rangeto:
            db = mysql.connector.connect(
                host="localhost",
                user="increasecapital",
                password="password",
                database="loan_db",
            )

            cursor = db.cursor()
            customers = []

            query = "SELECT lo.`customer_id`, lo.`customer_station`, cs.`station_name`  FROM `loans` AS lo INNER JOIN `customer_stations` AS cs ON lo.`customer_station` = cs.`station_id` WHERE lo.`loan_date` BETWEEN 'rangefrom' AND 'rangeto';"
            cursor.execute(query)
            customers_data = cursor.fetchall()
            for row in customers_data:
                customers.append(row)

            cursor.close()

            db.commit()

            db.close()

            return render(
                request, "customers_report.html", {"customers": customers}
            )
        # else:
        #     return "No data found for that range. Kindly pick another range"

    return render(request, "process_customers_report.html")


def process_loans_report(request):
    if request.method == "GET":
        rangefrom = request.GET.get("rangefrom", None)
        rangeto = request.GET.get("rangeto", None)
        if rangefrom and rangeto:
            db = mysql.connector.connect(
                host="localhost",
                user="increasecapital",
                password="password",
                database="loan_db",
            )

            cursor = db.cursor()
            loans = []

            loan_query = "SELECT lo.`customer_id`, lo.`loan_date`, lo.`loan_code`, lo.`loan_amount` FROM `loans` AS lo WHERE lo.`loan_date` BETWEEN 'rangefrom' AND 'rangeto';"
            cursor.execute(loan_query)
            loans_data = cursor.fetchall()
            for row in loans_data:
                loans.append(row)

            cursor.close()

            db.commit()

            db.close()

            return render(request, "loans_report.html", {"loans": loans})

    return render(request, "process_loans_report.html")


def process_repayments_report(request):
    if request.method == "GET":
        rangefrom = request.GET.get("rangefrom", None)
        rangeto = request.GET.get("rangeto", None)
        if rangefrom and rangeto:
            db = mysql.connector.connect(
                host="localhost",
                user="increasecapital",
                password="password",
                database="loan_db",
            )

            cursor = db.cursor()
            repayments = []

            repayment_query = "SELECT lo.`customer_id`, lo.`due_date`, lo.`loan_code`, ls.`loan_status` FROM `loans` AS lo INNER JOIN `loan_status` AS ls ON lo.`loan_status` = ls.`status_id` WHERE lo.`loan_date` BETWEEN 'rangefrom' AND 'rangeto';"
            cursor.execute(repayment_query)
            repayments_data = cursor.fetchall()
            for row in repayments_data:
                repayments.append(row)

            cursor.close()

            db.commit()

            db.close()

            return render(
                request, "repayments_report.html", {"repayments": repayments}
            )

    return render(request, "process_repayments_report.html")


class Pdf(View):
    def customers_pdf_report(self, request):
        customers_html = templates.customers_report.html
        return Render.render(customers_html)

    def loans_pdf_report(self, request):
        loans_html = templates.loans_report.html
        return Render.render(loans_html)

    def repayments_pdf_report(self, request):
        repayments_html = templates.repayments_report.html
        return Render.render(repayments_html)

