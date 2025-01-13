import math
import pandas as pd

# Function to calculate distance between two coordinates
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of the Earth in km

    lat1, lon1 = math.radians(lat1), math.radians(lon1)
    lat2, lon2 = math.radians(lat2), math.radians(lon2)

    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1

    a = math.sin(delta_lat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(delta_lon / 2) ** 2
    delta_sigma = 2 * math.asin(math.sqrt(a))
    distance = R * delta_sigma

    return distance

# Function to calculate the distance matrix
def calculate_distance_matrix(latitudes, longitudes, airport_codes):
    num_airports = len(latitudes)
    distance_matrix = [[0 for _ in range(num_airports)] for _ in range(num_airports)]

    for i in range(num_airports):
        for j in range(num_airports):
            if i != j:  
                distance_matrix[i][j] = calculate_distance(latitudes[i], longitudes[i], latitudes[j], longitudes[j])

    # Create a DataFrame with airport codes as row and column labels
    distance_df = pd.DataFrame(distance_matrix, index=airport_codes, columns=airport_codes)
    return distance_df

# Load the data from your adjusted AirportData.xlsx
file_path_airports = "adjusted_AirportData-2.xlsx"  # Adjust the file name/path if needed
df_airports = pd.read_excel(file_path_airports)

# Extract relevant data
airport_codes = df_airports["IATA code"].tolist()
latitudes = df_airports["Latitude (deg)"].tolist()
longitudes = df_airports["Longitude (deg)"].tolist()

# Calculate the distance matrix
distance_df = calculate_distance_matrix(latitudes, longitudes, airport_codes)

# Save the distance matrix to a CSV file
distance_df.to_csv("FullDistanceMatrix.csv", index=True)

print("Full distance matrix saved to 'FullDistanceMatrix.csv'.")