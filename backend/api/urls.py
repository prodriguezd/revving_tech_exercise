from django.urls import path

from . import views


urlpatterns = [
    path('loadCSVFile', views.load_file),
    path('revenueSource/', views.RevenueSourceView.as_view()),
    path('customer/', views.CustomerView.as_view())
]