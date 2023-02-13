import requests
import json
import math
from queue import PriorityQueue
from geopy.distance import geodesic
#TODO: Task list
#! Rewrite mapRouteToPNG for better naming scheme
#! call and save elevation data to speed up runtimes - call and save to a file.
#! find potential way to include full path programatically.
#! Delete all current pictures - rename them
#! - or call large area all at once
#! Fix Path Finding Algorithm, allowing it to choose options that are farther away than present - only if a closer option is not available.



# Function to calculate the total distance and change in elevation between two points
def calculateElevationDifference(point1, point2, api_key):
    # Get the elevation data for the two points
    elev1 = getElevation(point1, api_key)
    elev2 = getElevation(point2, api_key)

    # Calculate the change in elevation
    elev_diff = abs(elev1 - elev2)

    return elev_diff

def calculateDistance(point1, point2):
    # Calculate the distance between the two points using the Haversine formula
    distance = geodesic(point1, point2).kilometers
    # Return the total distance and change in elevation
    return distance

# Function to get the elevation for a given point from the Google Elevation API
def getElevation(point, api_key):
    lat, lng = point
    url = f"https://maps.googleapis.com/maps/api/elevation/json?locations={lat},{lng}&key={api_key}"
    response = requests.get(url)
    data = json.loads(response.text)
    return data["results"][0]["elevation"]

# Function to find the shortest path between two points with an allowable change in altitude
def findShortestPath(start, end, api_key, max_elev_diff):
    # Add the starting point to the queue
    queue = PriorityQueue()
    queue.put(( start, [start]))
    visited = set()
    lat_diff_threshold = 0.005
    lng_diff_threshold = 0.005
    shortest_distance = calculateDistance(start, end)

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
        shortest_available_distance = -1;
        for neighbor in neighbors:
            elevChange = calculateElevationDifference(point, neighbor, api_key)
            distance = calculateDistance(neighbor, end)
            if shortest_available_distance == -1:
                shortest_available_distance = distance
                
            if elevChange <= max_elev_diff and distance < shortest_distance:
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

def mapRouteToPNG(api_key, center, zoom, pathstring, name="Picture"):

    # Build the URL for the static map
    url = "https://maps.googleapis.com/maps/api/staticmap?"
    scale = 4

    r = requests.get(url + "center=" + str(center[0])+","+str(center[1]) + "&zoom=" + str(zoom) 
                     + "&maptype=satellite" + "&scale=" + str(scale)
                     + "&path="+pathstring
                     + "&size=1200x1200&key=" + api_key)
    map = r.content

    f = open("Pictures/"+name+"z"+str(zoom)+"l"+str(center)+".png", 'wb')
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
start = (49.900138, -119.366779)
end   = (49.484091, -119.600200)
f = open("API_KEY.txt","r")
api_key = f.readline()
max_elev_diff = 50

completePath, shortest_path = findShortestPath(start, end, api_key, max_elev_diff)
print("Complete Path: " + str(completePath))
pathString = toURLString(shortest_path)
print(pathString)
mapRouteToPNG(api_key, start, 12, pathString, "Kel")
mapRouteToPNG(api_key, end, 12, pathString, "Pen")
mapRouteToPNG(api_key, (49.67933, -119.535625), 9, pathString, "KelToPen")
#print("Shortest path:", shortest_path)

