from geopy.distance import geodesic

# Calculate distance using geopy (accurate earth model)
def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    return geodesic((lat1, lon1), (lat2, lon2)).km