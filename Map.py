import tkinter
import tkintermapview
import osm2rail as orl
import osmium as osm
import pandas as pd
import sys
from typing import List, Callable
from collections import deque

from tkintermapview.canvas_position_marker import CanvasPositionMarker

CanvasPositionMarker.right_click_menu_commands: List[dict] = []  # list of dictionaries with "label": str, "command": Callable, "pass_coords": bool

def add_right_click_menu_command(self, label: str, command: Callable, pass_coords: bool = False) -> None:
    CanvasPositionMarker.map_widget.canvas.bind("<Button-3>", CanvasPositionMarker.map_widget.mouse_right_click)
    self.right_click_menu_commands.append({"label": label, "command": command, "pass_coords": pass_coords})

CanvasPositionMarker.add_right_click_menu_command = add_right_click_menu_command

# create tkinter window
root_tk = tkinter.Tk()
root_tk.geometry(f"{1000}x{700}")
root_tk.title("map_view_simple_example.py")

# create map widget
map_widget = tkintermapview.TkinterMapView(root_tk, width=1000, height=700, corner_radius=0)
map_widget.pack(fill="both", expand=True)

# set other tile server (standard is OpenStreetMap)
# map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)  # google normal
map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)  # google satellite
map_widget.set_overlay_tile_server("http://a.tiles.openrailwaymap.org/standard/{z}/{x}/{y}.png")  # railway infrastructure

#map_widget.set_tile_server("http://c.tile.stamen.com/watercolor/{z}/{x}/{y}.png")  # painting style
subarea_name = 'Kamloops'
download_dir = './osmData'
#osm_file=orl.download_osm_data_from_overpass(subarea_names=subarea_name,download_dir = download_dir,ret_download_path=True)
# osm_file = ["./osmData/Okanagan_Rail_Trail.osm"]

#net=orl.get_network_from_file(filename=osm_file[0],POIs=True,check_boundary=False, target_elements=['CP Thompson Subdivision'])
#print("separator")
#orl.show_network(net)
# set current position and zoom
# map_widget.set_position(52.516268, 13.377695, marker=False)  # Berlin, Germany
# map_widget.set_zoom(17)

# set current position with address
# map_widget.set_address("Berlin Germany", marker=False)

def marker_click(marker):
    print(f"marker clicked - text: {marker.text}  position: {marker.position}")

def marker_right_click(marker):
    print(marker.coords)

def add_marker_event(coords):
    print("Add marker:", coords)
    new_marker = map_widget.set_marker(coords[0], coords[1], text="new marker", command=marker_click)
    new_marker.add_right_click_menu_command(label="coords",
                                        command=marker_right_click,
                                        pass_coords=True)

    

map_widget.add_right_click_menu_command(label="Add Marker",
                                        command=add_marker_event,
                                        pass_coords=True)


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




map_widget.set_position(49.8784991, -119.4544503, marker=False)  # ~ Kamloops, BC, Canada
map_widget.set_zoom(12)

root_tk.mainloop()