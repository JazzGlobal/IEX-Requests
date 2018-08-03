#IEX API Documentation: https://iextrading.com/developer/docs/
#IEX API Terms of Use: https://iextrading.com/api-exhibit-a/
#Source: https://iextrading.com/developer/docs/#attribution
#Developer Terms: https://iextrading.com/api-terms/
import json
import requests

prefix = 'https://api.iextrading.com/1.0/'

#Builds URL and requests data from the API. Returns JSON. Supports the API's Chart, Book, Earnings, etc.
#Example: stock = getStock('aapl','chart','1d')
#symbol: Symbol for stock. 
#datatype: Determines the format and selection of certain attributes for the data to be returned. Accepted values: 'book' or 'chart'.
def getStock(symbol, datatype, time=''):
    print('Running Service: getStock ' + str(symbol) + ' ... ' + str(datatype) + ' ... ' + str(time))
    url = prefix + str('stock') + str('/') + str(symbol) + str('/') + str(datatype) + str('/') + str(time)
    
    if(datatype == 'book' or datatype == 'chart'):
        try:
            response = requests.get(url)
            return response.json()
        except urllib.error.HTTPError as err:
            if(err.code == 403 and datatype == 'book' and time != ''):
                print('Cannot specify \'time\' if \'datatype\' is set to book')
                print('Leave \'time\' empty.')
    else:
        print('\'getStock\' cannot accept ' + '\'' + str(datatype) + '\'' + ' as a parameter')
        print('Must be of value \'book\' or \'chart\'')

#Builds URL and requests data from the API's Company endpoint
#Example: getCompanyInformation('aapl')
#symbol: Symbol for stock.
def getCompanyInformation(symbol):
    url = prefix + str('stock') + '/' + str(symbol) + str('/') + str('company')
    response = requests.get(url)
    return response.json()

#Builds URL and requests data from the API's Dividend endpoint.
#Example: getDividendInformation('aapl')
#symbol: Symbol for stock.
#time: Range for data. Accepted values: '1m','3m','6m','ytd','1y','2y','5y'. Defaulted to '6m'.
def getDividendInformation(symbol, time='6m'):
    url = prefix + str('stock') + '/' + str(symbol) + '/' + str('dividends') + str('/') + str(time)
    response = requests.get(url)
    return response.json()

#Builds URL and requests data from the API's 'Earnings' endpoint.
#Example: getEarningsInformation('aapl')
#symbol: Symbol for stock.
def getEarningsInformation(symbol):
    url = prefix + str('stock') + '/' + str(symbol) + '/' + str('earnings')
    response = requests.get(url)
    return response.json()
