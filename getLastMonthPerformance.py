import sys
from yahoo_finance_api2 import share
from yahoo_finance_api2.exceptions import YahooFinanceError


shares = [	'ACB', 'PDD', 'YUMC', 'ACN', 'PEP',
			'DSM.AS', 'LIGHT.AS', 'RDSA.AS', 'T', 'BABA',
			'ABN.AS', 'VWRL.AS', 'NN.AS', 'SPOT', 'AAPL'
			]

print(('TICKER\t\t\tLast Month Price\tYesterday Price\t\tChange in %'))

for my_share in shares:
	my_share_date = share.Share(my_share)
	symbol_data = None

	try:
		symbol_data = my_share_date.get_historical(share.PERIOD_TYPE_MONTH,
											  1,
											  share.FREQUENCY_TYPE_DAY,
											  1)
	except YahooFinanceError as e:
		print("Cannot find data for ticker symbol", my_share)
		print(e.message)
		sys.exit(1)

	lastMonthClosePrice = float(symbol_data['close'][0])
	yesterdayClosePrice = float(symbol_data['close'][-2])
	ChangePercent = float(yesterdayClosePrice - lastMonthClosePrice)
	
	'''
	print ("Share: ", my_share)
	print ("")
	print ("Last month price:\t {:.2f}".format(lastMonthClosePrice))
	print ("Yesterday price:\t {:.2f}".format(yesterdayClosePrice))
	print ("Change:\t\t\t {:.2f}".format(ChangePercent), "%")
	print ("")
	print ("")
	'''
	
	print('{:<20}\t{:5.2f}\t\t\t{:6.2f}\t\t\t{:2.2f}%'.format(my_share, lastMonthClosePrice, yesterdayClosePrice, ChangePercent, ChangePercent))