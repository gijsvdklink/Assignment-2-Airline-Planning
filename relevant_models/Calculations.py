import pandas as pd
import os
import numpy as np

distance_matrix_path = 'DistanceMatrix_FRA.csv'


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


def calculate_operating_costs(distances, fleet_data):
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

def calculate_and_save_flight_times(fra_distances, fleet_data, output_csv_path):

    # Maak een DataFrame om vluchtduur op te slaan
    flight_times_df = pd.DataFrame(index=fra_distances.index)

    # Bereken vluchtduur voor elk vliegtuigtype en voeg het toe aan de DataFrame
    for _, row in fleet_data.iterrows():
        type_name = row['Type']
        speed = row['Speed']
        tat = row['TAT']
        
        # Bereken vluchtduur in minuten en rond af naar het dichtstbijzijnde veelvoud van 6
        flight_times_df[type_name] = (
            ((((fra_distances / speed) + 0.5) * 60) + tat)
            .apply(lambda x: int(np.ceil(x / 6.0) * 6))  # Ronden binnen de berekening
        )

    # Sla de vluchtduur op in een CSV-bestand
    flight_times_df.to_csv(output_csv_path, index=True)
    print(f"\nFlight times have been saved to '{output_csv_path}'.")


distances = pd.read_csv(distance_matrix_path, index_col=0)["Distance to/from FRA"]
operating_costs = calculate_operating_costs(distances, fleet_data)
output_csv_path = 'OperatingCosts_FRA.csv'
operating_costs.to_csv(output_csv_path, index=True)


calculate_and_save_flight_times(distances, fleet_data, 'FlightTimes_FRA.csv')