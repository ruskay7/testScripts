import config
import csv
import time
db = config.db
count = 0
maximum = 0.30
timestr = time.strftime(" %Y%m%d-%H%M%S")
PartnerAccess = {'_id':'PLS'}
getid = db.PartnerAccess.find(PartnerAccess)
for document in getid:
    print(document)
    for term in document["terms"]:
        print(term["termId"])
        #csv header
        filename = term["termName"] + timestr + ".csv"
        with open(filename, 'w') as csvfile:
            fieldnames = ['termId', 'entityId', 'FY', 'FQ', 'stockSymbol', 'value', 'ChangePcntYoY', 'ChangePcntYoYExp' ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',', lineterminator='\n')
            writer.writeheader()
            for entity in document["entities"]:
                count = count + 1
                print(entity["entityId"])
                print(count)
                termresults = db.TermResults.find({"termId":term["termId"], "entityId": entity["entityId"]})
                for result in termresults:
                    datarow = {"termId":result["termId"], "entityId": result["entityId"],"FY": result["FY"], "FQ": result["FQ"], "stockSymbol": result["stockSymbol"], "value": result["value"]}
                    try:
                        if abs(result["changePcntYoY"]) >= maximum:
                            datarow.update({"ChangePcntYoY": result["changePcntYoY"], 'ChangePcntYoYExp': result["changePcntYoYExp"]})
                            writer.writerow(datarow)
                    except KeyError:
                        error = " No ChangePcntYoY"
                        pass
