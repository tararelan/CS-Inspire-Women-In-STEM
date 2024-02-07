import pandas as pd
import pycountry_convert as pc
import folium
import webbrowser

from geopy import Nominatim
from folium.plugins import MarkerCluster

geolocator = Nominatim(user_agent='maps.py')

data_set = pd.read_csv('map.csv', header=0)
data_set = data_set.values.tolist()

for i in range(len(data_set)):
    data_set[i].append(pc.country_name_to_country_alpha2(data_set[i][0]))
    data_set[i].append(pc.country_alpha2_to_continent_code(data_set[i][2]))
    loc = geolocator.geocode(data_set[i][0])
    data_set[i].append(loc.latitude)
    data_set[i].append(loc.longitude)

data_set = pd.DataFrame(data_set, columns=[
                        'CountryName', 'User_Num', 'Country', 'Continent', 'Latitude', 'Longitude'])

world_map = folium.Map(tiles="cartodbpositron")
marker_cluster = MarkerCluster().add_to(world_map)
for i in range(len(data_set)):
    lat = data_set.iloc[i]['Latitude']
    long = data_set.iloc[i]['Longitude']
    if data_set.iloc[i]['User_Num'] < 5:
        radius = 6
    elif 6 < data_set.iloc[i]['User_Num'] < 10:
        radius = 8
    else:
        radius = 10
    popup_text = """{country}<br>
                    {users} Users<br>"""
    popup_text = popup_text.format(
        country=data_set.iloc[i]['CountryName'], users=data_set.iloc[i]['User_Num'])
    iframe = folium.IFrame(html=popup_text, width=125, height=60)
    popup = folium.Popup(iframe, max_width=500)
    folium.CircleMarker(location=[lat, long], radius=radius,
                        popup=popup, fill=True).add_to(marker_cluster)

world_map.save("profile_of_user\\templates\\map.html")
# webbrowser.open("profile_of_user\\templates\\map.html")