
#Forecasting model

#moving average model
Amazon['Moving_Avg_3'] = Amazon['Total amount'].rolling(window=3).mean()

print(Amazon[['OrderDate','Total amount','Moving_Avg_3']].head())

#Exponential Smoothing


sales = Amazon.groupby('OrderDate')['Total amount'].sum()

model = SimpleExpSmoothing(sales)
fit_model = model.fit()

forecast = fit_model.forecast(10)

print(forecast)

#ARIMA model

sales = Amazon.groupby('OrderDate')['Total amount'].sum()

model = ARIMA(sales, order=(1,1,1))
model_fit = model.fit()

forecast = model_fit.forecast(steps=10)

print(forecast)

#Training and testing
sales = Amazon.groupby('OrderDate')['Total amount'].sum()

train_size = int(len(sales) * 0.8)

train = sales[:train_size]
test = sales[train_size:]

print("Training size:", len(train))
print("Testing size:", len(test))

#Train forecasting Model

model = ARIMA(train, order=(1,1,1))
model_fit = model.fit()

print(model_fit.summary())

#MAke Predictions
forecast = model_fit.forecast(steps=len(test))

print("Predicted Sales:")
print(forecast)

#make comparision with predictions


rmse = np.sqrt(mean_squared_error(test, forecast))

print("RMSE:", rmse)

#Visualize preictions

plt.figure(figsize=(10,5))

plt.plot(train.index, train, label="Training Data")
plt.plot(test.index, test, label="Actual Sales")
plt.plot(test.index, forecast, label="Predicted Sales")

plt.legend()
plt.title("Sales Forecast vs Actual")
plt.show()


#Generate Future Sales Predictions
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA

# Convert OrderDate
Amazon['OrderDate'] = pd.to_datetime(Amazon['OrderDate'], format='%d-%m-%Y')

# Create daily sales
sales = Amazon.groupby('OrderDate')['Total amount'].sum()

# Train ARIMA model
model = ARIMA(sales, order=(1,1,1))
model_fit = model.fit()

# Predict next 12 periods
future_forecast = model_fit.forecast(steps=12)

print("Future Sales Forecast:")
print(future_forecast)

#Visualize Forecasted Sales
plt.figure(figsize=(10,5))

plt.plot(sales.index, sales, label="Historical Sales")

future_dates = pd.date_range(start=sales.index.max(), periods=12)

plt.plot(future_dates, future_forecast, label="Predicted Sales")

plt.legend()
plt.title("Future Sales Forecast")
plt.xlabel("Date")
plt.ylabel("Sales")

plt.show()

#Valodate forecast accuracy
from sklearn.metrics import mean_squared_error

# Split dataset
train_size = int(len(sales) * 0.8)

train = sales[:train_size]
test = sales[train_size:]

# Train model
model = ARIMA(train, order=(1,1,1))
model_fit = model.fit()

# Predict
predictions = model_fit.forecast(steps=len(test))

# Calculate RMSE
rmse = np.sqrt(mean_squared_error(test, predictions))

print("RMSE:", rmse)


#CSV Forecast Dataset Code
future_dates = pd.date_range(start=sales.index.max(), periods=12)

forecast_df = pd.DataFrame({
    "Date": future_dates,
    "Predicted_Sales": future_forecast
})

forecast_df.to_csv("future_sales_forecast.csv", index=False)

print("Forecast dataset saved successfully.")

#Charts code for submission
plt.figure(figsize=(10,5))

plt.plot(sales.index, sales, label="Historical Sales")

future_dates = pd.date_range(start=sales.index.max(), periods=12)

plt.plot(future_dates, future_forecast, label="Predicted Sales")

plt.title("Historical vs Forecasted Sales")
plt.xlabel("Date")
plt.ylabel("Sales")

plt.legend()
plt.show()

#Bar Chart
monthly_sales = Amazon.groupby(Amazon['OrderDate'].dt.month)['Total amount'].sum()

monthly_sales.plot(kind='bar')

plt.title("Monthly Sales Distribution")
plt.xlabel("Month")
plt.ylabel("Total Sales")

#plt.show()

# Create future dates (next 12 periods)
future_dates = pd.date_range(start=sales.index.max(), periods=12)

# Create forecast dataset
forecast_df = pd.DataFrame({
    "Date": future_dates,
    "Predicted_Sales": future_forecast
})

# Save dataset as CSV
forecast_df.to_csv("future_sales_forecast.csv", index=False)

print("Forecast dataset saved successfully")


#high growth product categories
#category wise total sales
#Category wise total sales

category_sales = Amazon.groupby('Category')['Total amount'].sum().sort_values(ascending=False)

print("Top Selling Categories:")
print(category_sales)




category_sales.plot(kind='bar')

plt.title("Sales by Category")
plt.xlabel("Category")
plt.ylabel("Total Sales")
plt.show()

#identify regional sales growth 
city_sales = Amazon.groupby('City')['Total amount'].sum().sort_values(ascending=False)

print("Top Cities by Sales:")
print(city_sales.head(10))

#country wise sales
country_sales = Amazon.groupby('Country')['Total amount'].sum().sort_values(ascending=False)

print("Sales by Country:")
print(country_sales)

#undersstanding customer behaviour
customer_sales = Amazon.groupby('CustomerName')['Total amount'].sum().sort_values(ascending=False)

