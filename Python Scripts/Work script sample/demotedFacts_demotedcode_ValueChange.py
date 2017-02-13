import config
import csv
import time
import os
db = config.db
import pandas
timestr = time.strftime("%Y%m%d-%H%M%S")
filename1 = "demotedfactsSheet1_"+".csv"
filename2= "demotedFactsSheet2_" + ".csv"
count = 0
with open(filename1, 'w') as csvfile:       #sheet 1 containing demotedFacts
    fieldnames = ['FQ','FY','cik','demotedFilingDate','demotedValues', 'elementName','entityId','filingDate','stockSymbol','value']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',', lineterminator='\n')
    writer.writeheader()
    with open(filename2, 'w') as csvfile1:  #sheet 2 containing time series of demoted Facts
        fieldnames1 = ['FQ', 'FY', 'cik', 'elementName', 'entityId', 'filingDate', 'stockSymbol', 'value']
        writer1 = csv.DictWriter(csvfile1, fieldnames=fieldnames1, delimiter=',', lineterminator='\n')
        writer1.writeheader()
        SECFacts = db.SECNormalizedFacts.find({"demotedFacts.demoteCode": "ValueChange"})    #retrieving rows which has demotedfacts.demoted code as ValueChange
        for facts in SECFacts:
            dfvalue=[]  #demotedfactsvalue
            fdate =[]  #filingDate
            for demoted in facts["demotedFacts"]:
                dfvalue.append((demoted["value"]))
                fdate.append((demoted["filingDate"]))
            ent = "'" + facts["entityId"]
            datarow1= {'entityId': ent, 'cik': facts["cik"], 'stockSymbol': facts["stockSymbol"], 'FY': facts["FY"], 'FQ': facts["FQ"], 'value': facts["value"], 'elementName': facts["elementName"], 'filingDate':facts["filingDate"], 'demotedValues': dfvalue, 'demotedFilingDate': fdate}
            datarow2 = {'entityId': ent, 'cik': facts["cik"], 'stockSymbol': facts["stockSymbol"], 'FY': facts["FY"], 'FQ': facts["FQ"], 'value': facts["value"], 'elementName': facts["elementName"], 'filingDate':facts["filingDate"]}
            writer.writerow(datarow1)
            writer1.writerow(datarow2)
            count+=1
            print(count)
io1 = pandas.read_csv('demotedfactsSheet1_.csv')
io2 = pandas.read_csv('demotedFactsSheet2_.csv')
io1.sort_values(['stockSymbol','elementName','FY','FQ'],inplace = True) #sorting using pandas
io2.sort_values(['stockSymbol','elementName','FY','FQ'],inplace = True)
io1.to_csv('DemotedFactsSheet1.csv', index=False)
io2.to_csv('DemotedFactsSheet2.csv', index=False)
os.remove("demotedfactsSheet1_"+".csv") #remove unsorted and old csvs
os.remove("demotedfactsSheet2_"+".csv")
print("Completed Program Successfully")