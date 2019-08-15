import sys
from yahoo_finance_api2 import share
from yahoo_finance_api2.exceptions import YahooFinanceError
from colorama import init
from colorama import Fore, Back, Style

# Initialize colorama for coloring
init()

# Inserting shares TODO: use config file?
shares = [	'ACB', 'PDD', 'YUMC', 'ACN', 'PEP',
			'DSM.AS', 'LIGHT.AS', 'RDSA.AS', 'T', 'BABA',
			'ABN.AS', 'VWRL.AS', 'NN.AS', 'SPOT', 'AAPL'
			]

# Print header
print(('\033[1;37;40mTICKER\t\tLast Month Price     Yesterday Price\tChange in %'))

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
	lastMonthClosePrice = float(symbol_data['close'][0])
	yesterdayClosePrice = float(symbol_data['close'][-2])
	ChangePercent = float((yesterdayClosePrice - lastMonthClosePrice)/lastMonthClosePrice*100)
	
	# Print output	
	if yesterdayClosePrice < lastMonthClosePrice:		# print in red
		print('\033[1;37;40m{:<20}{:6.2f}\t\t{:6.2f}\t\t\033[1;31;40m{:6.2f}%'.format
		(my_share, lastMonthClosePrice, yesterdayClosePrice, ChangePercent, ChangePercent))
	else:												# Print in green
		print('\033[1;37;40m{:<20}{:6.2f}\t\t{:6.2f}\t\t\033[1;32;40m{:6.2f}%'.format
		(my_share, lastMonthClosePrice, yesterdayClosePrice, ChangePercent, ChangePercent))
