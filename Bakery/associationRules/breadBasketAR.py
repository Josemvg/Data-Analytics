import pandas as pd
from mlxtend.preprocessing import TransactionEncoder

df = pd.read_csv("../datasets/BreadBasket_DMS_DT.csv")

transactions=[]
for item in df['Transaction'].unique():
    itemList = list(set(df[df['Transaction']==item]['Item']))
    transactions.append(itemList)
te = TransactionEncoder()
encodedData = te.fit(transactions).transform(transactions)
basketData = pd.DataFrame(encodedData, columns=te.columns_)
basketData