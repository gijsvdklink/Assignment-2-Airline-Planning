# Group 16
# Sjoerd Bootsma: 5242053
# Gijs van der Klink: 5389283
# Jelle Weijland: 5093457

#------------------------------------------------------------------------------------------------

import math
import pandas as pd


data_file_path = 'data/AirportData.xlsx'
data_file_path2 = 'data/Group16.xlsx'

#------------------------------------------------------------------------------------------------

def load_airport_data(file_path, sheet_name='Airport'):
    """Laadt de data van vliegvelden uit een Excel-bestand."""
    airport_data = pd.read_excel(file_path, sheet_name=sheet_name, header=None)
    airport_data_transposed = airport_data.transpose()
    airport_data_transposed.columns = airport_data_transposed.iloc[0]
    airport_data_transposed = airport_data_transposed[1:]
    return airport_data_transposed

def calculate_distance(lat1, lon1, lat2, lon2):
    """Bereken de afstand in kilometers tussen twee geografische coördinaten."""
    R = 6371  # Aarde straal in kilometers
    lat1, lon1 = math.radians(lat1), math.radians(lon1)
    lat2, lon2 = math.radians(lat2), math.radians(lon2)
    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1
    a = math.sin(delta_lat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(delta_lon / 2)**2
    delta_sigma = 2 * math.asin(math.sqrt(a))
    return R * delta_sigma

def calculate_distance_matrix(latitudes, longitudes):
    """Maak een afstandsmatrix voor de opgegeven breedte- en lengtegraden."""
    num_airports = len(latitudes)
    distance_matrix = [[0 for _ in range(num_airports)] for _ in range(num_airports)]
    for i in range(num_airports):
        for j in range(num_airports):
            if i != j:
                distance_matrix[i][j] = calculate_distance(latitudes[i], longitudes[i], latitudes[j], longitudes[j])
    return distance_matrix

def calculate_distance_dataframe(airport_data):
    """Berekent een DataFrame van afstanden tussen vliegvelden."""
    latitudes = airport_data['Latitude (deg)'].astype(float).values
    longitudes = airport_data['Longitude (deg)'].astype(float).values
    city_names = airport_data['IATA code'].tolist()
    distance_matrix = calculate_distance_matrix(latitudes, longitudes)
    distance_df = pd.DataFrame(distance_matrix, index=city_names, columns=city_names)
    return distance_df.round(1)

def save_and_print_fra_distances(distance_df, output_csv_path='DistanceMatrix_FRA.csv'):
    """Filtert de afstanden vanaf Frankfurt (FRA) en slaat ze op in een CSV-bestand."""
    if 'FRA' in distance_df.index and 'FRA' in distance_df.columns:
        fra_distances = distance_df.loc['FRA']
        filtered_distance_df = pd.DataFrame({"Distance to/from FRA": fra_distances})
        filtered_distance_df.to_csv(output_csv_path, index=True)
        print("\nFiltered distance matrix (to/from FRA):")
        print(filtered_distance_df)
    else:
        print("\nFRA not found in the dataset. No filtered distance matrix was saved.")

#------------------------------------------------------------------------------------------------

def process_demand_data(file_path2, sheet_name, output_csv_file):
    # Laad Excel-data en verwijder eerste kolom
    data = pd.read_excel(
        file_path2, 
        sheet_name=sheet_name, 
        header=None, 
        usecols=lambda x: x != 0  
)
    data.columns = [f"Column_{i}" for i in range(1, data.shape[1] + 1)]
    data = data.rename(columns={"Column_1": "Departure", "Column_2": "Arrival"})

    # Label kolommen 3 tot 32 als 0 tot 29
    columns_to_label = [f"Column_{i}" for i in range(3, 33)]  # Kolommen 3 tot 32
    new_labels = list(range(30))  # Labels 0 tot 29
    label_mapping = dict(zip(columns_to_label, new_labels))
    data = data.rename(columns=label_mapping)

    # Filter rijen waar 'FRA' in voorkomt
    fra_related_rows = data[
        (data["Departure"] == "FRA") | (data["Arrival"] == "FRA")
    ].reset_index(drop=True)

    # Sla het resultaat op als CSV-bestand
    fra_related_rows.to_csv(output_csv_file, index=False)



# Laad vliegvelddata
airport_data = load_airport_data(data_file_path)
distance_df = calculate_distance_dataframe(airport_data)
save_and_print_fra_distances(distance_df)


process_demand_data(data_file_path2, 'Group 16', 'demand_data.csv')