print("Top Customers:")
print(customer_sales.head(10))

#cross selling (Products Bought together)
from itertools import combinations
from collections import Counter

product_pairs = Amazon.groupby('OrderID')['ProductName'].apply(list)

pair_counter = Counter()

for products in product_pairs:
    pairs = combinations(products,2)
    pair_counter.update(pairs)

print("Most Common Product Pairs:")
print(pair_counter.most_common(10))

#pricing and promotion analysis
discount_sales = Amazon.groupby('Discount')['Total amount'].sum()

print("Sales based on Discount:")
print(discount_sales)

#customer retension (Recent customers)
# convert date first
Amazon['OrderDate'] = pd.to_datetime(Amazon['OrderDate'], dayfirst=True)

latest_date = Amazon['OrderDate'].max()

customer_recency = Amazon.groupby('CustomerID')['OrderDate'].max()

print("Customer Last Purchase Date:")
print(customer_recency.head())

#print bussiness oppurtunities insigts
print("\nBusiness Opportunities Identified:\n")

print("1. Increase inventory for top selling product categories.")
print("2. Focus marketing campaigns in top performing cities.")
print("3. Create bundle offers for commonly purchased products.")
print("4. Offer discounts to price sensitive customers.")
print("5. Introduce loyalty programs for frequent buyers.")

#Data visualization codes
#sales Trend (line chart)
import matplotlib.pyplot as plt
import pandas as pd

# Convert date
Amazon['OrderDate'] = pd.to_datetime(Amazon['OrderDate'], dayfirst=True)

# Monthly sales
monthly_sales = Amazon.groupby(Amazon['OrderDate'].dt.to_period('M'))['Total amount'].sum()

monthly_sales.plot(kind='line', marker='o')

plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Total Sales")
plt.show()

#top product categories (bar chart)
category_sales = Amazon.groupby('Category')['Total amount'].sum().sort_values(ascending=False)

category_sales.plot(kind='bar')

plt.title("Sales by Product Category")
plt.xlabel("Category")
plt.ylabel("Total Sales")
plt.show()

#regional sales (city analysis)
city_sales = Amazon.groupby('City')['Total amount'].sum().sort_values(ascending=False)

city_sales.head(10).plot(kind='bar')

plt.title("Top 10 Cities by Sales")
plt.xlabel("City")
plt.ylabel("Total Sales")
plt.show()

#payment method analysis
payment_sales = Amazon.groupby('PaymentMethod')['Total amount'].sum()

payment_sales.plot(kind='bar')

plt.title("Sales by Payment Method")
plt.xlabel("Payment Method")
plt.ylabel("Total Sales")
plt.show()

#customer purchase behaviour
customer_sales = Amazon.groupby('CustomerName')['Total amount'].sum().sort_values(ascending=False)

customer_sales.head(10).plot(kind='bar')

plt.title("Top 10 Customers by Spending")
plt.xlabel("Customer")
plt.ylabel("Total Spending")
plt.show()

#Auto bussiness insights code
print("\nKEY BUSINESS INSIGHTS\n")

print("1. Some product categories generate the highest revenue and represent major business opportunities.")

print("2. Certain cities contribute more to total sales, indicating strong regional demand.")

print("3. A small group of customers contribute significantly to total revenue.")

print("4. Payment method preferences show how customers prefer to transact.")

print("5. Forecasting results indicate expected future sales patterns.")

#updated data set (csv)

import pandas as pd

# convert date
Amazon['OrderDate'] = pd.to_datetime(Amazon['OrderDate'], dayfirst=True)

# create extra columns
Amazon['Year'] = Amazon['OrderDate'].dt.year
Amazon['Month'] = Amazon['OrderDate'].dt.month
Amazon['Day'] = Amazon['OrderDate'].dt.day

# customer total spending
customer_total = Amazon.groupby('CustomerID')['Total amount'].sum().reset_index()
customer_total.columns = ['CustomerID','Customer_Total_Spending']

# merge with dataset
Amazon = Amazon.merge(customer_total, on='CustomerID', how='left')

# simple customer segmentation
Amazon['Customer_Segment'] = Amazon['Customer_Total_Spending'].apply(
    lambda x: 'High Value' if x > 500 else 'Medium Value' if x > 200 else 'Low Value'
)

# save updated dataset
Amazon.to_csv("updated_amazon_sales_dataset.csv", index=False)

print("Updated dataset saved successfully!")

#save visul charts
import matplotlib.pyplot as plt

monthly_sales = Amazon.groupby(Amazon['OrderDate'].dt.to_period('M'))['Total amount'].sum()

monthly_sales.plot(kind='line', marker='o')

plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Total Sales")

plt.savefig("sales_trend_chart.png")

plt.show()

category_sales = Amazon.groupby('Category')['Total amount'].sum()

category_sales.plot(kind='bar')

plt.title("Sales by Category")
plt.xlabel("Category")
plt.ylabel("Total Sales")

plt.savefig("category_sales_chart.png")

plt.show()

city_sales = Amazon.groupby('City')['Total amount'].sum().sort_values(ascending=False)

city_sales.head(10).plot(kind='bar')

plt.title("Top Cities by Sales")
plt.xlabel("City")
plt.ylabel("Total Sales")

plt.savefig("city_sales_chart.png")

plt.show()