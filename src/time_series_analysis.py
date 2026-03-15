#TIME SERIES DATA

#Convert OrderDate to datetime
Amazon['OrderDate'] = pd.to_datetime(Amazon['OrderDate'], format='%d-%m-%Y')

# Extract date components
Amazon['Year'] = Amazon['OrderDate'].dt.year
Amazon['Month'] = Amazon['OrderDate'].dt.month
Amazon['Day'] = Amazon['OrderDate'].dt.day
Amazon['Week'] = Amazon['OrderDate'].dt.isocalendar().week

print("\n",Amazon[['OrderDate','Year','Month','Day','Week']].head())

# Calculate total sales per day

daily_sales = Amazon.groupby('OrderDate')['Total amount'].sum().reset_index()

print("\n",daily_sales.head())

# Set OrderDate as index
daily_sales.set_index('OrderDate', inplace=True)

# Create full date range
all_dates = pd.date_range(start=daily_sales.index.min(),
                          end=daily_sales.index.max())

# Reindex dataset
daily_sales = daily_sales.reindex(all_dates)

# Fill missing sales with 0
daily_sales['Total amount'] = daily_sales['Total amount'].fillna(0)

print(daily_sales.head())


#ploting

plt.figure(figsize=(10,5))
plt.plot(daily_sales.index, daily_sales['Total amount'])
plt.title("Sales Trend Over Time")
plt.xlabel("Date")
plt.ylabel("Total Sales")
plt.show()

# Sort dataset by date
daily_sales = daily_sales.sort_index()

# Ensure index is datetime
daily_sales.index = pd.to_datetime(daily_sales.index)

print(daily_sales.head())

daily_sales.to_csv("processed_time_series_sales.csv")

print("\nDataset saved successfully!")
