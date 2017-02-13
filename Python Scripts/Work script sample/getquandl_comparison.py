import config
import csv
import time
from dateutil.parser import parse
timestr = time.strftime(" %Y%m%d-%H%M%S")
import time
import os
db = config.db
count = 0
from pandas_datareader import data
sym = ['fb','nke','aapl','amzn'] #enter stock symbols
tolerance_Quandl_Google = 0.10   #set tolerance to ignore difference in stock prices
newDateformat = {}    # has the date format %Y %m %d with the price
quandlcombined = {}  #has the EODdate and EODPrice
forprint =[]  #list of dict to print the results into a single csv
for symbol in sym:
    cursor = data.DataReader(symbol, 'google', '20090101', '20151231')    #pulls data for the stoackSymbol and uses google finance for the specified start and end date
    cursor["stockSymbol"] = symbol
    cursor.to_csv(symbol + "googlefinance" + ".csv")
    filename = "fromQuandl" + symbol +".csv"
    with open(filename, 'w') as csvfile:
        fieldnames = ['entityId','stockSymbol','EODdate','EODPrice']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',', lineterminator='\n')
        writer.writeheader()
        quandl =db.QuandlStockPrices.find({'stockSymbol': symbol}) #retrieves data from MongoDb
        for document in quandl:
            datarow1 ={"entityId":document["entityId"], "stockSymbol":document["stockSymbol"],"EODdate":document["EODdate"],"EODPrice":document["EODPrice"]}
            writer.writerow(datarow1)
            count+=1
            print(count)
    csvfile.close()  #closes quandl csv file


    with open('fromQuandl'+symbol+'.csv', 'r') as csvfile2:   #reads quandl csv file
        reader = csv.DictReader(csvfile2)
        for info in reader:
            quandlcombined.update({info["EODdate"]:info["EODPrice"]})  #update dict quandlcombined

        with open(symbol+'googlefinance.csv', 'r') as csvfile3:   #reads the goog finance csv file
            reader1 = csv.DictReader(csvfile3)
            googfinancedateandprice = {}
            for row in reader1:
                googfinancedateandprice.update({row["Date"]:row["Close"]})
            for Date,price in googfinancedateandprice.items():
                dt = parse(Date)  # to find the format of the date
                newfmt = dt.strftime('%Y%m%d') #converting the date(google finance) format to Ymd
                newDateformat.update({newfmt:price})
        sharedKeys = set(quandlcombined.keys()).intersection(newDateformat.keys())  #intersection of dates
        for key in sharedKeys:
            if quandlcombined[key] != newDateformat[key]:
                diff = abs(float(quandlcombined[key])-float(newDateformat[key]))
                if diff > tolerance_Quandl_Google: #check tolerance
                    print('Key: {}, Value 1: {}, Value 2: {}'.format(key, quandlcombined[key], newDateformat[key]))
                    datarow = {"stockSymbol":symbol,'quandldate': key, 'quandlprice': quandlcombined[key], "googleprice": newDateformat[key]}
                    forprint.append(datarow)
        os.remove(symbol + "googlefinance" + ".csv") #removes csv
    os.remove('fromQuandl'+symbol+'.csv')
    filename1 = "Quandl_Google_Stockprices_comparison_"+"output" + timestr + ".csv"
    with open(filename1, 'w') as csvfile1: #write output file
        fieldnames = ['stockSymbol', 'quandldate', 'quandlprice', "googleprice"]
        writer = csv.DictWriter(csvfile1, fieldnames=fieldnames, delimiter=',', lineterminator='\n')
        writer.writeheader()
        for out in forprint:
            writer.writerow(out)