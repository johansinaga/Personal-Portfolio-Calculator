import sys
from yahoo_finance_api2 import share
from yahoo_finance_api2.exceptions import YahooFinanceError
from colorama import init

formatColorWhite = '\033[1;37;40m'
formatColorRed = '\033[1;31;40m'
formatColorGreen = '\033[1;32;40m'

index2weeks = -11
index1weeks = -6
indexYesterday = -2
indexToday = -1

def correctPrice(price):
	if (price == None):
		newIndex = index2weeks -1
		while (price == None):
			price = symbol_data['close'][newIndex]
			newIndex = newIndex -1
	return float(price)

# Initialize colorama for coloring
init()

# Inserting shares			//TODO: use config file?
shares = [	'ACB', 'PDD', 'YUMC', 'ACN', 'PEP',
			'DSM.AS', 'LIGHT.AS', 'RDSA.AS', 'T', 'BABA',
			'ABN.AS', 'VWRL.AS', 'NN.AS', 'SPOT', 'AAPL'
			]

# Print header
print(('\033[1;37;40mTICKER\t   Last Month Price   Yesterday Price\t1m Change %\t2w Change %\t1w Change %'))

for my_share in shares:
	my_share_date = share.Share(my_share)
	symbol_data = None
	
	# Getting data from Yahoo Finance
	try:
		symbol_data = my_share_date.get_historical(share.PERIOD_TYPE_MONTH,
											  1,
											  share.FREQUENCY_TYPE_DAY,
											  1)
	except YahooFinanceError as e:
		print("Cannot find data for ticker symbol", my_share)
		print(e.message)
		sys.exit(1)
		
	# Calculation
	lastMonthClosePrice = symbol_data['close'][0]
	_2WeeksAgoPrice = symbol_data['close'][index2weeks]
	_1WeeksAgoPrice = symbol_data['close'][index1weeks]
	yesterdayClosePrice = symbol_data['close'][indexYesterday]	
	
	
	################################################################	Handling if no price history can be found at certain date using a function
	lastMonthClosePrice = correctPrice(lastMonthClosePrice)
	_2WeeksAgoPrice = correctPrice(_2WeeksAgoPrice)
	_1WeeksAgoPrice = correctPrice(_1WeeksAgoPrice)
	yesterdayClosePrice = correctPrice(yesterdayClosePrice)
	################################################################
	

	_1MonthChangePercent = float((yesterdayClosePrice - lastMonthClosePrice)/lastMonthClosePrice*100)
	_2WeeksChangePercent = float((yesterdayClosePrice - _2WeeksAgoPrice)/_2WeeksAgoPrice*100)
	_1WeeksChangePercent = float((yesterdayClosePrice - _1WeeksAgoPrice)/_1WeeksAgoPrice*100)

	todayPrice = float(symbol_data['close'][indexToday])
	
	
	# Determine Color Format based on %
	if (_1MonthChangePercent < 0):
		formatColor1m = formatColorRed
	else:
		formatColor1m = formatColorGreen
	if (_2WeeksChangePercent < 0):
		formatColor2w = formatColorRed
	else:
		formatColor2w = formatColorGreen
	if (_1WeeksChangePercent < 0):
		formatColor1w = formatColorRed
	else:
		formatColor1w = formatColorGreen
	
	
	# Print output
	print('{}{:<15}{:6.2f}\t\t{:6.2f}\t\t{}{:6.2f}\t\t{}{:6.2f}\t\t{}{:6.2f}{}'.format
		(formatColorWhite, my_share, lastMonthClosePrice, yesterdayClosePrice, formatColor1m, _1MonthChangePercent,
		formatColor2w, _2WeeksChangePercent, formatColor1w, _1WeeksChangePercent, formatColorWhite))