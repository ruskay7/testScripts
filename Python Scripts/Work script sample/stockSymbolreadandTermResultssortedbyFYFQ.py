import config
import csv
import time
db = config.db
#enter value
maximum = 0.30
start = 2009
end = 2016
endd = end + 1
timestr = time.strftime(" %Y%m%d-%H%M%S")
filename = "outputTermResults" + timestr + ".csv"
#csv writing
with open(filename, 'w') as csvfile:
    fieldnames = ['termId', 'entityId', 'FYFQ', 'stockSymbol', 'value', 'ChangePcntPoP', 'ChangePcntPoPExp']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',', lineterminator='\n')
    writer.writeheader()
    #csv read (opening the csv file which contains the list of terms and entities)
    with open('RohithTestFile1.csv', 'r') as csvfile1:
        reader = csv.DictReader(csvfile1)
        stock = []
        for row in reader:
            #Check
            if row["stockSymbol"]:
                stock.append(row["stockSymbol"])
        print(stock)
        aa = ['Q1', 'Q2', 'Q3', 'Q4', 'FY']
        for i in stock:
            for n in range(start, endd):
                for ss in aa:
                    print(str(n) + str(ss))

                    termresults = db.TermResults.find({"stockSymbol": i})
                    for result in termresults:
                        awe = str(result["FY"]) + str(result["FQ"])
                        if awe == str(n) + str(ss):
                            ent = "'" + result["entityId"]
                            datarow = {"termId": result["termId"], "entityId": ent, "FYFQ": awe, "stockSymbol": result["stockSymbol"], "value": result["value"]}
                            try:
                                if abs(result["changePcntPoP"]) >= maximum:
                                    datarow.update({"ChangePcntPoP": result["changePcntPoP"], 'ChangePcntPoPExp': result["changePcntPoPExp"]})
                                    writer.writerow(datarow)
                            except KeyError:
                                error = " No ChangePcntPoP"
