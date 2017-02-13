import pandas as pd


df= pd.read_csv("outputTermResults_PLS_TotalDebt 20170127-093725.csv")
#custom sort using ranking
custom_dict = {'Q1':0, 'Q2':1, 'Q3':2,'Q4':3, 'FY':4}
df['rank'] = df['FQ'].map(custom_dict)

df.sort(columns=['stockSymbol','termName','FY','rank'],inplace=True)
#dropping un-necessary columns
df.drop("rank", axis=1, inplace=True)
df["FYFQ"]=df["FY"].map(str) + df["FQ"]
df.drop("FY", axis=1, inplace=True)
df.drop("FQ", axis=1, inplace=True)
df.drop("expression", axis=1, inplace=True)
df.drop("elementName", axis=1, inplace=True)
#print(df)
#pivot FYFQ to individual columns
table = pd.pivot_table(df,values='value', index=['termId','entityId','stockSymbol','termName'], columns='FYFQ')
print(table)
table.to_csv("pivot_issue13.csv", index=True)

#sorting after pivoting with index false
sortedtable=pd.read_csv("pivot_issue13.csv")
sortedtable.sort(columns=['stockSymbol','termName'],inplace=True)
sortedtable.to_csv("pivot_sorted_issue13.csv", index=False)

