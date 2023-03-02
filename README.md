# Simulation
A personal project to investgate different modes of transit, and the effects they have

I plan to use Python and <a href="https://console.cloud.google.com/google/maps-apis/">Google MAPS API</a> to map and visualize data used in Civil Planning. 
  
### API_KEY and Running Project
Because I do not want to share my API key with anyone. I have saved it to a file that is not in the git repo. To run this software, you must create a `API_KEY.txt` File, and put *your own* API key on the first line.

### Goals
- [ ] Include a Weighted Decision Matrix exploring different modes of transit for specified corridors
- [ ] For over mountain trips, I would like to put in average speed, max speed, and Max time traveled to optimise the creation of the hypothetical route.
    - [ ] Max speed would be based of off max grade and max turn radius.
    - [ ] lower average speed, paired with max speed, would allow for "shorter routes" with more bends or switch banks.
    - [ ] Max Time travelled will be the biggest determiner of the route, paired only with grade.

### Simple Proposed Algorthm
1. Input *Start point* **S** and *End point* **E** and *Resolution* **R**
2. Load 10x10 square of points at Res ***R*** starting at ***S***, toward ***E***.
3. Create path with smallest distance, limited to Grade ***G***
4. Snap Path to selected road type: *RAIL, ROAD, PATH, etc...*
    a. IF no path snaps withing ***R*** resolution, return to step 2
5. Retreive all elevation data for path section.
6. 
    a. If Snapped Path continues toward ***E***, continue on snapped path
    
    c. Else if ***E*** is reached, Finish.

    b. Else repeat from step 2