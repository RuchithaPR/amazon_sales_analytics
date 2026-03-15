#VISUALISATION
#BAR CHART OF REVENUE BY CATEGORY
plt.bar(category_summary['Category'], category_summary['Total amount'])
plt.xlabel('Category')
plt.ylabel('Total amount')
plt.title('Revenue by Category')
plt.show()

#PIE CHART OF SALES DISTRIBUTION
plt.pie(category_summary['Quantity'], labels=category_summary['Category'], autopct='%1.1f%%')
plt.title('Sales Distribution by Category')
plt.show()

#COMPARING PROFITABILITY OF BEST SELLERS
Amazon['Cost'] = [30, 10, 500, 20, 200,400,200,1600,500]  # Example costs
Amazon['Profit'] = Amazon['Total amount'] - Amazon['Cost']

# Find products with high sales AND good profit
profitable_products = Amazon[(Amazon['Quantity'] > 2) & (Amazon['Profit'] > 100)]

print("\nPROFITABLE PRODUCTS\n")
print(profitable_products)

print(Amazon.columns)
sales_by_city = Amazon.groupby('City')['Quantity'].sum().sort_values(ascending=False)

print("\nSALES BY CITY\n",sales_by_city)
print("\ntop 5 cities with more sales\n",sales_by_city.head())

print("\nsales by city and category\n")
print(Amazon.groupby(['City','Category'])['Quantity'].sum())

print("\nREPEAT CUSTOMERS\n")
print(Amazon.groupby('City')['CustomerID'].nunique())

#Bar graph

sales_by_city.plot(kind='bar', figsize=(10,5))
plt.title('Bar chart of sales distribution')
plt.show()

#HEATMAP
pivot = Amazon.pivot_table(values='Quantity', index='City', aggfunc='sum')

sns.heatmap(pivot, cmap='coolwarm')
plt.title('Heat Map of sales distribution')
plt.show()

