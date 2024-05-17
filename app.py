import pandas as pd

csv_file_path = 'spreadsheet/transactional-sample.csv'

df = pd.read_csv(csv_file_path, engine='python')

print(df.head())
