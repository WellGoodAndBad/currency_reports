import csv
import io
import os

import requests
import pdfkit

url = "https://open.er-api.com/v6/latest/USD"


def get_api_data(url: str):
    try:
        resp = requests.get(url=url)
        return resp.json()
    except:
        return {}


def create_pdf(data: dict):

    body = f"""
        <html>
          <head>
            <meta charset="utf-8">
            <meta name="pdfkit-page-size" content="Legal"/>
            <meta name="pdfkit-orientation" content="Landscape"/>
          </head>
            <div style="text-align: center">
                %s
            </div>
          </html>
        """

    str_list = [
        f'<p>{k}: {v}</p>'
        for k, v in data.items()
    ]
    str_for_pdf = ''.join(str_list)
    if not os.path.exists('pdf_docs'):
        os.makedirs('pdf_docs')
    pdfkit.from_string(body % str_for_pdf, f'pdf_docs/currency.pdf')

