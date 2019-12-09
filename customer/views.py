# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from easy_pdf.views import PDFTemplateView
from django.http import HttpResponse

import mysql.connector
import xlwt

customer_details = []
customers = []
loans = []
repayments = []


def customer_data(request):
    db = mysql.connector.connect(
        host="localhost",
        user="increasecapital",
        password="password",
        database="loan_db",
    )

    cursor = db.cursor()

    if request.method == "GET":
        query = "SELECT lo.`customer_id`, lo.`customer_station`, cs.`station_name`  FROM `loans` AS lo INNER JOIN `customer_stations` AS cs ON lo.`customer_station` = cs.`station_id`;"
        cursor.execute(query)
        customer_data = cursor.fetchall()

        for row in customer_data:
            customer_details.append(row)

        cursor.close()

    db.commit()

    db.close()

    return render(
        request, "customer_data.html", {"customer_details": customer_details}
    )


def search_results(request):
    search_results = []
    q = request.GET.get("q", None)
    if q:
        for x in customer_details:
            if q in x:
                search_results.append(x)

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
            

            try:
                xrange
            except NameError:
                xrange = range

            cursor.execute("SELECT count(*) FROM loans")

            count = cursor.fetchone()[0]
            batch_size = 100

            for offset in xrange(0, count, batch_size):
                query = (
                    "SELECT lo.`customer_id`, lo.`customer_station`, cs.`station_name`  FROM `loans` AS lo INNER JOIN `customer_stations` AS cs ON lo.`customer_station` = cs.`station_id` WHERE lo.`loan_date` BETWEEN %s AND %s LIMIT %s OFFSET %s;",
                    (rangefrom, rangeto, batch_size, offset),
                )
                cursor.execute(query)
                for row in cursor:
                    customers.append(row)

            cursor.close()

            db.commit()

            db.close()

            return render(
                request, "customers_report.html", {"customers": customers}
            )

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

            try:
                xrange
            except NameError:
                xrange = range

            cursor.execute("SELECT count(*) FROM loans")

            count = cursor.fetchone()[0]
            batch_size = 100

            for offset in xrange(0, count, batch_size):
                loan_query = (
                    "SELECT lo.`customer_id`, lo.`loan_date`, lo.`loan_code`, lo.`loan_amount` FROM `loans` AS lo WHERE lo.`loan_date` BETWEEN %s AND %s LIMIT %s OFFSET %s;",
                    (rangefrom, rangeto, batch_size, offset),
                )
                cursor.execute(loan_query)
                for row in cursor:
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

            try:
                xrange
            except NameError:
                xrange = range

            cursor.execute("SELECT count(*) FROM loans")

            count = cursor.fetchone()[0]
            batch_size = 100

            for offset in xrange(0, count, batch_size):
                repayment_query = (
                    "SELECT lo.`customer_id`, lo.`due_date`, lo.`loan_code`, ls.`loan_status` FROM `loans` AS lo INNER JOIN `loan_status` AS ls ON lo.`loan_status` = ls.`status_id` WHERE lo.`loan_date` BETWEEN %s AND %s LIMIT %s OFFSET %s;",
                    (rangefrom, rangeto, batch_size, offset),
                )
                cursor.execute(repayment_query)
                for row in cursor:
                    repayments.append(row)

            cursor.close()

            db.commit()

            db.close()

            return render(
                request, "repayments_report.html", {"repayments": repayments}
            )

    return render(request, "process_repayments_report.html")


class CustomerPDFView(PDFTemplateView):
    template_name = "customers_report.html"

    def get_context_data(self, **kwargs):
        context = super(CustomerPDFView, self).get_context_data(**kwargs)
        return context


class LoanPDFView(PDFTemplateView):
    template_name = "loans_report.html"

    def get_context_data(self, **kwargs):
        context = super(LoanPDFView, self).get_context_data(**kwargs)
        return context


class RepaymentPDFView(PDFTemplateView):
    template_name = "repayments_report.html"

    def get_context_data(self, **kwargs):
        context = super(RepaymentPDFView, self).get_context_data(**kwargs)
        return context

def excel_customers_report(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'inline; filename="Registered Customers.xls"'

    excel_file = xlwt.Workbook(encoding='utf-8')
    excel_sheet = excel_file.add_sheet('Registered Customers')

    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Customer id', 'Customer station', 'Station name',]

    for col_num in range(len(columns)):
        excel_sheet.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()

    rows = customers
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            excel_sheet.write(row_num, col_num, row[col_num], font_style)


    excel_file.save(response)
    return response

def excel_loans_report(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'inline; filename="Disbursed Loans.xls"'

    excel_file = xlwt.Workbook(encoding='utf-8')
    excel_sheet = excel_file.add_sheet('Disbursed Loans')

    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Customer id', 'Loan date', 'Loan code', 'Loan amount',]

    for col_num in range(len(columns)):
        excel_sheet.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()

    rows = loans
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            excel_sheet.write(row_num, col_num, row[col_num], font_style)


    excel_file.save(response)
    return response

def excel_repayments_report(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'inline; filename="Repayments.xls"'

    excel_file = xlwt.Workbook(encoding='utf-8')
    excel_sheet = excel_file.add_sheet('Repayments')

    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Customer id', 'Due date', 'Loan code', 'Loan status',]

    for col_num in range(len(columns)):
        excel_sheet.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()

    rows = repayments
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            excel_sheet.write(row_num, col_num, row[col_num], font_style)


    excel_file.save(response)
    return response