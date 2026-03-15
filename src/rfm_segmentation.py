#Convert OrderDate to datetime
Amazon['OrderDate'] = pd.to_datetime(Amazon['OrderDate'])

#Create Reference Date
reference_date = Amazon['OrderDate'].max() + pd.Timedelta(days=1)

# Create RFM Table
rfm = Amazon.groupby('CustomerID').agg({
    'OrderDate': lambda x: (reference_date - x.max()).days,
    'CustomerID': 'count',
    'Total amount': 'sum'
})

rfm.columns = ['Recency', 'Frequency', 'Monetary']
rfm.reset_index(inplace=True)

#Create RFM Scores using Rank + qcut (SAFE METHOD)
rfm['R_Score'] = pd.qcut(
    rfm['Recency'].rank(method='first'),
    5,
    labels=[5,4,3,2,1]
).astype(int)

rfm['F_Score'] = pd.qcut(
    rfm['Frequency'].rank(method='first'),
    5,
    labels=[1,2,3,4,5]
).astype(int)

rfm['M_Score'] = pd.qcut(
    rfm['Monetary'].rank(method='first'),
    5,
    labels=[1,2,3,4,5]
).astype(int)


# 5️⃣ Combine RFM Score
rfm['RFM_Score'] = (
    rfm['R_Score'].astype(str) +
    rfm['F_Score'].astype(str) +
    rfm['M_Score'].astype(str)
)

# 6️⃣ Customer Segmentation
def segment(row):
    if row['R_Score'] == 5 and row['F_Score'] >= 4:
        return "High Value"
    elif row['R_Score'] >= 4 and row['F_Score'] >= 3:
        return "Potential Loyalist"
    elif row['R_Score'] <= 2 and row['F_Score'] >= 3:
        return "At Risk"
    else:
        return "Others"

rfm['Segment'] = rfm.apply(segment, axis=1)

print(rfm.head())
print("\nSegment Distribution:")
print(rfm['Segment'].value_counts())

#segment summary
segment_summary = rfm.groupby('Segment').agg({
    'CustomerID': 'count',
    'Monetary': 'sum'
})

print(segment_summary)


# ===============================
# TODAY'S WORK – FINAL CONTINUATION (ERROR SAFE)
# ===============================

# 1. Detailed Segment Analysis
segment_analysis = rfm.groupby('Segment').agg({
    'Recency': 'mean',
    'Frequency': 'mean',
    'Monetary': 'mean',
    'CustomerID': 'count'
}).rename(columns={'CustomerID': 'Customer_Count'})

print("\nDetailed Segment Analysis:")
print(segment_analysis)


# 2. Customer Lifetime Value (CLV)
rfm['CLV'] = rfm['Frequency'] * rfm['Monetary']

print("\nAverage CLV per Segment:")
print(rfm.groupby('Segment')['CLV'].mean())

# 3. Bar Chart – Segment Distribution
import matplotlib.pyplot as plt

plt.figure()
rfm['Segment'].value_counts().plot(kind='bar')
plt.title("Customer Distribution by Segment")
plt.xlabel("Segment")
plt.ylabel("Number of Customers")
plt.show()


# 4. Pie Chart – Segment Share
plt.figure()
rfm['Segment'].value_counts().plot(kind='pie', autopct='%1.1f%%')
plt.title("Customer Segment Share")
plt.ylabel('')
plt.show()

# 5. Heatmap – R_Score vs F_Score (Monetary Mean)
import seaborn as sns

pivot = rfm.pivot_table(
    index='R_Score',
    columns='F_Score',
    values='Monetary',
    aggfunc='mean'
)

plt.figure()
sns.heatmap(pivot, annot=True)
plt.title("Heatmap of Monetary (R_Score vs F_Score)")
plt.show()


# 6. Marketing Recommendations
print("\nMARKETING RECOMMENDATIONS:\n")

recommendations = {
    "High Value": "Offer loyalty programs, VIP benefits, exclusive discounts.",
    "Potential Loyalist": "Encourage repeat purchases with personalized offers.",
    "At Risk": "Send re-engagement emails and limited-time discounts.",
    "Others": "Send general promotional campaigns."
}

for segment, message in recommendations.items():
    print(f"{segment}: {message}")


# 7. Final Key Insights
print("\nKEY INSIGHTS SUMMARY\n")

print("Total Customers:", rfm.shape[0])

print("\nCustomer Distribution:")
print(rfm['Segment'].value_counts())

print("\nRevenue by Segment:")
print(rfm.groupby('Segment')['Monetary'].sum().sort_values(ascending=False))



# Scatter / Bubble plot for RFM
plt.figure(figsize=(8,6))

plt.scatter(
    rfm['Recency'], 
    rfm['Frequency'], 
    s=rfm['Monetary'],      # bubble size based on Monetary value
    alpha=0.6
)

plt.title("RFM Scatter Plot (Recency vs Frequency with Monetary Bubble Size)")
plt.xlabel("Recency")
plt.ylabel("Frequency")

plt.show()

print("\nKEY INSIGHTS SUMMARY\n")
rfm.to_csv("customer_segmentation_rfm.csv", index=False)
