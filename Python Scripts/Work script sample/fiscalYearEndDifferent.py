import config
import csv
import time
db = config.db
timestr = time.strftime("%Y%m%d-%H%M%S")
filename = "fiscalYearEnd_Different" + timestr + ".csv"
with open(filename, 'w') as csvfile:
    fieldnames = ['_id', 'entityId', 'stockSymbol', 'fiscalYearEnd1','fiscalYearEnd2']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',', lineterminator='\n')
    writer.writeheader()
    entitycollection = db.EntityReferences.find()
    countbadentity = 0
    for entity in entitycollection:
        SECFiling = db.SECFilings.find({"entityId": entity["entityId"]})
        x = None
        knownfe=dict()
        badentity = False
        for document in SECFiling:
            a = document["fiscalYearEnd"]
            if a in knownfe:
                continue
            
            if x!= None:
                if a != x:
                    badentity = True
                    ent = "'" + document["entityId"]
                    writer.writerow({'_id': document["_id"], 'entityId': ent, 'stockSymbol': document["stockSymbol"], 'fiscalYearEnd1': x,'fiscalYearEnd2': a})
            else:
                 x = a
            knownfe[a] = True
                 
        if badentity == True:
            countbadentity = countbadentity + 1
            print(countbadentity)

print(countbadentity)
print("Completed Program Successfully")
