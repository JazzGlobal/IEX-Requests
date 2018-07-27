import services 
import xlwt
import xlrd
import csv
from xlutils.copy import copy

#Stock object that contains the symbol and various market information. 
class Stock:
    def __init__(self,symbol):
        self.symbol = symbol     
        #Creates list object for various charts. 
        self.charts = []
        self.charts.append(self.getChart('1d'))
        self.charts.append(self.getChart('1m'))
        self.charts.append(self.getChart('3m'))
        self.charts.append(self.getChart('6m'))
        self.charts.append(self.getChart('1y'))
        self.charts.append(self.getChart('2y'))
        self.charts.append(self.getChart('5y'))
        
        self.earnings = self.getEarnings()

        #Creates a list object for various dividends
        self.dividends = []
        self.dividends.append(self.getDividend('1d'))
        self.dividends.append(self.getDividend('1m'))
        self.dividends.append(self.getDividend('3m'))
        self.dividends.append(self.getDividend('6m'))
        self.dividends.append(self.getDividend('1y'))
        self.dividends.append(self.getDividend('2y'))
        self.dividends.append(self.getDividend('5y'))      

    #Returns chart from stock. Shouldn't typically run this. It runs upon creation of a 'Stock' object.
    def getChart(self,time):
        return services.getStock(self.symbol,'chart',time)

    #Returns dividend information for stock. Shouldn't run this. It will be called upong creation of a 'Stock' object
    def getDividend(self,time):
        return services.getDividendInformation(self.symbol,time)

    #Returns earnings information for stock. Shouldn't run this. It will be called upong creation of a 'Stock' object
    def getEarnings(self):
        return services.getEarningsInformation(self.symbol)

#Returns stock object.
def CreateStock(symbol):
    stockObj = Stock(symbol)
    return stockObj

def CreateStyle(fontname, color):
    style = xlwt.XFStyle()
    pattern = xlwt.Pattern()
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = xlwt.Style.colour_map[color]
    style.pattern = pattern
    font = xlwt.Font()
    font.name = fontname
    style.font = font
    return style

#Function to write labels, function to write data.
def ExportStocks(stockList,filename):
    workbook = copy(xlrd.open_workbook('template.xlsx'))
    s = workbook.get_sheet(0)

    leftStyle = CreateStyle('Calibri','light_orange')
    rightStyle = CreateStyle('Calibri','light_green')

    #Writes labels and other non-data to spreadsheet.
    def ArrangeLabels():
        print('arranging labels')
        i = 1
        for stock in stockList:
            s.write(i,0,str(stock.symbol),leftStyle)
            i = i + 1
        
    #Writes data to spreadsheet
    def ArrangeValues():
        
        def writeMarketOpen():
            #i always starts at 1 so the values don't overwrite the labels.
            i = 1
            for stock in stockList:
                chart = stock.charts[0]
                
                try:
                    marketOpen = chart[0]['marketOpen']
                    s.write(i,7,marketOpen,leftStyle)
                    i = i + 1
                except KeyError as e:
                    print(e, 'Has occured ... Atempting to find next valid "marketOpen". ')
                    j = 1
                    valueFound = False
                    while(valueFound == False):
                        if('marketOpen' in chart[j]):
                            marketOpen = chart[j]['marketOpen']
                            s.write(i,7,marketOpen,leftStyle)
                            valueFound = True
                        j = j + 1
                    i = i + 1
        
        def writeMarketClose():
            i = 1
            for stock in stockList:
                chart = stock.charts[0]
                lastEntry = len(chart) - 1
                #marketClose = 0
                
                try: 
                    marketClose = chart[lastEntry]['marketClose']
                    s.write(i,1,marketClose,leftStyle)
                    print(stock.symbol, 'MarketClose Written')
                    i = i + 1
                except KeyError as e:
                    print(e, ' Has occured... Attempting to find next valid "marketCLose". ')
                    j = lastEntry -1
                    while(j > 0):
                        if('marketClose' in chart[j]):
                            marketClose = chart[j]['marketClose']
                            s.write(i,1,marketClose,leftStyle)
                            print(stock.symbol, 'MarketClose written after keyerror fix')
                            j = 0
                        j = j - 1
                    i = i + 1
                    
        #Iterates through 1D chart in stock and finds the highest 'marketHigh' value.            
        def writeMarketHigh():
            i = 1
            for stock in stockList:
                chart = stock.charts[0]
                numberList = []
                for chunk in chart:
                    numberList.append(chunk['marketHigh'])
                s.write(i,6,max(numberList),leftStyle)
                i = i + 1

        def writeEarnings():
            i = 1
            for stock in stockList:
                earnings = stock.earnings['earnings'][0]
                #Check to see if field is 'null'. If so, then set it to 0. 
                if(earnings['EPSSurpriseDollar'] == None):
                    earnings['EPSSurpriseDollar'] = 0
                    
                s.write(i,2,earnings['actualEPS'],leftStyle)
                s.write(i,3,earnings['EPSSurpriseDollar'],leftStyle)
                s.write(i,4,earnings['yearAgoChangePercent'],leftStyle)
                i = i + 1

        writeMarketClose()
        writeMarketOpen()
        writeEarnings()
        writeMarketHigh()

    #Writes Formulas to spreadsheet
    def ArrangeFormulas():
        s.write(1,12,xlwt.Formula("((B2*G2)/H2)+(C2*8.5+(2*((1.6*D2/(C2-D2))+(1.4*E2))))"),rightStyle)
        s.write(1,13,xlwt.Formula("-(B2-M2)"),rightStyle)
        s.write(1,14,xlwt.Formula("(N2*P2)-10"),rightStyle)
        s.write(1,15,xlwt.Formula("FLOOR(300/B2,1)"),rightStyle)


    ArrangeLabels()
    ArrangeValues()
    ArrangeFormulas()
    
    workbook.save(str(filename) + '.xls')

def GetStocksFromFile(filename):
    #Returns all of the symbols found in specified CSV file.
    with open(filename, encoding='utf-8') as f:
        reader = csv.reader(f)
        data = []
        for field in reader:
            data.append(field)
        f.close()

        #List of 'Stock' objects.
        stockList = []
        
        #Creates a list of 'Stock' objects by iterating through the 'data' list and using the 'CreateStock()' function.
        for i in range(0,len(data)):
            j = 0
            for symbol in data[i]:
                stockList.append(CreateStock(symbol))
            j = j + 1
            
    return stockList

#Returns dict object of averages from stock charts.
def AverageStocks(chart):
    averageOpen = 0
    averageHigh = 0 
    averageLow = 0
    averageChangePercent = 0
    i = 0

    #Sums the values for 'open', 'high', 'low', and 'changePercent' for all dataChunks in chart.
    for dataChunk in chart:
        averageOpen = averageOpen + dataChunk['open']
        averageHigh = averageHigh + dataChunk['high']
        averageLow = averageLow + dataChunk['low']
        averageChangePercent = averageChangePercent + dataChunk['changePercent']
        i = i + 1

    #Calculates averages of 'open', 'high', 'low', and 'changePercent' in the given chart object.
    averageOpen = averageOpen / i
    averageHigh = averageHigh / i
    averageLow = averageLow / i
    averageChangePercent = averageChangePercent / i

    #Puts averages in a dictionary object
    averages = {}
    averages['averageOpen'] = averageOpen
    averages['averageHigh'] = averageHigh
    averages['averageLow'] = averageLow
    averages['averageChangePercent'] = averageChangePercent

    #Returns 'averages' dictionary object
    return averages


