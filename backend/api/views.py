from ingestion_engine.data_storage import load_system_data
from ingestion_engine.revenue_source import get_revenue_source_data
from ingestion_engine.customer_totals import get_customer_totals
from rest_framework.views import APIView
from django.http import JsonResponse,  HttpResponse
import json

def load_file(request, *args, **kwargs):
    load_system_data()
    return JsonResponse({"message": "initial data loaded"})

class RevenueSourceView(APIView):
    def get(self, request, *args, **kwargs):
        revenue_source = request.GET.get('revenue_source', None)
        if revenue_source is None:
            response_data = {'status': 'error', 'message': 'No revenue source provided'}
        else:
            response_data = get_revenue_source_data(revenue_source)

        return JsonResponse(response_data)

class CustomerView(APIView):
    def get(self, request, *args, **kwargs):
        customer = request.GET.get('customer', None)
        if customer is None:
            response_data = {'status': 'error', 'message': 'No customer provided'}
        else:
            response_data = get_customer_totals(customer)

        return JsonResponse(response_data)

    def post(self, request, *args, **kwargs):
        customer = request.GET.get('customer', None)
        if customer is None:
            response_data = {'status': 'error', 'message': 'No customer provided'}
        else:
            try:
                data = json.loads(request.body.decode('utf-8'))
            except json.JSONDecodeError:
                return HttpResponse('Invalid JSON', status=400)
            file_path = data.get('file_path')
            print(file_path)
            response = load_system_data(file_path)
            response_data = {'message': response}

        return JsonResponse(response_data)
