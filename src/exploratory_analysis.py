#EXPLORATORY ANALYSIS

import pandas as pd
import matplotlib.pyplot as plt #ploting graph
import seaborn as sns #styling graph
from datetime import datetime
from statsmodels.tsa.holtwinters import SimpleExpSmoothing
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error
import numpy as np

monthly_sales = Amazon.groupby(['Year','Month'])['Total amount'].sum()
monthly_sales.plot(kind='line')
plt.title("Monthly Sales Trend")
plt.show()

print("\nYEARLY SALES")
yearly_sales = Amazon.groupby('Year')['Total amount'].sum()
print(yearly_sales)

best_month = monthly_sales.idxmax()
worst_month = monthly_sales.idxmin()

print("Best Month:", best_month)
print("Worst Month:", worst_month)

#GROUPING OF DATA  SET

print("\nProductNames and their TotalQuantity\n")
print(Amazon.groupby("ProductName")["Quantity"].sum())
print("\nProductNames and their NetRevenue\n")
print(Amazon.groupby("ProductName")["Total amount"].sum())
print("\nCategoryNames and their NetRevenue\n")
print(Amazon.groupby("Category")["Total amount"].sum())

#TOP PRODUCTS BY QUANTITY
product_summary=Amazon.groupby("ProductName").agg({"Quantity":"sum","Total amount":"sum"}).reset_index()
top_by_Quantity=product_summary.sort_values(by="Quantity",ascending=False)
print("\nTOP PRODUCTS BY QUANTITY\n")
print("\n",top_by_Quantity)

#TOP PRODUCTS BY REVENUE
top_by_Revenue=product_summary.sort_values(by="Total amount",ascending=False)
print("\nTOP PRODUCTS BY REVENUE\n")
print("\n",top_by_Revenue)

print("\nTOP 5 PRODUCTS\n")
top5=top_by_Revenue.head(5)
print(top5)


#SEASONAL ANALYSIS
Amazon["Month"]=Amazon["OrderDate"].dt.month
monthly_sales=Amazon.groupby(["Month","ProductName"])["Quantity"].sum().reset_index()
print("\nSEASONAL ANALYSIS\n")
print(monthly_sales)

category_summary=Amazon.groupby("Category").agg({"Quantity":"sum","Total amount":"sum"}).reset_index()
print("\nCATEGORY SUMMARY\n",category_summary)