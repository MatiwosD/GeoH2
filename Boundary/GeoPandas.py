import geopandas as gpd
from shapely.geometry import Polygon
import numpy as np

# Load Namibia's boundary from the JSON file
namibia = gpd.read_file('gadm41_NAM_2.json')

print(namibia.head())  # Debugging line to check if the file was read correctly

# Get the boundary coordinates
xmin, ymin, xmax, ymax = namibia.total_bounds
hex_size = 0.1  # Adjust the size as needed

# Function to create a hexagon at a given x, y position
def create_hexagon(x_center, y_center, size):
    angle = np.linspace(0, 2 * np.pi, 7)[:-1]  # 6 sides + closing side
    x_hex = x_center + size * np.cos(angle)
    y_hex = y_center + size * np.sin(angle)
    return Polygon(zip(x_hex, y_hex))

hexagons = []
x_step = 3/2 * hex_size
y_step = np.sqrt(3) * hex_size

# Create hexagons covering the area
for x in np.arange(xmin, xmax + x_step, x_step):
    for y in np.arange(ymin, ymax + y_step, y_step):
        hexagon = create_hexagon(x, y, hex_size)
        hexagons.append(hexagon)

hex_gdf = gpd.GeoDataFrame(geometry=hexagons)
hex_gdf = gpd.clip(hex_gdf, namibia)  # Clip hexagons to Namibia's boundary
hex_gdf['country'] = 'Namibia'

# Save as GeoJSON
hex_gdf.to_file('hex_final_NA.geojson', driver='GeoJSON')

print("Hexagonal grid created and saved successfully.")