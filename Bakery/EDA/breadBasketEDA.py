import pandas as pd
import plotly.express as px
from mlxtend.preprocessing import TransactionEncoder

#Load data
df = pd.read_csv("../datasets/BreadBasket_DMS_DT.csv", sep = ";")

#Explore structure and values of our dataset
df.describe(include="all")
df.info()

print(df.head(10))
print(df.tail(10))

uniqueItems = df["Item"].unique()
print("There are " + str(len(uniqueItems)) + " unique items:")
print(uniqueItems)

#Drop Null/None values. We drop columns with "NONE" value as we have seen in the uniqueItems list
df = df[df.Item != "NONE"]

#Getting the 10 most common objects and labelling the rest as "Others"
mostPopularItems = df.Item.value_counts()[:10]
otherItemsCount = df.Item.count() - mostPopularItems.sum()
itemList = mostPopularItems.append(pd.Series([otherItemsCount], index = ["Others"]))
print(itemList)
fig = px.pie(itemList, values=0, names=itemList.index, title="Most Popular Items on our Bakery")
fig.show()

#Sales by Month (Chronological order)
df["DateTime"] = pd.to_datetime(df["DateTime"], utc=True)
monthsCount = df.DateTime.dt.month_name().unique()
fig = px.histogram(df, x = "DateTime", nbins = len(monthsCount), title = "Sales per month in chronological order")
fig.update_layout(bargap=0.2)
fig.show()
#Sales by Month
countByMonth = df.groupby(df.DateTime.dt.month_name())['Item'].count().sort_values(ascending=False)
fig = px.bar(countByMonth, title = "Most Productive Month")
fig.show()
#Sales by Day
countByDay = df.groupby(df.DateTime.dt.day_name())['Item'].count().sort_values(ascending=False)
fig = px.bar(countByDay, title = "Most Productive Day")
fig.show()
#Sales by Hour
countbyHour = pd.DataFrame({"Time":range(1, 25)})
countbyHour["Count"] = df.groupby(df.DateTime.dt.hour.sort_values(ascending=True))["Item"].count()
countbyHour["Count"] = countbyHour["Count"].fillna(0)
fig = px.bar(countbyHour, x = "Time", y = "Count", title = "Sales per Hour of the Day")
fig.show()
#Sales by Session (Morning, Afternoon, Evening)
hours = [0,12,18,24]
sessions = ["Morning","Afternoon","Evening"]
countbyHour["Session"] = pd.cut(countbyHour["Time"], bins=hours, labels=sessions, include_lowest=True)
countbyHour = countbyHour.groupby(countbyHour.Session)["Count"].sum().reset_index()
fig = px.pie(countbyHour, names = "Session", values = "Count", title = "Peak Selling Hours")
fig.show()

#Association Rules
#Transaction List
transactions=[]
for item in df['Transaction'].unique():
    itemList = list(set(df[df['Transaction']==item]['Item']))
    transactions.append(itemList)
#Use Transaction Encoder to go from Transaction List to boolean array
te = TransactionEncoder()
encodedData = te.fit(transactions).transform(transactions)
basketData = pd.DataFrame(encodedData, columns=te.columns_)
basketData