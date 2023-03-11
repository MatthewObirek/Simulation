import tkinter
import tkintermapview
import osm2rail as orl
import osmium as osm
import pandas as pd
from collections import deque

# create tkinter window
root_tk = tkinter.Tk()
root_tk.geometry(f"{1000}x{700}")
root_tk.title("map_view_simple_example.py")

# create map widget
map_widget = tkintermapview.TkinterMapView(root_tk, width=1000, height=700, corner_radius=0)
map_widget.pack(fill="both", expand=True)

# set other tile server (standard is OpenStreetMap)
# map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)  # google normal
# map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)  # google satellite

subarea_name = 'Kamloops'
download_dir = './osmData'
osm_file=orl.download_osm_data_from_overpass(subarea_names=subarea_name,download_dir = download_dir,ret_download_path=True)
# osm_file = ["./osmData/Okanagan_Rail_Trail.osm"]

net=orl.get_network_from_file(filename=osm_file[0],POIs=True,check_boundary=False, target_elements=['CP Thompson Subdivision'])
#print("separator")
orl.show_network(net)
# set current position and zoom
# map_widget.set_position(52.516268, 13.377695, marker=False)  # Berlin, Germany
# map_widget.set_zoom(17)

# set current position with address
# map_widget.set_address("Berlin Germany", marker=False)

def marker_click(marker):
    print(f"marker clicked - text: {marker.text}  position: {marker.position}")

def create_adjacency_list(edges):
    adjacency_list = {}
    for edge in edges:
        p1, p2 = edge
        if p1 not in adjacency_list:
            adjacency_list[p1] = []
        if p2 not in adjacency_list:
            adjacency_list[p2] = []
        adjacency_list[p1].append(p2)
        adjacency_list[p2].append(p1)
    return adjacency_list

def bfs_iterative(adjacency_list, start):
    visited = set()
    path = []
    queue = deque([start])

    while queue:
        node = queue.popleft()
        if node not in visited:
            visited.add(node)
            path.append(node)
            for neighbor in adjacency_list[node]:
                if neighbor not in visited:
                    queue.append(neighbor)
    return path

def create_adjacency_list(edges):
    adjacency_list = {}
    for u, v in edges:
        if u not in adjacency_list:
            adjacency_list[u] = []
        adjacency_list[u].append(v)
        if v not in adjacency_list:
            adjacency_list[v] = []
        adjacency_list[v].append(u)
    return adjacency_list

def extract_simple_paths(adjacency_list):
    paths = []
    visited = set()

    for start_node in adjacency_list:
        if start_node in visited:
            continue
        
        visited.add(start_node)
        
        # Find a start node of degree 2
        neighbors = adjacency_list[start_node]
        while len(neighbors) == 2 and neighbors is not None and len(neighbors) > 0:
            next_node = neighbors[0] if neighbors[0] != start_node else neighbors[1]
            visited.add(next_node)
            start_node, next_node = next_node, start_node
            neighbors = adjacency_list.get(start_node) # Use .get() to avoid KeyError

        # Follow the path until we hit a node of degree other than 2
        if neighbors is not None and len(neighbors) > 0:
            path = [start_node]
            while len(neighbors) == 2:
                next_node = neighbors[0] if neighbors[0] != start_node else neighbors[1]
                visited.add(next_node)
                path.append(next_node)
                start_node, next_node = next_node, start_node
                neighbors = adjacency_list.get(start_node) # Use .get() to avoid KeyError
            paths.append(path + [start_node])

    return paths




#edges = [((0, 0), (0, 1)), ((0, 1), (1, 1)), ((1, 1), (1, 0)), ((1, 0), (0, 0)), ((1, 1), (2, 1)), ((2, 1), (2, 0)), ((2, 0), (1, 0))]


# set a position marker (also with a custom color and command on click)
# marker_2 = map_widget.set_marker(start[0],start[1] , text="Brandenburger Tor", command=marker_click)
# marker_3 = map_widget.set_marker(end[0], end[1], text="52.55, 13.4")
# marker_3.set_position(...)
# marker_3.set_text(...)
# marker_3.delete()

# set a path
# path_1 =  map_widget.set_path([marker_2.position, marker_3.position, (52.57, 13.4), (52.55, 13.35)])
# path_1.set_position_list(createPathFromNetwork(net))
# path_1.add_position(...)
# path_1.remove_position(...)
# path_1.delete()

pathArray = []
linkArray = []
point = None
for _,link in net.link_dict.items():
    coords = list(link.geometry.coords)
    p1 = (coords[0])
    p2 = (coords[1])
    linkArray.append([(p1[1],p1[0]),(p2[1],p2[0])])
    
#path = map_widget.set_path(linkArray[1]);
#edges = [((0, 0), (0, 1)), ((0, 1), (1, 1)), ((1, 1), (1, 0)), ((1, 0), (0, 0))]

#adjList = create_adjacency_list(linkArray)
#path =bfs_iterative(adjList, linkArray[0][0])
print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
#linkArray = [((0, 0), (0, 1)), ((0, 1), (1, 1)), ((1, 1), (1, 0)), ((1, 0), (0, 0)), ((1, 1), (2, 1)), ((2, 1), (2, 0)), ((2, 0), (1, 0))]
adjacency_list = create_adjacency_list(linkArray)
#paths = extract_simple_paths(adjacency_list)
print(adjacency_list)
railPaths = []
print(len(linkArray))
railPaths.append(map_widget.set_path(adjacency_list))


map_widget.set_position(linkArray[0][0][0], linkArray[0][0][1], marker=False)  # Berlin, Germany
map_widget.set_zoom(12)

root_tk.mainloop()