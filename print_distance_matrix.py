import sys
from distance_calculations import calculate_distance, calculate_distance_matrix
import pandas as pd

# Load airport data
data_file_path = 'AirportData.xlsx'
airport_data = pd.read_excel(data_file_path, sheet_name='Airport', header=None)
airport_data_transposed = airport_data.transpose()
airport_data_transposed.columns = airport_data_transposed.iloc[0]
airport_data_transposed = airport_data_transposed[1:]

print("\nTransposed Airport Data:")
print(airport_data_transposed)

# Calculate distances
latitudes = airport_data_transposed['Latitude (deg)'].astype(float).values
longitudes = airport_data_transposed['Longitude (deg)'].astype(float).values
city_names = airport_data_transposed['IATA code'].tolist()

distance_matrix = calculate_distance_matrix(latitudes, longitudes)
distance_df = pd.DataFrame(distance_matrix, index=city_names, columns=city_names)

# Round distance values
distance_df = distance_df.round(1)
print("\nDistance Matrix from airport i to airport j [km]:")
print(distance_df)

# Save distance matrix to a CSV file
output_csv_path = 'DistanceMatrix.csv'  # Specify the path and name of the CSV file
distance_df.to_csv(output_csv_path, index=True)

print(f"\nDistance Matrix has been saved to '{output_csv_path}'")
