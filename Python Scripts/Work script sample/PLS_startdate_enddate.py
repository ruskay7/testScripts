import config
import csv
import time
import sys
db = config.db
count = 0
timestr = time.strftime(" %Y%m%d-%H%M%S")
starting = int(sys.argv[1]) #argument for starting year
ending = int(sys.argv[2])   #argument for ending year
ending_for_range = ending + 1
ID = sys.argv[3]    #enter argument for _id
getid = db.PartnerAccess.find({'_id': ID})
for document in getid:
    for term in document["terms"]:
        filename = term["termName"] + timestr + ".csv"
        fieldnames = ['termId', 'entityId', 'companyName','PcntgCountofZero','No_of_Filings', 'stockSymbol']
        with open(filename, 'w') as csvfile:
            for n in range(starting, ending_for_range):
                fieldnames.extend([str(n) + 'Q1', str(n) + 'Q2', str(n) + 'Q3', str(n) + 'Q4', str(n) + "FY"])
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',', lineterminator='\n')
            writer.writeheader()
            for entity in document["entities"]:
                ent = "'" + entity["entityId"]
                datarow = ({"termId": term["termId"], "entityId": ent, "companyName": entity["companyName"]})
                termresults = db.TermResults.find({"termId": term["termId"], "entityId": entity["entityId"], "FY": {"$gte": starting, "$lte": ending}})
                noofzerocount = 0
                full = []
                for result in termresults:
                    full.append(result["value"])
                    concatenatedFYFQ = str(result["FY"]) + str(result["FQ"])
                    datarow.update({concatenatedFYFQ: result["value"], 'stockSymbol': result["stockSymbol"]})
                    if abs(result["value"]) == 0:
                        noofzerocount += 1
                datarow.update({'No_of_Filings': len(full)})
                if len(full)!=0:
                    PcntgCountofZero = noofzerocount / len(full)
                    print(PcntgCountofZero)
                    datarow.update({"PcntgCountofZero": PcntgCountofZero})
                writer.writerow(datarow)

