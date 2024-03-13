from django.db import models
from decimal import Decimal

class Customer(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class RevenueSource(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Invoice(models.Model):
    invoice_number = models.CharField(max_length=20, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='invoice_customer')
    revenue_source = models.CharField(max_length=255)
    date = models.DateField()
    value = models.DecimalField(max_digits=12, decimal_places=2)
    haircut_percent = models.DecimalField(max_digits=5, decimal_places=2)
    daily_fee_percent = models.DecimalField(max_digits=5, decimal_places=2)
    currency = models.CharField(max_length=3)
    expected_payment_duration = models.PositiveIntegerField()

    @property
    def advance_amount(self):
        """Calculate the amount available for advance. it applies haircut"""
        return self.value * ((Decimal('100.00') - self.haircut_percent) / Decimal('100.00'))

    @property
    def expected_daily_fee(self):
        "expected fee based on the daily fee"
        daily_fee = Decimal('1.00') - self.daily_fee_percent
        return self.advance_amount * (daily_fee ** self.expected_payment_duration - Decimal('1.00'))
