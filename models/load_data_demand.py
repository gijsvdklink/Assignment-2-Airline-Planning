import pandas as pd

# Load the Excel file, excluding Column_0
data_file_path2 = 'Group16.xlsx'
airport_data2 = pd.read_excel(
    data_file_path2, 
    sheet_name='Group 16', 
    header=None, 
    usecols=lambda x: x != 0  # Exclude column with index 0
)

# Rename columns for clarity based on their positions
airport_data2.columns = [f"Column_{i}" for i in range(1, airport_data2.shape[1] + 1)]

# Dynamically identify departure and destination columns
departure_column = "Column_1"  # Adjust this if departure column is at a different index
destination_column = "Column_2"  # Adjust this if destination column is at a different index
airport_data2 = airport_data2.rename(columns={departure_column: "Departure", destination_column: "Arrival"})

# Label columns 3 to 32 as 0 to 29
columns_to_label = [f"Column_{i}" for i in range(3, 33)]  # Column indices from 3 to 32
new_labels = list(range(30))  # Sequential labels from 0 to 29
label_mapping = dict(zip(columns_to_label, new_labels))  # Map old labels to new labels
airport_data2 = airport_data2.rename(columns=label_mapping)

# Filter rows where "FRA" is either in Departure or Destination
fra_related_rows = airport_data2[
    (airport_data2["Departure"] == "FRA") | (airport_data2["Arrival"] == "FRA")
]

# Reset the index to clean up the output
fra_related_rows = fra_related_rows.reset_index(drop=True)

# Save the filtered DataFrame to a CSV file
fra_related_rows.to_csv('demand_data.csv', index=False)

# Print confirmation message
print("The filtered data has been saved as 'correct_data.csv'")
