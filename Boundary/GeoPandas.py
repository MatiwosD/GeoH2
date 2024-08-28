import geopandas as gpd
from shapely.geometry import Polygon, Point

# Assuming the JSON file is in the same directory as the script
namibia = gpd.read_file('gadm41_NAM_2.json')

print(namibia.head())  # Debugging line to check if the file was read correctly

# Example of creating a hexagonal grid within Namibia's boundaries
xmin, ymin, xmax, ymax = namibia.total_bounds
hex_size = 0.1  # Adjust the size as needed

hexagons = []
for x in range(int(xmin), int(xmax), int(hex_size * 2)):
    for y in range(int(ymin), int(ymax), int(hex_size * 2)):
        hexagons.append(Polygon([
            (x, y),
            (x + hex_size, y),
            (x + hex_size, y + hex_size),
            (x, y + hex_size),
            (x - hex_size, y + hex_size),
            (x - hex_size, y),
        ]))

hex_gdf = gpd.GeoDataFrame(geometry=hexagons)
hex_gdf = gpd.clip(hex_gdf, namibia)  # Clip hexagons to Namibia's boundary
hex_gdf['country'] = 'Namibia'

# Save as GeoJSON
hex_gdf.to_file('Data/hex_final_NA.geojson', driver='GeoJSON')