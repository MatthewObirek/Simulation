import requests
import json

class PointData:
    def __init__(self, lat, lng, elev, denc=None, traf=None):
        self.lat = lat
        self.lng = lng
        self.elev = elev
        self.denc = denc
        self.traf = traf
    def __repr__(self):
        return f"Point({self.lat}, {self.lng}, {self.elev}) - Density:{self.denc}, Traffic;{self.traf}"    


def APILoadArray(start: PointData, end: PointData, res, api_key):
    sLat = start.lat
    sLng = start.lng
    eLat = end.lat
    eLng = end.lng
    
    latDif = eLat - sLat
    lngDif = eLng - sLng

    latDir = 0
    lngDir = 0

    if latDif < 0:
        latDir = -1
    elif latDif > 0:
        latDir = 1
    else:
        latDir = 0

    if lngDif < 0:
        lngDir = -1
    elif lngDif > 0:
        lngDir = 1
    else:
        lngDir = 0

    latDif = abs(sLat - eLat)
    lngDif = abs(sLng - eLng)
    i = 0
    locations = ""
    while not (latDif <= res): #change in latitudue
        sLng = start.lng
        lngDif = abs(sLng - eLng)
        while not (lngDif <= res): # change in longitude
            if i != 0:
                locations += f"|"
            locations += f"{sLat},{sLng}"
            print(f"{sLat}, {sLng}")
            i=i+1
            sLng = sLng + (lngDir * res)
            lngDif = abs(sLng - eLng)
            print(lngDif)
        sLat = sLat + (latDir * res)
        latDif = abs(sLat - eLat)
        print(latDif)

    print(i)
    elevData = getElevation(locations, api_key)
    sLat = start.lat
    sLng = start.lng
    eLat = end.lat
    eLng = end.lng
    
    latDif = eLat - sLat
    lngDif = eLng - sLng

    latDir = 0
    lngDir = 0

    if latDif < 0:
        latDir = -1
    elif latDif > 0:
        latDir = 1
    else:
        latDir = 0

    if lngDif < 0:
        lngDir = -1
    elif lngDif > 0:
        lngDir = 1
    else:
        lngDir = 0

    latDif = abs(sLat - eLat)
    lngDif = abs(sLng - eLng)

    i = 0
    pointMap = [PointData(0, 0, 0) for i in range(90)]
    while not (latDif <= res): #change in latitudue
        sLng = start.lng
        lngDif = abs(sLng - eLng)
        while not (lngDif <= res): # change in longitude
            pointMap[i] = PointData(sLat, sLng, elevData[i])
            print(f"{sLat}, {sLng}")
            i=i+1
            sLng = sLng + (lngDir * res)
            lngDif = abs(sLng - eLng)
        sLat = sLat + (latDir * res)
        latDif = abs(sLat - eLat)

    return pointMap

def getElevation(points, api_key):
    #lat, lng = point
    url = f"https://maps.googleapis.com/maps/api/elevation/json?locations="+points+f"&key={api_key}"
    response = requests.get(url)
    #print(response.text)
    data = json.loads(response.text)
    elevations = [result["elevation"] for result in data["results"]]
    return elevations

def create_map(data):
    elevation_map = {}
    for point in data:
        lat, lng, elev = point
        elevation_map[(lat, lng)] = elev
    return elevation_map

def get_elevation(lat, lng, elevation_map):
    return elevation_map.get((lat, lng), None)


start = PointData(49.900138, -119.366779, 0)
end   = PointData(49.950138, -119.316779, 0) #(49.484091, -119.600200)

mid   = ((end.lat - start.lat)/2 + start.lat, (end.lng - start.lng)/2 + start.lng) 
f = open("API_KEY.txt","r")
api_key = f.readline()
max_elev_diff = 50
resolution = .005

print(mid)

pointArray = APILoadArray(start, end, resolution, api_key)

for point in pointArray:
    print(point)