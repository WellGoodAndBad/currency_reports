from django.urls import path
from .views import CurrView, CSVReport, PDFView, XLSXView


urlpatterns = [
    path('', CurrView.as_view(), name='home_page'),
    path('get_csv', CSVReport.as_view(), name='download_csv'),
    path('get_pdf', PDFView.as_view(), name='download_pdf'),
    path('get_xlsx', XLSXView.as_view(), name='download_xlsx')
]