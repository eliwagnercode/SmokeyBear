# Load GeoDataFrames from CSV
import pandas as pd
import geopandas as gpd
from shapely import wkt
import json

def csv_to_gdf(filepath):
  gdf = pd.read_csv(filepath)
  gdf = gdf.drop(gdf.columns[0],axis=1)
  gdf['geometry'] = gdf['geometry'].apply(wkt.loads) # Convert geometry string to WKT geometry object
  gdf = gpd.GeoDataFrame(gdf,geometry='geometry').set_crs(epsg=4326) # Convert df to gdf
  return gdf

# County wildfire data
df_CAFires_BurnAreaByCountyAndYear = pd.read_csv(
    'https://raw.githubusercontent.com/eliwagnercode/SmokeyBear/main/CAFires_BurnAreaByCountyAndYear.csv')

# County border geometry
gdf_CACounties = csv_to_gdf(
    'https://raw.githubusercontent.com/eliwagnercode/SmokeyBear/main/gdf_CACounties.csv')
gdf_CACounties.index = gdf_CACounties['countyFIPS']
geojson_CACounties = json.loads(gdf_CACounties[['geometry']].to_json())

# Build Choropleth Map Dashboard
import plotly.express as px

df = df_CAFires_BurnAreaByCountyAndYear.copy()
Q3 = df['Total Burn Area'].quantile(0.75)
Q1 = df['Total Burn Area'].quantile(0.25)
IQR = Q3 - Q1
range_color_max = Q3 + (1.5*IQR)
fig = px.choropleth_mapbox(
    data_frame = df,
    geojson=geojson_CACounties,
    locations='FIPS',
    hover_name='County Name',
    color='Total Burn Area',
    color_continuous_scale='blues',
    range_color=(0,range_color_max),
    mapbox_style='carto-positron',
    zoom=3,
    center={'lat': 37.0902, 'lon': -119.4179},
    opacity=0.8,
    animation_frame = 'Year',
    animation_group = 'FIPS'
)
fig.show()