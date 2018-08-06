import services

class Stock:
	def __init__(self,symbol):
		self.symbol = symbol
		self.earnings = services.GetEarnings(self.symbol)
		self.company = services.GetCompany(self.symbol)
		self.charts = []
		self.charts.append(services.GetStock(self.symbol,'1d'))
		self.charts.append(services.GetStock(self.symbol,'1m'))
		self.charts.append(services.GetStock(self.symbol,'3m'))
		self.charts.append(services.GetStock(self.symbol,'6m'))
		self.charts.append(services.GetStock(self.symbol,'1y'))
		self.charts.append(services.GetStock(self.symbol,'2y'))
		self.charts.append(services.GetStock(self.symbol,'5y'))

