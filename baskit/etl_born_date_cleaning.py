import gspread
import pandas as pd
import sqlite3

print("--- EXTRACT START ---")

client = gspread.service_account(r"D:\data_engineering\Project\docker\database-385606-4a08c85dcd54.json")

data = client.open("Salinan dari Take Home Test Data Engineer Baskit").worksheet("data").get_all_values()
df = pd.DataFrame(data[2:], columns=data[1])

print("--- EXTRACT SUCCESS ---")


print("--- TRANSFORM START ---")
# clean phone_number
df['phone_number'] = df['phone_number'].str.replace(r'\D', '', regex=True)
df['phone_number'] = df['phone_number'].apply(lambda x: '62' + x if x.startswith('8') else x if x.startswith('62') else None)

# clean born_day
def clean_born_day(born_day):
    try:
        return pd.to_datetime(born_day, errors='coerce').strftime('%Y-%m-%d')
    except ValueError:
        return None

df['born_day'] = df['born_day'].apply(clean_born_day)

print("--- TRANSFORM SUCCESS ---")


print("--- LOAD SUCCESS ---")

conn = sqlite3.connect(r'D:\data_engineering\Project\docker\db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS born_date_data (
        id TEXT PRIMARY KEY,
        name TEXT,
        phone_number TEXT,
        born_day DATE
    )
''')
conn.commit()

df.to_sql('born_date_data', conn, if_exists='replace', index=False)

result = pd.read_sql_query("SELECT * FROM born_date_data LIMIT 10", conn)
print("--- LOAD SUCCESS ---")
print(result)

