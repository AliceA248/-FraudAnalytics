import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('spreadsheet/transactional-sample.csv', delimiter=';')
total_transactions = len(df)
print("Total transactions:", total_transactions)

# Convert values in the 'has_cbk' column to lowercase if needed
if df['has_cbk'].dtype == bool:
    df['has_cbk'] = df['has_cbk'].astype(str).str.lower()

# Count transactions with and without chargeback
chargeback_counts = df['has_cbk'].value_counts()
print("Count of transactions with and without chargeback:")
print(chargeback_counts.to_string())
if 'true' in chargeback_counts.index:
    total_chargeback = chargeback_counts.get('true', 0)
    chargeback_percent = (total_chargeback / total_transactions) * 100
    print("Percentage of transactions with chargeback:", chargeback_percent)

# Visualize the results
if 'true' in chargeback_counts.index:
    plt.figure(figsize=(6, 6))
    plt.pie(chargeback_counts, labels=chargeback_counts.index, autopct='%1.1f%%', colors=['skyblue', 'lightgreen'])
    plt.title('Percentage of transactions with chargeback')
    plt.show()

# Calculate the mean transaction amount
mean_transaction_amount = round(df['transaction_amount'].mean(), 2)
print("Mean transaction amount:", mean_transaction_amount)

# Identify high-value transactions and transactions with chargeback among them
high_value_limit = 1.5 * mean_transaction_amount
high_value_transactions = df[df['transaction_amount'] > high_value_limit]
high_value_chargebacks = high_value_transactions[high_value_transactions['has_cbk'] == 'true']
print("High-value transactions:", len(high_value_transactions))
print("High-value transactions with chargeback:", len(high_value_chargebacks))

# Analyze the distribution of chargebacks per user
user_chargebacks = df[df['has_cbk'] == 'true'].groupby('user_id').size()
print("Users with multiple chargebacks:", len(user_chargebacks))
plt.hist(user_chargebacks, bins=range(1, user_chargebacks.max() + 1), color='skyblue', edgecolor='black')
plt.title('Distribution of chargebacks per user')
plt.xlabel('Number of chargebacks')
plt.ylabel('User count')
plt.show()
