# Simulation
A personal project to investgate different modes of transit, and the effects they have

I plan to use Python and <a href="https://developers.arcgis.com/python/">ArcGIS API<a> to map and visualize data used in Civil Planning. 
  
### API_KEY and Running Project
Because I do not want to share my API key with anyone. I have saved it to a file that is not in the git repo. To run this software, you must create a `API_KEY.txt` File, and put the API key on the first line.

### Goals
- [ ] Include a Weighted Decision Matrix exploring different modes of transit for specified corridors
- [ ] For over mountain trips, I would like to put in average speed, max speed, and Max time traveled to optimise the creation of the hypothetical route.
    - [ ] Max speed would be based of off max grade and max turn radius.
    - [ ] lower average speed, paired with max speed, would allow for "shorter routes" with more bends or switch banks.
    - [ ] Max Time travelled will be the biggest determiner of the route, paired only with grade.

### Example path finding algorithm
if a point has (lat, lng, elv, distance)

def ShortestPath(start, end, maxGrade):
    distance = calculateDistance(start, end):
    neighbors = get_neighbors(start)

    for neighbor in neighbors
        rank neightbors by distance smallest to largest
    
    For point in rankedNeighbors
        Path = Path + ShortestPath(point)
