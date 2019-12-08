# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Loans, LoanStatus, CustomerStations


class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        "customer_id",
        "loan_amount",
        "loan_code",
        "loan_date",
        "due_date",
        "loan_status",
        "customer_station",
    )
    search_fields = ("customer_id", "customer_station")


admin.site.register(Loans, CustomerAdmin)


class LoanStatusAdmin(admin.ModelAdmin):
    list_display = ("status_id", "loan_status")


admin.site.register(LoanStatus, LoanStatusAdmin)


class CustomerStationsAdmin(admin.ModelAdmin):
    list_display = (
        "station_id",
        "station_name",
        "daily_target",
        "monthly_target",
    )


admin.site.register(CustomerStations, CustomerStationsAdmin)
