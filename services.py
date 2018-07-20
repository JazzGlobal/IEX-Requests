import json
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import datetime

#URL building prefix. 
prefix = 'https://api.iextrading.com/1.0/'

#Builds URL and requests data from the API. Returns JSON. Supports the API's Chart, Book, Earnings, etc.
#Example: stock = getStock('aapl','chart','1d')
def getStock(symbol, datatype, time=''):
    print('Running Service: getStock ' + str(symbol) + ' ... ' + str(datatype) + ' ... ' + str(time))
    url = prefix + str('stock') + str('/') + str(symbol) + str('/') + str(datatype) + str('/') + str(time)
    try:
        response = requests.get(url)
        return response.json()
    except urllib.error.HTTPError as err:
        if(err.code == 403 and datatype == 'book' and time != ''):
            print('Cannot specify \'time\' if \'datatype\' is set to book')

#Builds URL and requests data from the API's Company endpoint
#Example: getCompanyInformation('aapl')
def getCompanyInformation(symbol):
    url = prefix + str('stock') + '/' + str(symbol) + str('/') + str('company')
    response = requests.get(url)
    return response.json()

#Builds URL and requests data from the API's Dividend endpoint.
#Example: getDividendInformation('aapl')
def getDividendInformation(symbol, time='6m'):
    url = prefix + str('stock') + '/' + str(symbol) + '/' + str('dividends') + str('/') + str(time)
    response = requests.get(url)
    return response.json()

#Builds URL and requests data from the API's 'Earnings' endpoint.
#Example: getEarningsInformation('aapl')
def getEarningsInformation(symbol):
    url = prefix + str('stock') + '/' + str(symbol) + '/' + str('earnings')
    response = requests.get(url)
    return response.json()

#Sends an email from the specified account to another specified account.
#subject: Subject line of email
#fileNameList: filepath list to be sent to user.
#Example: sendEmail('email@gmail.com','password','receiver@gmail.com','IMPORTANT NOTICE', ['filepath1','filepath2']
def sendEmail(email_user,password, email_send, subject,fileNameList):
    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = email_send
    msg['Subject'] = subject

    now = datetime.datetime.now()
    body = "Here are the stocks from %s" % str(now)
    msg.attach(MIMEText(body,'plain'))
    
    #Iterates through the fileNameList and attaches each to the email.
    for file in fileNameList:
        
        attachment = open(file,'rb')

        part = MIMEBase('application','octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % file) 
        print('attaching file')
        msg.attach(part)
    
    text = msg.as_string()
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(email_user,str(password))
    server.sendmail(email_user,email_send,text)
    server.quit()
    print('Email Sent')
    