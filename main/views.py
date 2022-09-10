#imports
from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse

from .process import html_to_pdf 
import json


# Create your views here.
def index(request):
    #Retrieving Json Data
    json_data = open('/Users/mac/Django/Bitnob/account_statement/main/data.json')

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

            #adding each transaction information to list of transactions
            parsedData.append(transData.copy())
           
    #declaring dictionariy holding all transaction details to be passed into template
    response_dict = {}

    #populating dictionary with transactions
    for i in range(len(parsedData)):
        response_dict['Transaction{}'.format(i+1)]= parsedData[i]

    #Context variable for template
    context = {'data':response_dict}
    
    #rendering dynamic information into static html to be converted to pdf
    content = render_to_string('main/accounts.html', context)  
    #writing dynamic information into static html            
    with open('main/templates/main/statement.html', 'w') as static_file:
        static_file.write(content)

    #converting dynamic html into pdf
    pdf = html_to_pdf('main/statement.html')
    
          
    #rendering pdf 
    return HttpResponse(pdf, content_type='application/pdf')
    