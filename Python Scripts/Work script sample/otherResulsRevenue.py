import config
import csv
import time
db = config.db
timestr = time.strftime("%Y%m%d-%H%M%S")
filename = "otherResultsRevenue" + timestr + ".csv"
count = 0
with open(filename, 'w') as csvfile:
    fieldnames = ['termName', 'entityId','FY','FQ','value', 'Description','Expression', 'otherExpression']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',', lineterminator='\n')
    writer.writeheader()
    termRulescollection = db.TermRules.find({"name": {"$regex": "Revenue"}})
    for termRule in termRulescollection:
        termResultsCollection = db.TermResults.find({"otherTermResults": {"$exists": "true"}, "termId": termRule["termId"]})
        for termResult in termResultsCollection:
                found = False
                xyz = " "
                des = 'The main value is ' + str(termResult["value"]) + ' and the other value are '
                for otherResults in termResult['otherTermResults']:
                    if termResult["value"] < otherResults["value"]:
                        found = True
                        des = des + ' ' + str(otherResults["value"])
                        xyz = str(otherResults["expression"])
                if found:
                    ent = "'" + termResult["entityId"]
                    writer.writerow({'termName': termResult["termName"], 'entityId': ent, 'FY': termResult["FY"], 'FQ': termResult["FQ"], 'value': termResult["value"], 'Description': des, 'Expression': termResult["expression"],'otherExpression': xyz})
print("Completed Program Successfully")


