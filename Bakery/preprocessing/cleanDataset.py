import pandas as pd
import csv

route = "../datasets/"

def DateAndTimetoDateTime(df):
    """
    Concats Date and Time columns into DateTime
    """
    df["DateTime"] = df["Date"] + " " + df["Time"]
    return df.drop(columns=["Date","Time"])

def saveAsCsv(df, fileName): 
    df.to_csv(route + fileName,index=False)

df = pd.read_csv("../datasets/BreadBasket_DMS.csv")
df = DateAndTimetoDateTime(df)
saveAsCsv(df,"BreadBasket_DMS_DT.csv")