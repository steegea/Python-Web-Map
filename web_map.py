"""
An app that creates a map which displays population and volcano data

Population data is from 2005
"""

import folium
import pandas
import html

#Variables tied to volcano data
data = pandas.read_csv("world_volcanoes.csv")
lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])   #In meters
name = list(data["NAME"])

#Sets the volcano marker color
#Based on the volcano's elevation (in meters)
def marker_color(elevation):
    if elevation < 1000:
        return 'green'
    elif elevation >= 1000 and elevation < 3000:
        return 'orange'
    else:
        return 'red'

#Initializes the HTML output string
marker_content = """<h4>Volcano information:</h4>
Name: <a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""

#Creates the map
map = folium.Map(location=[38.58, -99.09], zoom_start=6)

#Creating the volcano feature group
featuregroup_volc = folium.FeatureGroup(name="Volcanoes")

#Code for setting the volcano marker properties
for lt, ln, el, volc_name in zip(lat, lon, elev, name):
    iframe = folium.IFrame(html = marker_content % (volc_name, volc_name, el), width=200, height=100)
    circ_marker = folium.CircleMarker(location=[lt, ln], radius = 6, popup=folium.Popup(iframe), fill = True, fill_color = marker_color(el), color = "grey", fill_opacity = 0.7)
    featuregroup_volc.add_child(circ_marker)

#Creating the population feature group
featuregroup_pop = folium.FeatureGroup(name="Population")

#Setting the population color properties
population_data = folium.GeoJson(data=open("world.json", "r", encoding="utf-8-sig").read(), 
style_function=lambda x: {"fillColor":"green" if x["properties"]["POPULATION"] < 10000000 
else "orange" if x["properties"]["POPULATION"] >= 10000000 and x["properties"]["POPULATION"] < 20000000 else "red"}, tooltip=folium.features.GeoJsonTooltip(fields=['POPULATION']))

featuregroup_pop.add_child(population_data)

#Adds markers to the map
map.add_child(featuregroup_pop)
map.add_child(featuregroup_volc)
map.add_child(folium.LayerControl())

#The map is saved to an HTML file
map.save("web_map.html")

