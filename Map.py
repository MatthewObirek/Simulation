from bokeh.io import output_notebook, show
from bokeh.plotting import gmap
from bokeh.models import GMapOptions

f = open("API_KEY.txt","r")
api_key = f.read().strip()

# Set up Google Maps API options
map_options = GMapOptions(lat=37.7749, lng=-122.4194, map_type="roadmap", zoom=13)

# Create the plot
p = gmap(google_api_key=google_maps_api_key, map_options=map_options, title="My Path")

# Define the latitude and longitude coordinates of the 5 points
points = [
    (37.7901, -122.3996),  # Point 1
    (37.7895, -122.4009),  # Point 2
    (37.7886, -122.4021),  # Point 3
    (37.7878, -122.4029),  # Point 4
    (37.7872, -122.4043)   # Point 5
]

# Extract the latitude and longitude coordinates into separate lists
latitudes, longitudes = zip(*points)

# Add the points to the plot
p.circle(x=longitudes, y=latitudes, size=15, fill_color='blue')

# Show the plot
show(p)
