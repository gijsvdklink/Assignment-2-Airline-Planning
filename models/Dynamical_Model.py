import pandas as pd
import numpy as np
from datetime import time, timedelta
import math



# Define the Node class
class Node:
    def __init__(self, timestamp, airport):
        self.timestamp = timestamp
        self.airport = airport
        self.total_profit = 0
        self.out_link = None

    def add_out_link(self, link):
        self.out_link = link

# Utility Functions
def add_time(current_time, hours, minutes=0):
    total_minutes = (current_time.minute + minutes) % 60
    total_hours = (current_time.hour + hours + (current_time.minute + minutes) // 60) % 24
    return time(total_hours, total_minutes)

def calculate_cost(aircraft_type, origin, destination, distance):
    """Calculate cost for a given flight."""
    print(df_aircraft, aircraft_type)
    aircraft = df_aircraft.loc[aircraft_type]
    fixed_cost = aircraft['Fixed Operating Cost (Per Flight Leg) [€]']
    fixed_cost = df_aircraft.iloc[aircraft_type, 'Fixed Operating Cost (Per Flight Leg) [€]']
    time_cost = df_aircraft.iloc[aircraft_type, 'Cost per Hour'] * distance / aircraft['Speed [km/h]']
    fuel_cost = df_aircraft.iloc[aircraft_type, 'Fuel Cost Parameter'] * fuel_price * distance / 1.5
    return fixed_cost + time_cost + fuel_cost

def calculate_revenue(distance, passengers):
    """Calculate revenue for a flight."""
    yield_factor = 5.9 * (distance ** -0.76) + 0.043
    return yield_factor * distance * passengers

def calculate_demand(timestamp, origin, destination):
    """Calculate demand between origin and destination at a given time."""
    hour = timestamp.hour
    try:
        return int(df_demand.loc[(origin, destination), str(hour)])
    except KeyError:
        return 0  # No demand for this route

def calculate_flight_time(distance, aircraft_type):
    """Calculate flight time based on distance and aircraft speed."""
    speed = df_aircraft.loc[aircraft_type, 'Speed [km/h]']
    turnaround_time = df_aircraft.loc[aircraft_type, 'Average TAT [min]'] / 60
    cruise_time = distance / speed
    return time(int(cruise_time), int((cruise_time % 1) * 60)) + timedelta(minutes=turnaround_time)

def is_flight_feasible(origin, destination, distance, aircraft_type):
    """Check if the flight is feasible based on aircraft range and airport constraints."""
    try:
        # Access the relevant parameters for the given aircraft type
        max_range = df_aircraft.loc['Maximum Range [km]', aircraft_type]
        runway_required = df_aircraft.loc['Runway Required [m]', aircraft_type]
    except KeyError as e:
        raise ValueError(f"Invalid aircraft type or parameter: {e}")
    
    # Check feasibility
    if distance > max_range:
        return False
    if df_airports.loc[origin, 'Runway (m)'] < runway_required or \
       df_airports.loc[destination, 'Runway (m)'] < runway_required:
        return False
    return True
# Load data

file_path_airports = 'adjusted_AirportData-2.xlsx'
file_path_aircraft = 'AdjustedFleetType.xlsx'
file_path_demand = 'new_demand_data.csv'
file_path_distances = 'FullDistanceMatrix.csv'

# Load Airport Data
df_airports = pd.read_excel(file_path_airports)
df_airports.set_index("IATA code", inplace=True)

# Ensure numeric columns are correctly parsed
df_airports["Latitude (deg)"] = pd.to_numeric(df_airports["Latitude (deg)"], errors="coerce")
df_airports["Longitude (deg)"] = pd.to_numeric(df_airports["Longitude (deg)"], errors="coerce")

# Load other datasets
# Load aircraft data and transpose
df_aircraft = pd.read_excel(file_path_aircraft)

# Set the first column as the index (parameters) and use the aircraft types as columns
df_aircraft.set_index(df_aircraft.columns[0], inplace=True)

print(df_aircraft)

# Transpose the DataFrame to have aircraft types as the index and parameters as columns
df_aircraft = df_aircraft.transpose()

# Ensure numeric columns are correctly parsed
df_aircraft = df_aircraft.apply(pd.to_numeric, errors='coerce')

df_demand = pd.read_csv(file_path_demand, index_col=[0, 1])  # Multi-index with Origin and Destination
df_distances = pd.read_csv(file_path_distances, index_col=0)
fuel_price = 1.42  # Example fuel price in EUR








# Main Dynamic Programming Algorithm
hub_airport = 'FRA'  # Hub airport (Frankfurt)
# Generate hourly intervals and explicitly add the final timestamp (23:59)
time_intervals = [add_time(time(0, 0), i) for i in range(24)]  # Hourly intervalsgit pull
time_intervals.append(time(23, 59))  # Add the final time explicitly
routes = {}  # Store optimal routes for each aircraft type


for aircraft_type in df_aircraft.columns:  # Iterate over column names, not index
    # Initialize nodes and profits
    nodes = {time: {airport: Node(time, airport) for airport in df_airports.index} for time in time_intervals}
    nodes[time(23, 59)][hub_airport].total_profit = 0  # End node has profit 0

    for timestamp in reversed(time_intervals[:-1]):
        for airport in df_airports.index:
            current_node = nodes[timestamp][airport]
            best_profit = -float('inf')
            best_link = None

            for destination in df_airports.index:
                distance = df_distances.loc[airport, destination]
                if is_flight_feasible(airport, destination, distance, aircraft_type):  # Pass correct aircraft type
                    demand = calculate_demand(timestamp, airport, destination)
                    passengers = min(demand, df_aircraft.loc['Cargo capacity [kg]', aircraft_type])
                    cost = calculate_cost(aircraft_type, airport, destination, distance)
                    revenue = calculate_revenue(distance, passengers)
                    profit = revenue - cost
                    flight_time = calculate_flight_time(distance, aircraft_type)
                    arrival_time = add_time(timestamp, flight_time.hour, flight_time.minute)

                    if arrival_time in nodes and destination in nodes[arrival_time]:
                        future_profit = nodes[arrival_time][destination].total_profit
                        total_profit = profit + future_profit

                        if total_profit > best_profit:
                            best_profit = total_profit
                            best_link = Link(current_node, nodes[arrival_time][destination], distance, cost, revenue, profit, passengers, flight_time)

            if best_link:
                current_node.add_out_link(best_link)
                current_node.total_profit = best_profit

    # Store route for this aircraft type
    route = []
    node = nodes[time(0, 0)][hub_airport]
    while node and node.out_link:
        route.append((node.airport, node.out_link.to_node.airport, node.out_link.profit))
        node = node.out_link.to_node
    routes[aircraft_type] = route


 
# Output results
for aircraft_type, route in routes.items():
    print(f"\nOptimal Route for {aircraft_type}:")
    for leg in route:
        print(f"From {leg[0]} to {leg[1]} with profit {leg[2]:.2f}")