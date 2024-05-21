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

# Convert values in the 'has_cbk' column to lowercase, if necessary
if df['has_cbk'].dtype == bool:
    df['has_cbk'] = df['has_cbk'].astype(str).str.lower()

# Count transactions with and without chargeback
chargeback_counts = df['has_cbk'].value_counts()

# Calculate the percentage of transactions with chargeback
if 'true' in chargeback_counts.index:
    total_chargeback = chargeback_counts.get('true', 0)
    chargeback_percent = (total_chargeback / total_transactions * 100)

# Calculate the average transaction amount
mean_transaction_amount = round(df['transaction_amount'].mean(), 2)

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

# Add chargebacks per user histogram
plt.figure(figsize=(8, 6))
sns.set(style="whitegrid")
sns.histplot(user_chargebacks, bins=range(1, user_chargebacks.max() + 2), color='skyblue', edgecolor='black', kde=True)
plt.title('Distribution of chargebacks per user')
plt.xlabel('Number of chargebacks')
plt.ylabel('User count')
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.tight_layout()
plt.savefig('chargebacks_per_user.png')
plt.close()

report.append(Paragraph("Distribution of chargebacks per user", styles['Heading2']))
report.append(Spacer(1, 12))
report.append(Image('chargebacks_per_user.png', width=400, height=300))

# Add chargebacks in transactions with multiple cards pie chart
plt.figure(figsize=(8, 6))
sns.set(style="whitegrid")
plt.pie([len(multiple_cards_chargebacks), len(multiple_cards_transactions) - len(multiple_cards_chargebacks)], labels=['With Chargeback', 'Without Chargeback'], autopct='%1.1f%%', colors=['skyblue', 'lightgreen'], startangle=90)
plt.title('Percentage of Chargebacks in Transactions with Multiple Cards')
plt.axis('equal')
plt.tight_layout()
plt.savefig('chargebacks_multiple_cards.png')
plt.close()

report.append(Paragraph("Percentage of Chargebacks in Transactions with Multiple Cards", styles['Heading2']))
report.append(Spacer(1, 12))
report.append(Image('chargebacks_multiple_cards.png', width=400, height=300))

# Add chargebacks in transactions with multiple devices pie chart
plt.figure(figsize=(8, 6))
sns.set(style="whitegrid")
plt.pie([len(multiple_devices_chargebacks), len(multiple_devices_transactions) - len(multiple_devices_chargebacks)], labels=['With Chargeback', 'Without Chargeback'], autopct='%1.1f%%', colors=['skyblue', 'lightgreen'], startangle=90)
plt.title('Percentage of Chargebacks in Transactions with Multiple Devices')
plt.axis('equal')
plt.tight_layout()
plt.savefig('chargebacks_multiple_devices.png')
plt.close()

report.append(Paragraph("Percentage of Chargebacks in Transactions with Multiple Devices", styles['Heading2']))
report.append(Spacer(1, 12))
report.append(Image('chargebacks_multiple_devices.png', width=400, height=300))

# Build PDF
doc.build(report)
