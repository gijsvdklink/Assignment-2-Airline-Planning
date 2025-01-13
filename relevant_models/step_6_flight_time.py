import pandas as pd
import numpy as np

# Load the filtered distance matrix file
distance_matrix_path = 'DistanceMatrix_FRA.csv'
distance_matrix = pd.read_csv(distance_matrix_path, index_col=0)

# Extract distances from Frankfurt (FRA) to other destinations
fra_distances = distance_matrix["Distance to/from FRA"]

# Define fleet data
fleet_data = pd.DataFrame({
    'Type': ['Small Freighter', 'Mid-size Old Freighter', 'Large Freighter'],
    'Speed': [800, 850, 920],  # Speed in km/h
    'Cargo_Capacity': [23000, 35000, 120000],  # Cargo capacity in kg
    'TAT': [90, 120, 150],  # Average Turn-Around Time in minutes
    'Max_Range': [1500, 3300, 6300],  # Maximum range in km
    'RQ': [1400, 1600, 1800],  # Runway required in meters
    'Lease_Cost': [2143, 4857, 11429],  # Lease cost in EUR/day
    'Fixed_Cost': [750, 1500, 3125],  # Fixed operating cost per flight leg in EUR
    'Time_Cost': [1875, 1938, 3500],  # Cost per hour in EUR
    'Fuel_Cost': [2.5, 5, 9.5],  # Fuel cost parameter
    'Fleet': [2, 2, 1]  # Fleet count
})

# Create a DataFrame to store flight times
flight_times_df = pd.DataFrame(index=fra_distances.index)

# Function to round up to the nearest multiple of 6
def round_up_to_multiple_of_6(x):
    return int(np.ceil(x / 6.0) * 6)

# Calculate flight time for each aircraft type and add it to the DataFrame
for _, row in fleet_data.iterrows():
    type_name = row['Type']
    speed = row['Speed']
    tat = row['TAT']
    # Calculate flight time in minutes and round up to nearest multiple of 6
    flight_times_df[type_name] = (
        ((((fra_distances / speed) + 0.5) * 60) + tat)
        .apply(round_up_to_multiple_of_6)
    )

# Save the flight times to a CSV file
output_csv_path = 'FlightTimes_FRA.csv'
flight_times_df.to_csv(output_csv_path, index=True)

print(f"\nFlight times have been saved to '{output_csv_path}'.")
