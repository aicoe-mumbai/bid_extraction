import pandas as pd

# List of keywords to filter
keywords = [
    "Weapon", "Launcher", "Torpedo", "Rocket", "Sonar", "Low Frequency Variable Depth Sonar",
    "Fire Control System", "Future Combat System", "Gun", "Submarine", "Degaussing system",
    "Gear Box", "Radar Mast", "Shafting", "Helicopter", "Propulsion", "Radar", "Modular Bridge",
    "Helicopter landing Grid", "Helicopter Hangar Door", "Foldable Hanger Door", "Steering Gear",
    "Fin Stabilizer", "Winch System", "Mast Hoisting Gear", "Helicopter Traversing system",
    "Waterjet Propulsion System", "Sonar Dome", "Electric Propulsion", "Hangar Shutter",
    "Controllable Pitch propeller", "Stern Gear"
]

# Input and output file paths
input_file = r"c:\Users\20353979\Desktop\Intern Rohit\DEFPROC_SEL\output_bids_gem\bid_data.csv"
output_file = r"c:\Users\20353979\Desktop\Intern Rohit\DEFPROC_SEL\output_bids_gem\GEM_Portal_Bids.csv"  # Replace with desired output file name

# Column name to filter on
column_to_filter = "Information"  # Replace with the actual column name

# Read the CSV file into a DataFrame
df = pd.read_csv(input_file, encoding='ISO-8859-1')

# Filter rows containing any of the keywords (case insensitive)
filtered_df = df[df[column_to_filter].str.contains('|'.join(keywords), case=False, na=False)]

# Save the filtered DataFrame to a new CSV file
filtered_df.to_csv(output_file, index=False)

print(f"Filtered data has been saved to {output_file}")
