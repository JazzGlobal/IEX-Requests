#IEX API Documentation: https://iextrading.com/developer/docs/
#IEX API Terms of Use: https://iextrading.com/api-exhibit-a/
#Source: https://iextrading.com/developer/docs/#attribution
#Developer Terms: https://iextrading.com/api-terms/
import requests
import json

#Builds URL from given arguments. 
def BuildURL(symbol,typeOfUrl,time=''):
	prefix = 'https://api.iextrading.com/1.0/stock/'
	
	url = prefix + symbol + '/' + typeOfUrl + '/' + time
	response = requests.get(url)
	if(response.status_code == 404):
		print('Unknown symbol. Cannot retrieve JSON data.')
	elif(time != '1d' and time != '1m' and time != '3m' and time != '6m' and time != '1y' and time != '2y' and time != '5y' and time != ''):
		print('Time value is invalid. Cannot retrieve JSON data.')
	else:
		return response.json()

def GetStock(symbol, time='1d'):
	return BuildURL(symbol,'chart',time)
def GetDividend(symbol,time='1y'):
	return BuildURL(symbol,'dividends',time)
def GetEarnings(symbol):
	return BuildURL(symbol,'earnings')
def GetCompany(symbol):
	return BuildURL(symbol,'company')
