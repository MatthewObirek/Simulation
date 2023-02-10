import requests
import json
import math
from queue import PriorityQueue
from geopy.distance import geodesic

# Function to calculate the total distance and change in elevation between two points
def calculate_elevation_difference(point1, point2, api_key):
    # Get the elevation data for the two points
    elev1 = get_elevation(point1, api_key)
    elev2 = get_elevation(point2, api_key)

    # Calculate the change in elevation
    elev_diff = abs(elev1 - elev2)

    return elev_diff

def calculate_distance(point1, point2):
    # Calculate the distance between the two points using the Haversine formula
    distance = geodesic(point1, point2).kilometers
    # Return the total distance and change in elevation
    return distance

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
    queue = PriorityQueue()
    queue.put(( start, [start]))
    visited = set()
    lat_diff_threshold = 0.005
    lng_diff_threshold = 0.005
    shortest_distance = calculate_distance(start, end)

    # Continue searching until the queue is empty
    while not queue.empty():
        # Get the next point from the queue
        point, path = queue.get()
        nextPoint = None;
        # Check if the point has been visited
        if point in visited:
            continue
        visited.add(point)

        # Check if the point is close enough to the end point
        lat_end, lng_end = end
        lat_pnt, lng_pnt = point
        lat_diff = abs(lat_pnt - lat_end)
        lng_diff = abs(lng_pnt - lng_end)
        if lat_diff <= lat_diff_threshold and lng_diff <= lng_diff_threshold:
            return True, path

        # Get the neighbors of the current point
        neighbors = get_neighbors(point)

        # Add the neighbors to the queue if the change in elevation is within the allowed limit
        i = 0
        chosen = 0
        for neighbor in neighbors:
            elev_change = calculate_elevation_difference(point, neighbor, api_key)
            distance = calculate_distance(neighbor, end)
            if elev_change <= max_elev_diff and distance < shortest_distance:
                chosen = i
                nextPoint = neighbor
                shortest_distance = distance
                print(shortest_distance)
            i+=1


        if nextPoint == None:
            return False, path
        
        new_path = path + [nextPoint]
        queue.put((neighbors[chosen], new_path))
        
        

    # Return None if no path was found
    return False, path

# Function to get the neighbors of a given point
def get_neighbors(point):
    # Add code to get the neighbors of the given point based on the desired resolution and geography.
    # Example:
    lat, lng = point
    return [(lat + 0.005, lng),         (lat - 0.005, lng),
            (lat, lng - 0.005),         (lat, lng + 0.005),
            (lat + 0.005, lng + 0.005), (lat - 0.005, lng - 0.005),
            (lat + 0.005, lng - 0.005), (lat - 0.005, lng + 0.005)]

def display_route_on_map(api_key, center, pathstring, zoom):

    # Build the URL for the static map
    url = "https://maps.googleapis.com/maps/api/staticmap?"
    scale = 4

    r = requests.get(url + "center=" + str(center[0])+","+str(center[1]) + "&zoom=" + str(zoom) 
                     + "&maptype=satellite" + "&scale=" + str(scale)
                     + "&path="+pathstring
                     + "&size=1200x1200&key=" + api_key)
    map = r.content

    f = open("Pictures/Pictures1"+str(center)+".png", 'wb')
    # r.content gives content, in this case gives image
    f.write(map)
    # close method of file object save and close the file
    f.close()

def toURLString(pathSet):
    path_string = ""
    i = 0;
    for point in pathSet:
        if i != 0:
            path_string += f"|"
        print(i)
        lat, lng = point
        path_string += f"{lat},{lng}"
        i=i+1
    return path_string



# Example usage
start = (49.886894, -119.497638)
end   = (49.919958, -119.393355)
f = open("API_KEY.txt","r")
api_key = f.readline()
print(str(start[0])+","+str(start[1]))
print(get_elevation(end, api_key))
max_elev_diff = 100

distance = calculate_distance(start, end)
#print(distance)
#for i in range(1,20):
#    lat, lng = start
#    start = (lat-.00, lng+.005)
#    distance = calculate_distance(start, end)
#    print(distance)
completePath, shortest_path = find_shortest_path(start, end, api_key, max_elev_diff)
print("Complete Path: " + str(completePath))
pathString = toURLString(shortest_path)
print(pathString)
display_route_on_map(api_key, start, pathString, 15)
display_route_on_map(api_key, end, pathString, 15)
display_route_on_map(api_key, (49.92689400000002,-119.44763800000004), pathString, 12)
#print("Shortest path:", shortest_path)

