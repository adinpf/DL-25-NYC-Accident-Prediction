import geopandas as gpd
import networkx as nx
from shapely.geometry import LineString
import matplotlib.pyplot as plt

# Load the street centerlines shapefile
gdf = gpd.read_file(
    "preprocess/city_road_data/DCM_StreetCenterLine.shp")

"""
Commended out code below also from chat gpt trying to combine seg points 
"""
# Print invalid rows (if any)
# invalid_rows = gdf[~gdf.geometry.is_valid]
# print(f"Found {len(invalid_rows)} invalid geometries")

# # Try to fix them using buffer(0) trick (common Shapely workaround)
# gdf["geometry"] = gdf["geometry"].buffer(0)


G = nx.Graph()  # Use nx.DiGraph() if you want to track directionality

'this for loop is taking every point in every segment and turning it into a node'
for idx, row in gdf.iterrows():
    geom = row.geometry
    if isinstance(geom, LineString):
        coords = list(geom.coords)
        for i in range(len(coords) - 1):
            u = coords[i]
            v = coords[i + 1]
            # You can include edge attributes like street name or ID
            G.add_edge(u, v, **row.to_dict())


'I commented out the code, this is ChatGPTs solution to combing segment points into one node'
# for idx, row in gdf.iterrows():
#     attrs = row.to_dict()
#     geom = attrs.pop("geometry")  # remove geometry to avoid duplication
#     G.add_node(idx, geometry=geom, **attrs)

# # Now add edges between nodes if their geometries touch
# for i, row_i in gdf.iterrows():
#     geom_i = row_i.geometry
#     for j, row_j in gdf.iloc[i+1:].iterrows():  # avoid duplicate comparisons
#         geom_j = row_j.geometry
#         if geom_i.touches(geom_j):
#             G.add_edge(i, j)

# print(
#     f"Graph has {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")

subgraph = G.subgraph(list(G.nodes)[:1000])
plt.figure(figsize=(8, 8))
nx.draw(subgraph, node_size=1, edge_color='gray')
plt.title("NYC Street Subgraph (First 300 Nodes)")
plt.show()
