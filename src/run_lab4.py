import json

from shapely.geometry import box

from spatial import SpatialObject, Parcel
from analysis import (
    development_candidates,
    intersecting_parcels,
    classify_suitability_grid,
    count_suitable_cells,
)


# Load parcel data
with open("data/parcels_shapely_ready.json", "r", encoding="utf-8") as file:
    records = json.load(file)

parcels = []

for record in records:
    parcel = Parcel.from_dict(record)
    parcels.append(parcel)


# Define the study area
study_area = SpatialObject(
    box(121.050, 14.648, 121.060, 14.658)
)


# Find development candidates
candidates = development_candidates(
    parcels,
    min_area=5000.0,
    allowed_zones={"Residential", "Commercial"},
)


# Find candidates that intersect the study area
inside_study_area = intersecting_parcels(
    candidates,
    study_area,
)


# Load raster-style suitability data
with open("data/suitability_grid.json", "r", encoding="utf-8") as file:
    raster_data = json.load(file)

slope_grid = raster_data["slope_deg"]
flood_grid = raster_data["flood_m"]

max_slope = raster_data["criteria"]["max_slope_deg"]
max_flood = raster_data["criteria"]["max_flood_m"]


# Classify the raster cells
suitability_grid = classify_suitability_grid(
    slope_grid,
    flood_grid,
    max_slope,
    max_flood,
)


# Count suitable cells
suitable_cells = count_suitable_cells(suitability_grid)


# Report results
print("Total parcels:", len(parcels))
print("Development candidates:", len(candidates))
print("Candidates inside study area:", len(inside_study_area))
print("Suitable raster cells:", suitable_cells)