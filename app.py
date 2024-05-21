import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet

# Load the data
df = pd.read_csv('spreadsheet/transactional-sample.csv', delimiter=';')

# Total number of transactions
total_transactions = len(df)
print(f"Total transactions: {total_transactions}")

# Convert values in the 'has_cbk' column to lowercase, if necessary
if df['has_cbk'].dtype == bool:
    df['has_cbk'] = df['has_cbk'].astype(str).str.lower()

# Count transactions with and without chargeback
chargeback_counts = df['has_cbk'].value_counts()
print("Chargeback counts:")
print(chargeback_counts)

# Calculate the percentage of transactions with chargeback
if 'true' in chargeback_counts.index:
    total_chargeback = chargeback_counts.get('true', 0)
    chargeback_percent = (total_chargeback / total_transactions * 100)
    print(f"Percentage of transactions with chargeback: {chargeback_percent:.2f}%")

# Calculate the average transaction amount
mean_transaction_amount = round(df['transaction_amount'].mean(), 2)
print(f"Average transaction amount: ${mean_transaction_amount:.2f}")

# Identify high-value transactions and transactions with chargeback among them
high_value_limit = 2 * mean_transaction_amount
high_value_transactions = df[df['transaction_amount'] > high_value_limit]
high_value_chargebacks = high_value_transactions[high_value_transactions['has_cbk'] == 'true']

# Analyze the distribution of chargebacks per user
user_chargebacks = df[df['has_cbk'] == 'true'].groupby('user_id').size()

# Identify users with multiple cards and transactions with chargeback among them
user_cards = df.groupby('user_id')['card_number'].nunique()
multiple_cards_limit = 1
multiple_cards_users = user_cards[user_cards > multiple_cards_limit]
multiple_cards_transactions = df[df['user_id'].isin(multiple_cards_users.index)]
multiple_cards_chargebacks = multiple_cards_transactions[multiple_cards_transactions['has_cbk'] == 'true']

# Identify users with multiple devices and transactions with chargeback among them
user_devices = df.groupby('user_id')['device_id'].nunique()
multiple_devices_limit = 1
multiple_devices_users = user_devices[user_devices > multiple_devices_limit]
multiple_devices_transactions = df[df['user_id'].isin(multiple_devices_users.index)]
multiple_devices_chargebacks = multiple_devices_transactions[multiple_devices_transactions['has_cbk'] == 'true']

# Calculate chargeback rate per device
device_chargeback_rate = df.groupby('device_id')['has_cbk'].apply(lambda x: (x == 'true').mean())

# Convert transaction_date to datetime format
df['transaction_date'] = pd.to_datetime(df['transaction_date'])

# Extract hour from transaction_date for chargeback transactions
chargeback_hours = df[df['has_cbk'] == 'true']['transaction_date'].dt.hour

# Print some intermediate results
print("\nHigh-value transactions:")
print(high_value_transactions.head())
print("\nUser chargebacks:")
print(user_chargebacks.head())
print("\nMultiple cards users:")
print(multiple_cards_users.head())
print("\nMultiple devices users:")
print(multiple_devices_users.head())
print("\nDevice chargeback rate:")
print(device_chargeback_rate.head())

# Create a PDF report
doc = SimpleDocTemplate("transaction_report.pdf", pagesize=letter)
styles = getSampleStyleSheet()
report = []

# Add title
report.append(Paragraph("Transaction Analysis Report", styles['Title']))
report.append(Spacer(1, 12))

# Add total transactions
report.append(Paragraph(f"Total transactions: {total_transactions}", styles['Normal']))
report.append(Spacer(1, 12))

# Add percentage of transactions with chargeback
if 'true' in chargeback_counts.index:
    report.append(Paragraph(f"Percentage of transactions with chargeback: {chargeback_percent:.2f}%", styles['Normal']))
    report.append(Spacer(1, 12))

# Add average transaction amount
report.append(Paragraph(f"Average transaction amount: ${mean_transaction_amount:.2f}", styles['Normal']))
report.append(Spacer(1, 12))

# Create and save chargebacks vs. non-chargebacks bar chart
plt.figure(figsize=(8, 6))
sns.set(style="whitegrid")
sns.barplot(x=chargeback_counts.index, y=chargeback_counts.values, palette=['lightgreen', 'skyblue'])
plt.title('Total Transactions: Chargebacks vs. Non-Chargebacks')
plt.xlabel('Chargeback Status')
plt.ylabel('Number of Transactions')
plt.tight_layout()
plt.savefig('chargebacks_vs_non_chargebacks.png')
plt.close()

