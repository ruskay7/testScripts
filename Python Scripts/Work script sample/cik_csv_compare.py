import config
import csv
import time
timestr = time.strftime(" %Y%m%d-%H%M%S")
db = config.db
originalcount = 0
duplicatecount =0
differencecount =0
original = []
duplicate = []
with open('originalformattedfile1.csv', 'r') as csvfile1: #check formatting , add leading zeros to cik and entityId before running script
    reader1 = csv.DictReader(csvfile1)
    for orig in reader1:
        original.append((orig["stockSymbol"], orig["cik"], orig["companyName"], orig["entityId"], orig["sector"], orig["sic"], orig["sicCode"], orig["state"],orig["altCik"]))
with open('EntityReferencesCorrect_QAformatted.csv', 'r') as csvfile2:
    reader2 = csv.DictReader(csvfile2)
    for dup in reader2:
        duplicate.append((dup["stockSymbol"], dup["cik"], dup["companyName"], dup["entityId"], dup["sector"], dup["sic"], dup["sicCode"], dup["state"], dup["altCik"]))
for item1 in duplicate:
    duplicatecount+=1
for item2 in original:
    originalcount+=1
filename1 = "altCik_difference_CSV" + "output_files_changed" + timestr + ".csv"
with open(filename1, 'w') as csvfile1:
    fieldnames = ["stockSymbol","cik","companyName","entityId","sector","sic","sicCode","state","altCik"]
    writer = csv.DictWriter(csvfile1, fieldnames=fieldnames, delimiter=',', lineterminator='\n')
    writer.writeheader()
    changed_items = list(set(original)-set(duplicate))# difference between Original and duplicate(prints rows which are present in original but missing in duplicate)
    for rows in changed_items:
        datarow = {"stockSymbol": rows[0], "cik": rows[1], "companyName": rows[2], "entityId": rows[3],"sector": rows[4], "sic": rows[5], "sicCode": rows[6],"state": rows[7], "altCik": rows[8]}
        writer.writerow(datarow)
        differencecount+=1
print(originalcount)
print(duplicatecount)
print(differencecount)