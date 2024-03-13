from collections import defaultdict
from decimal import Decimal
from api.models import Customer, RevenueSource, Invoice
from django.db.models import Sum

def get_customer_totals(customer):
    customer_obj = Customer.objects.filter(name=customer).first()
    if not customer_obj:
        return {'status': 'error', 'message': 'This customer source does not exists'}

    customer_invoices = Invoice.objects.filter(customer=customer_obj.id)

    advance_totals = defaultdict(Decimal)
    for invoice in customer_invoices:
        advance = invoice.advance_amount
        advance_totals[invoice.revenue_source] += advance

    data = []

    for revenue_source, total_advance in advance_totals.items():
        res = {
            'revenue_source': revenue_source,
            'total_advance': total_advance
        }
        data.append(res)


    return {'status': 'ok', 'message': data}
