import pandas as pd
from datetime import datetime

# Provide the full path to the file
file_path = r'c:\Users\20353979\Desktop\Intern Rohit\DEFPROC_SEL\output_bids_gem\bid_data.csv'

# Load the CSV file
df = pd.read_csv(file_path, encoding='ISO-8859-1')

# Convert the 'End Date' column to datetime
df['End Date'] = pd.to_datetime(df['End Date'], format='%d-%m-%Y %I:%M %p', errors='coerce')

# Drop rows where 'End Date' could not be parsed
df = df.dropna(subset=['End Date'])

# Get the current datetime
current_time = datetime.now()

# Filter rows where 'End Date' is greater than the current time
df_filtered = df[df['End Date'] > current_time]

# Overwrite the original file with the filtered data
df_filtered.to_csv(file_path, index=False)

print(f"File '{file_path}' has been updated with filtered data")
