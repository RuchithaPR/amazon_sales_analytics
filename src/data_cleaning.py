#Step 1 — Import pandas
import pandas as pd
import matplotlib.pyplot as plt #ploting graph
import seaborn as sns #styling graph
from datetime import datetime
from statsmodels.tsa.holtwinters import SimpleExpSmoothing
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error
import numpy as np

# Step 2 — Load the dataset
Amazon = pd.read_csv(r"C:/Users/Ruchitha PR/OneDrive/Desktop/Statistics/Amazon.csv")

# Step 3 — Explore the dataset
print("First 5 rows:\n")
print(Amazon.head())

print("\nShape (rows, columns):")
print(Amazon.shape)

print("\nColumn names:")
print(Amazon.columns)

print("\nData types:")
print(Amazon.dtypes)

# Step 4 — Check Missing Values
print("\nMissing values in each column:\n")
print(Amazon.isnull().sum())

# Show rows with missing values (optional)
missing_rows = Amazon[Amazon.isnull().any(axis=1)]
print("\nRows with missing values:")
print(missing_rows)

# Handle Missing Values (choose one method)

# Method 1: Remove rows with missing values
Amazon = Amazon.dropna()

# Method 2 (optional instead): Fill missing with 0
Amazon = Amazon.fillna(0)

# Step 5 — Check Duplicates
print("\nNumber of duplicate rows:")
print(Amazon.duplicated().sum())

# Show duplicate rows (optional)
duplicates = Amazon[Amazon.duplicated()]
print("\nDuplicate rows:")
print(duplicates)

# Remove duplicates
Amazon = Amazon.drop_duplicates()

# Step 6 — Fix Date Format (if OrderDate column exists)
if 'OrderDate' in Amazon.columns:
    Amazon['OrderDate'] = pd.to_datetime(Amazon['OrderDate'], errors='coerce')

# Check again for missing after date conversion
print("\nMissing values after cleaning:\n")
print(Amazon.isnull().sum())

#adding extra columns
Amazon['OrderDate'] = pd.to_datetime(Amazon['OrderDate'])

Amazon['Year'] = Amazon['OrderDate'].dt.year
Amazon['Month'] = Amazon['OrderDate'].dt.month


print("\nColumn names:")
print(Amazon.columns)

# Step 7 — Final Clean Data Info
print("\nFinal dataset shape:")
print(Amazon.shape)

print("\nFinal duplicate count:")
print(Amazon.duplicated().sum())

# Step 8 — Save Cleaned Dataset
Amazon.to_csv("Cleaned_Amazon.csv", index=False)

print("\n✅ Data Cleaning Completed. Cleaned file saved as 'Cleaned_Amazon.csv'")

