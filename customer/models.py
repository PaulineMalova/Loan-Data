from django.db import models


class CustomerStations(models.Model):
    station_id = models.CharField(max_length=50, blank=True, null=False, primary_key=True)
    station_name = models.CharField(max_length=110, blank=True, null=True)
    daily_target = models.CharField(max_length=50, blank=True, null=True)
    monthly_target = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "customer_stations"

    def __str__(self):
        return self.station_name


class Loans(models.Model):
    loan_date = models.DateField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    loan_code = models.BigIntegerField(blank=True, null=True)
    loan_amount = models.BigIntegerField(blank=True, null=True)
    loan_status = models.CharField(max_length=50, blank=True, null=True)
    customer_id = models.CharField(max_length=50, blank=True, null=False, primary_key=True, unique=True)
    customer_station = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "loans"

    def __str__(self):
        return ({} - {}).format(self.customer_id, self.loan_amount)


class LoanStatus(models.Model):
    status_id = models.CharField(max_length=50, blank=True, null=False, primary_key=True)
    loan_status = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "loan_status"

    def __str__(self):
        return self.loan_status
