import pandas as pd
import matplotlib.pyplot as plt

# Load the data
df = pd.read_csv('spreadsheet/transactional-sample.csv', delimiter=';')

# Total number of transactions
total_transactions = len(df)
print("Total transactions:", total_transactions)

# Convert values in the 'has_cbk' column to lowercase, if necessary
if df['has_cbk'].dtype == bool:
    df['has_cbk'] = df['has_cbk'].astype(str).str.lower()

# Count transactions with and without chargeback
chargeback_counts = df['has_cbk'].value_counts()
print("Transaction count with and without chargeback:")
print(chargeback_counts.to_string())

# Calculate the percentage of transactions with chargeback
if 'true' in chargeback_counts.index:
    total_chargeback = chargeback_counts.get('true', 0)
    chargeback_percent = (total_chargeback / total_transactions * 100) * 100
    print("Percentage of transactions with chargeback:", chargeback_percent)

    # Visualize the results
    plt.figure(figsize=(6, 6))
    plt.pie(chargeback_counts, labels=chargeback_counts.index, autopct='%1.1f%%', colors=['skyblue', 'lightgreen'])
    plt.title('Percentage of transactions with chargeback')
    plt.show()

# Calculate the average transaction amount
mean_transaction_amount = round(df['transaction_amount'].mean(), 2)
print("Average transaction amount:", mean_transaction_amount)

# Identify high-value transactions and transactions with chargeback among them
high_value_limit = 2 * mean_transaction_amount
high_value_transactions = df[df['transaction_amount'] > high_value_limit]
high_value_chargebacks = high_value_transactions[high_value_transactions['has_cbk'] == 'true']
print("High-value transactions:", len(high_value_transactions))
print("High-value transactions with chargeback:", len(high_value_chargebacks))

# Analyze the distribution of chargebacks per user
user_chargebacks = df[df['has_cbk'] == 'true'].groupby('user_id').size()
print("Users with multiple chargebacks:", len(user_chargebacks))
plt.hist(user_chargebacks, bins=range(1, user_chargebacks.max() + 2), color='skyblue', edgecolor='black')
plt.title('Distribution of chargebacks per user')
plt.xlabel('Number of chargebacks')
plt.ylabel('User count')
plt.show()

# Identify users with multiple cards and transactions with chargeback among them
user_cards = df.groupby('user_id')['card_number'].nunique()
multiple_cards_limit = 1
multiple_cards_users = user_cards[user_cards > multiple_cards_limit]
multiple_cards_transactions = df[df['user_id'].isin(multiple_cards_users.index)]
multiple_cards_chargebacks = multiple_cards_transactions[multiple_cards_transactions['has_cbk'] == 'true']

print("Users with multiple cards:", len(multiple_cards_users))
print("Transactions with multiple cards and chargeback:", len(multiple_cards_chargebacks))

# Visualize the percentage of chargebacks in transactions with multiple cards
chargeback_multiple_cards = len(multiple_cards_chargebacks)
no_chargeback_multiple_cards = len(multiple_cards_transactions) - chargeback_multiple_cards

plt.figure(figsize=(6, 6))
plt.pie([chargeback_multiple_cards, no_chargeback_multiple_cards], labels=['With Chargeback', 'Without Chargeback'], autopct='%1.1f%%', colors=['skyblue', 'lightgreen'])
plt.title('Percentage of Chargebacks in Transactions with Multiple Cards')
plt.show()

# Identify users with multiple devices and transactions with chargeback among them
user_devices = df.groupby('user_id')['device_id'].nunique()
multiple_devices_limit = 1
multiple_devices_users = user_devices[user_devices > multiple_devices_limit]
multiple_devices_transactions = df[df['user_id'].isin(multiple_devices_users.index)]
multiple_devices_chargebacks = multiple_devices_transactions[multiple_devices_transactions['has_cbk'] == 'true']

print("Users with multiple devices:", len(multiple_devices_users))
print("Transactions with multiple devices and chargeback:", len(multiple_devices_chargebacks))

# Visualize the percentage of chargebacks in transactions with multiple devices
chargeback_multiple_devices = len(multiple_devices_chargebacks)
no_chargeback_multiple_devices = len(multiple_devices_transactions) - chargeback_multiple_devices

plt.figure(figsize=(6, 6))
plt.pie([chargeback_multiple_devices, no_chargeback_multiple_devices], labels=['With Chargeback', 'Without Chargeback'], autopct='%1.1f%%', colors=['skyblue', 'lightgreen'])
plt.title('Percentage of Chargebacks in Transactions with Multiple Devices')
plt.show()
