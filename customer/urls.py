from django.conf.urls import url
from .views import (
    customer_data,
    loan_data,
    repayment_data,
    search_results,
    process_customers_report,
    process_loans_report,
    process_repayments_report,
)
from .views import Pdf

urlpatterns = [
    url(r"^details/", customer_data, name="customer_data"),
    url(r"^searchdetails/", search_results, name="search_results"),
    url(r"^loan_details/", loan_data, name="loan_data"),
    url(r"^repayment_details/", repayment_data, name="repayment_data"),
    url(
        r"^customers_report/",
        process_customers_report,
        name="process_customers_report",
    ),
    url(r"^loans_report/", process_loans_report, name="process_loans_report"),
    url(
        r"^repayments_report/",
        process_repayments_report,
        name="process_repayments_report",
    ),
    url(
        r"^customers_pdf_report/",
        Pdf.customers_pdf_report,
        name="customers_pdf_report",
    ),
    url(r"^loans_pdf_report/", Pdf.loans_pdf_report, name="loans_pdf_report"),
    url(
        r"^repayments_pdf_report/",
        Pdf.repayments_pdf_report,
        name="repayments_pdf_report",
    ),
]

