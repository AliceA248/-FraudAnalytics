import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('spreadsheet/transactional-sample.csv', delimiter=';')

total_transactions = len(df)
print("Total de Transações:", total_transactions)

# Converter os valores da coluna 'has_cbk' para minúsculas, se necessário
if df['has_cbk'].dtype == bool:
    df['has_cbk'] = df['has_cbk'].astype(str).str.lower()

# Contar o número de transações com e sem chargeback
chargeback_counts = df['has_cbk'].value_counts()

# Exibir a contagem de transações com e sem chargeback
print("Contagem de Transações com e sem Chargeback:")
print(chargeback_counts.to_string())

# Verificar se há transações com chargeback
if 'true' in chargeback_counts.index:
    # Calcular o percentual de transações com chargeback
    total_chargeback = chargeback_counts.get('true', 0)
    chargeback_percent = (total_chargeback / total_transactions) * 100
    
    # Visualizar os resultados em um gráfico de pizza
    plt.figure(figsize=(6, 6))
    plt.pie([total_chargeback, total_transactions - total_chargeback], labels=['Com Chargeback', 'Sem Chargeback'], autopct='%1.1f%%', colors=['skyblue', 'lightgreen'])
    plt.title('Percentual de Transações com Chargeback')
    plt.show()
else:
    print("Não há transações com chargeback.")

# Calcular a média dos valores das transações
transaction_amounts = df['transaction_amount']
mean_transaction_amount = round(df['transaction_amount'].mean(), 2)

print("Média dos Valores das Transações:", mean_transaction_amount)
