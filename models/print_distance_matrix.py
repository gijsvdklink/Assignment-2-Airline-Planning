import os
import sys
import pandas as pd

# Add the project root directory to Python's module search path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

from models.distance_calculations import calculate_distance_matrix

# Load airport data
data_file_path = 'AirportData.xlsx'
airport_data = pd.read_excel(data_file_path, sheet_name='Airport', header=None)
airport_data_transposed = airport_data.transpose()
airport_data_transposed.columns = airport_data_transposed.iloc[0]
airport_data_transposed = airport_data_transposed[1:]

# Calculate distances
latitudes = airport_data_transposed['Latitude (deg)'].astype(float).values
longitudes = airport_data_transposed['Longitude (deg)'].astype(float).values
city_names = airport_data_transposed['IATA code'].tolist()

distance_matrix = calculate_distance_matrix(latitudes, longitudes)
distance_df = pd.DataFrame(distance_matrix, index=city_names, columns=city_names)

# Round distance values
distance_df = distance_df.round(1)

# Filter distances involving Frankfurt (FRA) and save to CSV
if 'FRA' in distance_df.index and 'FRA' in distance_df.columns:
    fra_distances = distance_df.loc['FRA']  # Distances from FRA to all airports

    # Create a single-column DataFrame
    filtered_distance_df = pd.DataFrame({
        "Distance to/from FRA": fra_distances
    })

    # Save the filtered distance matrix to a CSV file
    output_filtered_csv_path = 'DistanceMatrix_FRA.csv'
    filtered_distance_df.to_csv(output_filtered_csv_path, index=True)

    # Print the filtered distance matrix
    print(filtered_distance_df)
else:
    print("\nFRA not found in the dataset. No filtered distance matrix was saved.")
