import config
import csv
import time
import itertools
import dateutil.relativedelta
from itertools import cycle, islice, dropwhile
import datetime
db = config.db
count = 0
from itertools import cycle, islice, dropwhile
with open('stock.csv', 'r') as csvfile1:
    reader = csv.DictReader(csvfile1)
    tid = []
    stock = []
    for row in reader:
        if row["termId"]:
            tid.append(row["termId"])
        if row["stockSymbol"]:
            stock.append(row["stockSymbol"])
timestr = time.strftime(" %Y%m%d-%H%M%S")
filename = "splitFYFQ" + timestr + ".csv"
with open(filename, 'w') as csvfile:
    fieldnames = ['termId','entityId','companyName','stockSymbol','FY', 'FQ', 'filingPeriod', 'fiscalYearEnd', 'filingHTML']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',', lineterminator='\n')
    writer.writeheader()
    for symbol in stock:
        for tt in tid:
            filing = db.SECFilings.find({"stockSymbol": symbol})
            for document in filing:
                try:
                    a = str(document["filingPeriod"])
                    monthday = (a[4:])
                    yearpart = int((a[:4]))
                    x = str(document["fiscalYearEnd"])
                    months = int((x[:2]))
                    monthpart = int((a[4:-2]))
                except ValueError:
                    continue

                datarow = {'termId': tt,'entityId': document["entityId"],'companyName':document["companyName"], 'stockSymbol': document["stockSymbol"], "filingPeriod": document["filingPeriod"], 'fiscalYearEnd': document["fiscalYearEnd"],'filingHTML': document["filingHTML"]}
                aaa = [12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
                abc = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
                if months > 5:
                    if months in abc:
                        cycled = cycle(aaa)
                        skipped = dropwhile(lambda x: x != months, cycled)
                        sliced = islice(skipped, None, 15)
                        result = list(sliced)  # create a list from iterator
                        az0 = result[9]
                        az1 = result[10]
                        az2 = result[11]
                        bz0 = result[6]
                        bz1 = result[7]
                        bz2 = result[8]
                        cz0 = result[3]
                        cz1 = result[4]
                        cz2 = result[5]
                        dz0 = result[0]
                        dz1 = result[1]
                        dz2 = result[2]
                        Q1 = [az0, az1, az2]
                        Q2 = [bz0, bz1, bz2]
                        Q3 = [cz0, cz1, cz2]
                        FY = [dz0, dz1, dz2]
                        if monthpart in Q1:
                            d = datetime.datetime.strptime(a, "%Y%m%d")
                            resul1 = d.year
                            datarow.update({'FY': resul1, 'FQ': "Q1"})
                        elif monthpart in Q2:
                            d = datetime.datetime.strptime(a, "%Y%m%d")
                            resul2 = d.year
                            datarow.update({'FY': resul2, 'FQ': "Q2"})
                        elif monthpart in Q3:
                            d = datetime.datetime.strptime(a, "%Y%m%d")
                            resul3 = d.year
                            datarow.update({'FY': resul3, 'FQ': "Q3"})
                        elif monthpart in FY:
                            d = datetime.datetime.strptime(a, "%Y%m%d")
                            resul4 = d.year
                            datarow.update({'FY': resul4, 'FQ': "FY"})
                else:
                    if months in abc:
                        cycled = cycle(aaa)
                        skipped = dropwhile(lambda x: x != months, cycled)
                        sliced = islice(skipped, None, 15)
                        result = list(sliced)  # create a list from iterator
                        az0 = result[9]
                        az1 = result[10]
                        az2 = result[11]
                        bz0 = result[6]
                        bz1 = result[7]
                        bz2 = result[8]
                        cz0 = result[3]
                        cz1 = result[4]
                        cz2 = result[5]
                        dz0 = result[0]
                        dz1 = result[1]
                        dz2 = result[2]
                        Q1 = [az0, az1, az2]
                        Q2 = [bz0, bz1, bz2]
                        Q3 = [cz0, cz1, cz2]
                        FY = [dz0, dz1, dz2]
                        if monthpart in Q1:
                            d = datetime.datetime.strptime(a, "%Y%m%d")
                            d1 = d - dateutil.relativedelta.relativedelta(months=3)
                            resul1 = int(d1.year)
                            datarow.update({'FY': resul1, 'FQ': "Q1"})
                        elif monthpart in Q2:
                            d = datetime.datetime.strptime(a, "%Y%m%d")
                            d2 = d - dateutil.relativedelta.relativedelta(months=3)
                            resul2 = int(d2.year)
                            datarow.update({'FY': resul2, 'FQ': "Q2"})
                        elif monthpart in Q3:
                            d = datetime.datetime.strptime(a, "%Y%m%d")
                            d3 = d - dateutil.relativedelta.relativedelta(months=3)
                            resul3 =int(d3.year)
                            datarow.update({'FY': resul3, 'FQ': "Q3"})
                        elif monthpart in FY:
                            d = datetime.datetime.strptime(a, "%Y%m%d")
                            resul4 = int(d.year)-1
                            datarow.update({'FY': resul4, 'FQ': "FY"})
                writer.writerow(datarow)
                count += 1
                print(count)
print(count)
print("completed program successfully")