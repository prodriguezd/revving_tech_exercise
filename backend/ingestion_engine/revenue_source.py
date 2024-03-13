from decimal import Decimal
from api.models import Customer, RevenueSource, Invoice
from django.db.models import Sum

def get_revenue_source_data(revenue_source):
    if not RevenueSource.objects.filter(name=revenue_source).exists():
        return {'status': 'error', 'message': 'This revenue source does not exists'}

    invoices_related = Invoice.objects.filter(revenue_source=revenue_source)

    if invoices_related:
        total_value = invoices_related.aggregate(total=Sum('value'))['total']
        total_advance = sum([invoice.advance_amount for invoice in invoices_related], Decimal('0.00'))
        total_expected_daily_fee = sum([invoice.expected_daily_fee for invoice in invoices_related], Decimal('0.00'))

        data = {
            'total_value': total_value,
            'total_advance': total_advance,
            'total_expected_daily_fee': total_expected_daily_fee
        }
        return {'status':'ok', 'message': data}
