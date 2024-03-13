import pandas as pd
from api.models import Customer, RevenueSource, Invoice

def load_system_data(file_path=None):
    if file_path:
        data = pd.read_csv(file_path)
    else:
        data = pd.read_csv('/Users/paula/Documents/interviews/revving/backend/ingestor/data.csv')

    data = create_initial_data(data)

    #avoid duplicated invoices
    for index, row in data.iterrows():
        Invoice.objects.update_or_create(
            invoice_number=row['invoice number'],
            defaults={
                'customer_id':row['customer'],
                'date':row['date'],
                'value':row['value'],
                'haircut_percent':row['haircut percent'],
                'daily_fee_percent':row['Daily fee percent'],
                'currency':row['currency'],
                'revenue_source':row['Revenue source'],
                'expected_payment_duration':row['Expected payment duration']
            })

    return "Loaded data"


def create_initial_data(data):
    customers = data['customer'].unique()
    customer_to_id = {}
    for customer in customers:
        obj, create = Customer.objects.get_or_create(name=customer)
        customer_to_id[customer] = obj.id

    data['customer'] = data['customer'].map(customer_to_id)

    revenue_sources = data['Revenue source'].unique()
    for source in revenue_sources:
        RevenueSource.objects.get_or_create(name=source)

    return data