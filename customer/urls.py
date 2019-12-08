from django.conf.urls import url
from .views import customer_data, loan_data, repayment_data

urlpatterns = [
    url("details/", customer_data, name="customer_data"),
    url("loan_details/", loan_data, name="loan_data"),
    url("repayment_details/", repayment_data, name="repayment_data"),
]

