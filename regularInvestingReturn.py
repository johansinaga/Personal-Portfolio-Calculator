import sys
import configparser
import datetime
from yahoo_finance_api2 import share
from yahoo_finance_api2.exceptions import YahooFinanceError

# Convert prices (list format) to specific decimal number
def convertPrices(prices, decimalNumber):
    # Converting integer list to string list 
    roundedPrices = [round(price, decimalNumber) for price in prices]
    return(roundedPrices)
def getPriceData(sharename, periodType = share.PERIOD_TYPE_YEAR, periodValue = 5, frequencyType = share.FREQUENCY_TYPE_MONTH, frequencyValue = 1):
    my_share = sharename
    my_share_date = share.Share(my_share)

    try:
        symbol_data = my_share_date.get_historical(periodType, periodValue,
												   frequencyType, frequencyValue)										   

    except YahooFinanceError as e:
        print("Cannot find data for ticker symbol '{}'".format(my_share))
        print(e.message)
        sys.exit(1)
    return symbol_data
	
# Main code
print ("")
print ("Fill in some details....")
shareToUse = input("The ticker of the Stock/ETF to invest in: ")
priceData = getPriceData(shareToUse)
regularInleg = int(input("Amount to invest regularly: € "))
totalYears = int(input("Total years to invest: "))
buyMoment = input("Price bought in the day ('open', 'high', 'low', 'close'): ")

priceData = getPriceData(shareToUse, periodValue = totalYears)
prices = convertPrices(priceData[buyMoment],2)


# Calculation
positions = []
periodiekInleg = []
savedMoney = 0
for price in prices:
    inleg = regularInleg + savedMoney
    positionBought = round(inleg//price)
    if positionBought == 0:
        savedMoney = savedMoney + regularInleg
        actualInvestment = 0
    else:
        savedMoney = 0
        leftover = round(inleg - (price*positionBought), 2)
        savedMoney = savedMoney + leftover
        actualInvestment = inleg - leftover
    positions.append(positionBought)
    periodiekInleg.append(actualInvestment)

totalInleg = round(sum(periodiekInleg), 2)
buyCount = sum(1 for buy in positions if buy >= 1)
currentPosition = sum(positions)

latestPriceData = getPriceData(shareToUse, share.PERIOD_TYPE_DAY, 1, share.FREQUENCY_TYPE_DAY, 1)
latestClosePrice = round(latestPriceData['close'][0],2)
latestWorth = round(latestClosePrice * currentPosition,2)

# Print out Result
if buyCount == 0:
    print("")
    print ("Based on the given input data, you would not have been able to buy any shares during this period")
else:
    print ("")
    print ("Based on the given input data")
    print ("You would have been investing for the last", totalYears, "years")
    print ("Bought in", buyCount, "times, and accumulated", currentPosition, "shares of {}".format(shareToUse))
    print ("With a total investment of €", totalInleg)
    print ("")
    print ("Latest price of {} today is {}".format(shareToUse, latestClosePrice))
    print ("Which gives you a total worth today of €", latestWorth)
    print ("")
    difference = round(latestWorth - totalInleg, 2)
    diffPercentage = round(difference/totalInleg*100, 2)
    diffPercentageAverage = round(diffPercentage/5, 2)
    print ("You have a total profit of €", difference)
    print ("A {}% portfolio increase".format(diffPercentage))
    print ("Or annual growth of {}%".format(diffPercentageAverage))