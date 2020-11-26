from bs4 import BeautifulSoup
import pandas as pd
from folium import plugins
import folium
from random import randint

path = "./query.xml"
df   = []

with open(path) as file:
    text = file.read()
    soup = BeautifulSoup(text)

Networks = soup.find_all("network")
for Network in Networks:
    nCode             = Network.get('code') if Network.has_attr('code') else "NaN"
    nStartDate        = Network.get('startdate').split("T",1)[0] if Network.has_attr('startdate') else "NaN"
    nEndDate          = Network.get('enddate').split("T",1)[0] if Network.has_attr('enddate') else "NaN"
    nRestrictedStatus = Network.get('restrictedstatus') if Network.has_attr('restrictedstatus') else "NaN"
    nDescription      = Network.find("description").text
    
    Stations          = Network.find_all("station")
    for Station in Stations:
        sCode             = Station.get('code') if Station.has_attr('code') else "NaN"
        sStartDate        = Station.get('startdate').split("T",1)[0] if Network.has_attr('startdate') else "NaN"
        sRestrictedStatus = Station.get('restrictedstatus') if Network.has_attr('restrictedstatus') else "NaN"
        
        sLatitude  = float(Station.find("latitude").text)
        sLongitude = float(Station.find("longitude").text)
        sElevation = float(Station.find("elevation").text)
        sName      = Station.find("site").text
        df.append([nCode,
                   nDescription,
                   nStartDate,
                   nEndDate,
                   nRestrictedStatus,
                   sCode,
                   sName,
                   sStartDate,
                   sRestrictedStatus,
                   sLatitude,
                   sLongitude,
                   sElevation])
        
columns = ["Network_Code",
           "Network_Description",
           "Network_Start_Date",
           "Network_End_Date",
           "Network_Restricted_Status",
           "Station_Code",
           "Station_Name",
           "Station_Start_Date",
           "Station_Restricted_Status",
           "latitude",
           "longitude",
           "elevation"]

df      = pd.DataFrame(df,columns=columns)
r       = lambda: randint(0,255)
ranClr  = lambda: '#%02X%02X%02X' % (r(),r(),r())

center  = df[["latitude","longitude"]].mean().to_list()
m       = folium.Map(location=center,
                     zoom_start=5,
                     tiles='Stamen Terrain')

table = """<table style=\'width:100%\'>
  <tr>
    <th>Station_Name</th>
  </tr>
  <tr>
    <td>({}) {}</td>
  </tr>
  <tr>
    <th>Station_Start_Date</th>
  </tr>
  <tr>
    <td>{}</td>
  </tr>
</table>
""".format

fg       = plugins.MarkerCluster(control=False)
m.add_child(fg)

Networks = df["Network_Description"].unique()
for Network in Networks:
    Stations      = df[df["Network_Description"] == Network]
    Network_Layer = folium.plugins.FeatureGroupSubGroup(fg, Network)
    m.add_child(Network_Layer)

    color     = ranClr()
    for (Indx, Station) in Stations.iterrows():
        folium.CircleMarker(location=[Station["latitude"], Station["longitude"]],
                            radius=5,
                            popup=table(Station["Station_Code"], Station["Station_Name"], Station["Station_Start_Date"]),
                            color=color,
                            fill=True,
                            fill_color=color).add_to(Network_Layer)

folium.LayerControl().add_to(m)
m.save("gozlem_istasyonlari.html")
