import requests
import json
import math
import cv2
import sys

# Function to calculate the total distance and change in elevation between two points
def calculate_distance(point1, point2, api_key):
    # Get the elevation data for the two points
    elev1 = get_elevation(point1, api_key)
    elev2 = get_elevation(point2, api_key)

    # Calculate the change in elevation
    elev_diff = abs(elev1 - elev2)

    # Calculate the distance between the two points using the Haversine formula
    lat1, lng1 = point1
    lat2, lng2 = point2
    lat1, lat2 = map(math.radians, [lat1, lat2])
    lng1, lng2 = map(math.radians, [lng1, lng2])
    dlat = lat2 - lat1
    dlng = lng2 - lng1
    a = (math.sin(dlat/2)**2) + math.cos(lat1) * math.cos(lat2) * (math.sin(dlng/2)**2)
    c = 2 * math.asin(math.sqrt(a))
    distance = 6371 * c

    # Return the total distance and change in elevation
    return distance, elev_diff

# Function to get the elevation for a given point from the Google Elevation API
def get_elevation(point, api_key):
    lat, lng = point
    url = f"https://maps.googleapis.com/maps/api/elevation/json?locations={lat},{lng}&key={api_key}"
    response = requests.get(url)
    data = json.loads(response.text)
    return data["results"][0]["elevation"]

# Function to find the shortest path between two points with an allowable change in altitude
def find_shortest_path(start, end, api_key, max_elev_diff):
    # Add the starting point to the queue
    queue = [(start, get_elevation(start, api_key))]
    visited = set()

    # Continue searching until the queue is empty
    while queue:
        # Get the next point from the queue
        point, elev_diff = queue.pop(0)

        # Check if the point has been visited
        if point in visited:
            continue
        visited.add(point)

        # Check if the point is the end point
        if point == end:
            return elev_diff

        # Get the neighbors of the current point
        neighbors = get_neighbors(point)

        # Add the neighbors to the queue if the change in elevation is within the allowed limit
        for neighbor in neighbors:
            distance, elev_diff = calculate_distance(point, neighbor, api_key)
            if elev_diff <= max_elev_diff:
                print(elev_diff)
                queue.append((neighbor, elev_diff))

    # Return None if no path was found
    return None

# Function to get the neighbors of a given point
def get_neighbors(point):
    # Add code to get the neighbors of the given point based on the desired resolution and geography.
    # Example:
    lat, lng = point
    return [(lat + 0.025, lng + 0.025), (lat - 0.025, lng - 0.025), (lat + 0.025, lng - 0.025), (lat - 0.025, lng + 0.025)]

def display_route_on_map(api_key, center, pathstring):

    # Build the URL for the static map
    url = "https://maps.googleapis.com/maps/api/staticmap?"
    zoom = 15
    scale = 4

    r = requests.get(url + "center=" + str(center[0])+","+str(center[1]) + "&zoom=" + str(zoom) 
                     + "&maptype=satellite" + "&scale=" + str(scale)
                     + "&path="+ str(center[0]-.0025)+","+str(center[1]-.0025)+"|"+ str(center[0])+","+str(center[1])+"|"+ str(center[0]+.0025)+","+str(center[1])
                     + "&size=1200x1200&key=" + api_key)
    map = r.content

    f = open("Pictures/Pictures"+str(center)+".png", 'wb')
    # r.content gives content, in this case gives image
    f.write(map)
    # close method of file object save and close the file
    f.close()




# Example usage
start = (49.886894, -119.497638)
end = (49.919958, -119.393355)
f = open("API_KEY.txt","r")
api_key = f.readline()
print(str(start[0])+","+str(start[1]))
print(get_elevation(end, api_key))
max_elev_diff = 100
display_route_on_map(api_key, start)
display_route_on_map(api_key, end)

#shortest_path = find_shortest_path(start, end, api_key, max_elev_diff)
#print("Shortest path:", shortest_path)

