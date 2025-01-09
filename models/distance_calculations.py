#Group 16
#Sjoerd Bootsma:        5242053
#Gijs van der Klink:    5389283
#Jelle Weijland:        5093457

#----------------------------------------------------------------------------------------------------------------------------------------

import math

#definitions

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371


    lat1, lon1 = math.radians(lat1), math.radians(lon1)
    lat2, lon2 = math.radians(lat2), math.radians(lon2)


    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1


    a = math.sin(delta_lat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(delta_lon / 2)**2
    delta_sigma = 2 * math.asin(math.sqrt(a))
    distance = R * delta_sigma

    return distance

def calculate_distance_matrix(latitudes, longitudes):

    num_airports = len(latitudes)
    distance_matrix = [[0 for _ in range(num_airports)] for _ in range(num_airports)]

    for i in range(num_airports):
        for j in range(num_airports):
            if i != j:  
                distance_matrix[i][j] = calculate_distance(latitudes[i], longitudes[i], latitudes[j], longitudes[j])

    return distance_matrix
