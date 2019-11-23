import sys
import configparser
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

def determineColor(priceChange):
    if (priceChange < 0):
        formatColor = formatColorRed
    else:
        formatColor = formatColorGreen
    return formatColor

# Initialize colorama for coloring
init()

# Inserting shares
configParser = configparser.RawConfigParser()
configFilePath = r'portfolioConfig.txt'
configParser.read(configFilePath)

allTickers = configParser.items('Portfolio')
shares = []
for ticker in allTickers:
	shares.append(ticker[1])

# Print header
print(('\033[1;37;40mTICKER\t   Last Month Price   Today Price    1m Change %\td-9(%)\td-8(%)\td-7(%)\td-6(%)\td-5(%)\td-4(%)\td-3(%)\td-2(%)\td-1(%)\t Today'))

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
    yesterdayClosePrice = symbol_data['close'][indexYesterday]
    todayPrice = symbol_data['close'][indexToday]

    priceChangeList = []

    dayIndex = 10
    index = 0
    for i in range(-11, -1):
        priceThisDay = symbol_data['close'][i]
        priceNextDay = symbol_data['close'][i+1]
        priceChange = priceNextDay - priceThisDay
        priceChangePercent = priceChange/priceThisDay*100

        priceChangeList.insert(index, float(priceChangePercent))
        dayIndex-=1
        index+=1

    lastMonthClosePrice = correctPrice(lastMonthClosePrice)
    yesterdayClosePrice = correctPrice(yesterdayClosePrice)

    # Getting the price changes of the last 10 days
    d_9=priceChangeList[0]
    d_8=priceChangeList[1]
    d_7=priceChangeList[2]
    d_6=priceChangeList[3]
    d_5=priceChangeList[4]
    d_4=priceChangeList[5]
    d_3=priceChangeList[6]
    d_2=priceChangeList[7]
    d_1=priceChangeList[8]
    d_0=priceChangeList[9]


    _1MonthChangePercent = float((todayPrice - lastMonthClosePrice)/lastMonthClosePrice*100)


	# Determine Color Format based on %
    formatColor1m = determineColor(_1MonthChangePercent)
    formatcolor_d_9 = determineColor(d_9)
    formatcolor_d_8 = determineColor(d_8)
    formatcolor_d_7 = determineColor(d_7)
    formatcolor_d_6 = determineColor(d_6)
    formatcolor_d_5 = determineColor(d_5)
    formatcolor_d_4 = determineColor(d_4)
    formatcolor_d_3 = determineColor(d_3)
    formatcolor_d_2 = determineColor(d_2)
    formatcolor_d_1 = determineColor(d_1)
    formatcolor_d_0 = determineColor(d_0)


	# Print output
    print('{}{:<15}{:6.2f}\t\t{:6.2f}\t      {}{:6.2f}\t      {}{:6.2f}  {}{:6.2f}  {}{:6.2f}  {}{:6.2f}  '
          '{}{:6.2f}  {}{:6.2f}  {}{:6.2f}  {}{:6.2f}  {}{:6.2f}    {}{:6.2f}{}'.format
          (formatColorWhite, my_share, lastMonthClosePrice, todayPrice, formatColor1m, _1MonthChangePercent,
           formatcolor_d_9, d_9, formatcolor_d_8, d_8, formatcolor_d_7, d_7, formatcolor_d_6, d_6, formatcolor_d_5, d_5,
           formatcolor_d_4, d_4, formatcolor_d_3, d_3, formatcolor_d_2, d_2, formatcolor_d_1, d_1, formatcolor_d_0, d_0,
           formatColorWhite))