# Add chargebacks vs. non-chargebacks bar chart to the report
report.append(Paragraph("Total Transactions: Chargebacks vs. Non-Chargebacks", styles['Heading2']))
report.append(Spacer(1, 12))
report.append(Image('chargebacks_vs_non_chargebacks.png', width=500, height=300))
report.append(Spacer(1, 12))

# Create and save chargebacks per user histogram
plt.figure(figsize=(8, 6))
sns.set(style="whitegrid")
sns.histplot(user_chargebacks, bins=range(1, user_chargebacks.max() + 2), color='skyblue', edgecolor='black', kde=True)
plt.title('Distribution of Chargebacks per User')
plt.xlabel('Number of Chargebacks')
plt.ylabel('User Count')
plt.tight_layout()
plt.savefig('chargebacks_per_user.png')
plt.close()

# Create and save chargebacks in transactions with multiple cards pie chart
plt.figure(figsize=(8, 6))
sns.set(style="whitegrid")
plt.pie([len(multiple_cards_chargebacks), len(multiple_cards_transactions) - len(multiple_cards_chargebacks)], 
        labels=['With Chargeback', 'Without Chargeback'], autopct='%1.1f%%', colors=['skyblue', 'lightgreen'], startangle=90)
plt.title('Percentage of Chargebacks in Transactions with Multiple Cards')
plt.axis('equal')
plt.tight_layout()
plt.savefig('chargebacks_multiple_cards.png')
plt.close()

# Create and save chargebacks in transactions with multiple devices pie chart
plt.figure(figsize=(8, 6))
sns.set(style="whitegrid")
plt.pie([len(multiple_devices_chargebacks), len(multiple_devices_transactions) - len(multiple_devices_chargebacks)], 
        labels=['With Chargeback', 'Without Chargeback'], autopct='%1.1f%%', colors=['skyblue', 'lightgreen'], startangle=90)
plt.title('Percentage of Chargebacks in Transactions with Multiple Devices')
plt.axis('equal')
plt.tight_layout()
plt.savefig('chargebacks_multiple_devices.png')
plt.close()

# Create and save chargeback rate per device histogram
plt.figure(figsize=(10, 6))
sns.histplot(device_chargeback_rate, bins=20, kde=True, color='skyblue', edgecolor='black')
plt.title('Distribution of Chargeback Rate per Device')
plt.xlabel('Chargeback Rate')
plt.ylabel('Device Count')
plt.tight_layout()
plt.savefig('chargeback_rate_per_device.png')
plt.close()

# Plot the distribution of chargeback hours
plt.figure(figsize=(10, 6))
sns.histplot(chargeback_hours, bins=24, kde=True, color='skyblue', edgecolor='black')
plt.title('Distribution of Chargeback Hours')
plt.xlabel('Hour of the Day')
plt.ylabel('Number of Chargebacks')
plt.xticks(range(24))
plt.tight_layout()
plt.savefig('chargeback_hours_distribution.png')
plt.close()

# Add images to the report
report.append(Paragraph("Distribution of Chargebacks per User", styles['Heading2']))
report.append(Spacer(1, 12))
report.append(Image('chargebacks_per_user.png', width=500, height=300))
report.append(Spacer(1, 12))

report.append(Paragraph("Percentage of Chargebacks in Transactions with Multiple Cards", styles['Heading2']))
report.append(Spacer(1, 12))
report.append(Image('chargebacks_multiple_cards.png', width=500, height=300))
report.append(Spacer(1, 12))

report.append(Paragraph("Percentage of Chargebacks in Transactions with Multiple Devices", styles['Heading2']))
report.append(Spacer(1, 12))
report.append(Image('chargebacks_multiple_devices.png', width=500, height=300))
report.append(Spacer(1, 12))

report.append(Paragraph("Distribution of Chargeback Rate per Device", styles['Heading2']))
report.append(Spacer(1, 12))
report.append(Image('chargeback_rate_per_device.png', width=500, height=300))
report.append(Spacer(1, 12))

report.append(Paragraph("Distribution of Chargeback Hours", styles['Heading2']))
report.append(Spacer(1, 12))
report.append(Image('chargeback_hours_distribution.png', width=500, height=300))
report.append(Spacer(1, 12))

# Build PDF
doc.build(report)
