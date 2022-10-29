#imports
from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse,FileResponse
from datetime import datetime

from .process import html_to_pdf 
from .pdfc import compress

import pdfkit
import json

def sort(json_data):
    #Loading json data into dictionary to pull out relevant data.
    parsed_json = json.load(json_data)

    
    #declaring dictionary to hold each transaction detail
    transData = {}

    #declaring list to hold all transactions
    parsedData = []

    #looping through dictionary holding json data to filter needed data
    for data in parsed_json:
        for i in range(len(parsed_json[data])):
            transData['date'] = parsed_json[data][i]['created_at']
            transData['amount'] = parsed_json[data][i]['amount']
            transData['description'] = parsed_json[data][i]['description']
            transData['running_balance'] = parsed_json[data][i]['running_balance']
            transData['transaction_type'] = parsed_json[data][i]['transaction_type']
            transData['currency'] = parsed_json[data][i]['currency']

            #adding each transaction information to list of transactions
            parsedData.append(transData.copy())
           
    #declaring dictionariy holding all transaction details to be passed into template
    response_dict = {}


    #populating dictionary with transactions
    for i in range(len(parsedData)):
        response_dict['Transaction{}'.format(i+1)]= parsedData[i]
    return response_dict

def convert(response_dict, user, opening_balance, closing_balance, date, start_date, end_date,amount):
    #Context variable for template
    context = {'data':response_dict, 'opening_balance_usd':opening_balance,'closing_balance_usd':closing_balance, 'amount':amount, 'user': user, 'today': date, 'start_date':start_date, 'end_date':end_date }
    
    #rendering dynamic information into static html to be converted to pdf
    content = render_to_string('main/joint_accounts.html', context)  
    #writing dynamic information into static html            
    with open('main/templates/main/statement.html', 'w') as static_file:
        static_file.write(content)

    #converting dynamic html into pdf
    options = {
        'page-size':'Tabloid',
        'encoding':'UTF-8',
        "enable-local-file-access": None,
    }
    pdf = pdfkit.from_file('/Users/mac/Django/Bitnob/account_statement/main/templates/main/statement.html','out.pdf',options=options)

    response = FileResponse(open('out.pdf', 'rb'))

    if pdf._size > 10485760:
        compress(pdf, pdf, power=4)

    return response

# Create your views here.
def index(request):
    #Retrieving Json Data
    json_data = open('/Users/mac/Django/Bitnob/account_statement/main/data.json')

    #getting date
    datetime1 = datetime.now() 
    date1 = datetime1.date()

    response_dict = sort(json_data)
    pdf = convert(response_dict, 'Munirat Oyiwola', '0.01 ', '8.529994855', date1, '2nd September', '2nd October','8.529994855')
    #rendering pdf 
    return HttpResponse(pdf, content_type='application/pdf')
    