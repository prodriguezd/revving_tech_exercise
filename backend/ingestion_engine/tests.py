from decimal import Decimal
from django.test import TestCase
from api.models import Customer, RevenueSource, Invoice
from api.views import get_revenue_source_data, get_customer_totals

class RevenueSourceTests(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(name='Test Customer')
        self.revenue_source_name = 'Test Revenue Source'
        self.revenue_source = RevenueSource.objects.create(name=self.revenue_source_name)
        self.invoice = Invoice.objects.create(
            invoice_number='123',
            customer=self.customer,
            revenue_source=self.revenue_source_name,
            date='2020-01-01',
            value=Decimal('100.00'),
            haircut_percent=Decimal('10.00'),
            daily_fee_percent=Decimal('1.00'),
            currency='USD',
            expected_payment_duration=30
        )

    def test_revenue_source_does_not_exist(self):
        response = get_revenue_source_data('Nonexistent Revenue Source')
        self.assertEqual(response['status'], 'error')
        self.assertEqual(response['message'], 'This revenue source does not exists')

    def test_revenue_source_exists_with_invoices(self):
        response = get_revenue_source_data(self.revenue_source_name)
        self.assertEqual(response['status'], 'ok')
        data = response['message']
        self.assertEqual(data['total_value'], Decimal('100.00'))
        self.assertEqual(data['total_advance'], Decimal('90.00'))



class CustomerTotalTests(TestCase):
    def setUp(self):
        # Set up test data
        self.customer_name = "Test Customer"
        self.customer = Customer.objects.create(name=self.customer_name)
        self.revenue_source1 = RevenueSource.objects.create(name="Source 1")
        self.revenue_source2 = RevenueSource.objects.create(name="Source 2")
        Invoice.objects.create(
            invoice_number="INV001",
            customer=self.customer,
            revenue_source=self.revenue_source1.name,
            date="2021-01-01",
            value=Decimal("100.00"),
            haircut_percent=Decimal("10.00"),
            daily_fee_percent=Decimal("1.00"),
            currency="USD",
            expected_payment_duration=30
        )
        Invoice.objects.create(
            invoice_number="INV002",
            customer=self.customer,
            revenue_source=self.revenue_source2.name,
            date="2021-02-01",
            value=Decimal("200.00"),
            haircut_percent=Decimal("5.00"),
            daily_fee_percent=Decimal("1.50"),
            currency="USD",
            expected_payment_duration=60
        )

    def test_customer_does_not_exist(self):
        response = get_customer_totals("Nonexistent Customer")
        self.assertEqual(response['status'], 'error')
        self.assertIn('does not exists', response['message'])

    def test_customer_exists_no_invoices(self):
        Customer.objects.create(name="Customer No Invoices")
        response = get_customer_totals("Customer No Invoices")
        self.assertEqual(response['status'], 'ok')
        self.assertEqual(len(response['message']), 0)  # Expect empty data list

    def test_customer_exists_with_invoices(self):
        response = get_customer_totals(self.customer_name)
        self.assertEqual(response['status'], 'ok')
        self.assertEqual(len(response['message']), 2)  # Two revenue sources

        # Check for correct calculation of total advances
        # Assuming advance_amount calculation logic is correct and setup data is unchanged
        for item in response['message']:
            if item['revenue_source'] == self.revenue_source1.name:
                self.assertEqual(item['total_advance'], Decimal("90.00"))  # Example based on your advance_amount logic
            elif item['revenue_source'] == self.revenue_source2.name:
                self.assertEqual(item['total_advance'], Decimal("190.00"))  # Example based on your advance_amount logic