import csv
import io
import openpyxl

from django.conf import settings
from django.http import HttpResponse, FileResponse
from django.shortcuts import render
from django.views.generic.list import View

from . import service


class CurrView(View):

    def get(self, request):
        context = service.get_api_data(url=service.url)
        return render(request=request,
                      template_name='reports/main_page.html',
                      context=context)


class CSVReport(View):
    def get(self, request):
        file_out = io.StringIO()
        data = service.get_api_data(url=service.url)
        writer = csv.DictWriter(file_out, ["currency", "rate"])
        rows = [
            {"currency": key, "rate": value}
            for key, value in data["rates"].items()
        ]
        writer.writerows(rows)
        file = file_out.getvalue()
        filename = 'report.csv'
        response = HttpResponse(content_type="text/csv")
        response['Content-Disposition'] = "attachment;filename=%s" % filename
        response.write(file)
        return response


class XLSXView(View):

    def get(self, request):
        data = service.get_api_data(url=service.url)["rates"]
        file_out = io.BytesIO()
        wb = openpyxl.Workbook()
        sheet = wb.active
        for k, v in data.items():
            sheet.append([k, v])
        wb.save(file_out)
        file = file_out.getvalue()
        filename = 'report.xlsx'
        response = HttpResponse(content_type="text/xlsx")
        response['Content-Disposition'] = "attachment;filename=%s" % filename
        response.write(file)
        return response


class PDFView(View):
    def get(self, request):
        data = service.get_api_data(url=service.url)["rates"]
        service.create_pdf(data)
        pdf_path = settings.PDF_PATH
        return FileResponse(open(pdf_path, 'rb'), content_type='application/pdf')

