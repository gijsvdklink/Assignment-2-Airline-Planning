import pandas as pd

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
    'Fuel_Cost': [2.5, 5, 9.5],  # Fuel cost parameter in USD/gallon
    'Fleet': [2, 2, 1]  # Fleet count
})

# Conversion rate from USD to EUR
usd_to_eur_conversion_rate = 0.92  # Example rate, update with actual value if needed

# Define the fuel price in USD per gallon and convert to EUR
fuel_price_usd = 1.42  # USD/gallon
fuel_price_eur = fuel_price_usd * usd_to_eur_conversion_rate  # EUR/gallon

# Create a DataFrame to store costs for each flight leg
flight_costs_df = pd.DataFrame(index=fra_distances.index)

# Calculate costs for each aircraft type
for _, row in fleet_data.iterrows():
    type_name = row['Type']
    speed = row['Speed']  # Airspeed in km/h
    fixed_cost = row['Fixed_Cost']  # Fixed cost per flight leg
    time_cost_param = row['Time_Cost']  # Cost per hour
    fuel_cost_param = row['Fuel_Cost']  # Fuel cost parameter in USD/gallon
    
    # Convert the fuel cost parameter to EUR
    fuel_cost_param_eur = fuel_cost_param * usd_to_eur_conversion_rate  # EUR/gallon
    
    # Calculate costs
    time_costs = (time_cost_param *  (fra_distances / speed)).round(2)  # Time-based costs
    fuel_costs = (fuel_cost_param_eur * fuel_price_eur * fra_distances / 1.5).round(2)  # Fuel costs
    total_costs = (fixed_cost + time_costs + fuel_costs).round(2)  # Total operating cost
    
    # Add to DataFrame
    flight_costs_df[type_name] = total_costs

# Save the flight costs to a CSV file
output_csv_path = 'FlightCosts_FRA.csv'
flight_costs_df.to_csv(output_csv_path, index=True)

print(f"\nFlight costs have been saved to '{output_csv_path}'.")

# Example: Display the flight costs for verification
print(f"\nFlight Costs from FRA to Other Destinations:")
print(flight_costs_df)