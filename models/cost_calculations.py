import pandas as pd
import os

def calculate_operating_costs(distances, fleet_data):
    """
    Calculate operating costs for each flight leg using the provided formulas.

    Args:
        distances (pd.Series): Series with distances between airports.
        fleet_data (pd.DataFrame): DataFrame with aircraft data.

    Returns:
        pd.DataFrame: DataFrame with total operating costs for each aircraft type and airport.
    """
    total_costs_df = pd.DataFrame(index=distances.index)

    for _, row in fleet_data.iterrows():
        type_name = row['Type']
        fixed_cost = row['Fixed_Cost']
        time_cost_param = row['Time_Cost']
        fuel_cost_param = row['Fuel_Cost']
        airspeed = row['Speed']

        # Fixed operating cost (C^k_X)
        fixed_operating_cost = fixed_cost

        # Time-based costs (C^k_Tij)
        time_based_costs = (time_cost_param * distances / airspeed).round(2)

        # Fuel costs (C^k_Fij)
        fuel_costs = (fuel_cost_param * 1.42 *0.97*  distances / 1.5).round(2)

        # Total operating cost (C^k_ij)
        total_costs = fixed_operating_cost + time_based_costs + fuel_costs
        total_costs_df[type_name] = total_costs.round(2)

    return total_costs_df


if __name__ == "__main__":
    # Verify the input file exists
    distance_matrix_path = 'DistanceMatrix_FRA.csv'
    if not os.path.exists(distance_matrix_path):
        print(f"Error: '{distance_matrix_path}' not found.")
        exit(1)

    # Load distance data
    try:
        distances = pd.read_csv(distance_matrix_path, index_col=0)["Distance to/from FRA"]
        print(f"Loaded distances from '{distance_matrix_path}':\n{distances.head()}")
    except Exception as e:
        print(f"Error loading distances: {e}")
        exit(1)

    # Fleet data
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

    # Calculate operating costs
    try:
        operating_costs = calculate_operating_costs(distances, fleet_data)
        print(f"Operating costs calculated successfully:\n{operating_costs.head()}")
    except Exception as e:
        print(f"Error calculating operating costs: {e}")
        exit(1)

    # Save total operating costs to CSV
    output_csv_path = 'OperatingCosts_FRA.csv'
    try:
        operating_costs.to_csv(output_csv_path, index=True)
        print(f"Operating costs have been saved to '{output_csv_path}'.")
    except Exception as e:
        print(f"Error saving operating costs to file: {e}")
        exit(1)
