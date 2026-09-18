import json
import os

import matplotlib.pyplot as plt
from shapely.geometry import box

from spatial import SpatialObject, Parcel
from analysis import (
    total_active_area,
    parcels_above_threshold,
    count_by_zone,
    development_candidates,
    intersecting_parcels,
    classify_suitability_grid,
    count_suitable_cells,
)


def main():
    # 1. Load parcel data
    with open("data/parcels_shapely_ready.json", "r", encoding="utf-8") as file:
        records = json.load(file)

    parcels = []

    for record in records:
        parcels.append(Parcel.from_dict(record))

    if not parcels:
        raise ValueError("No parcel records were loaded.")

    # 2. Set analysis parameters
    threshold = 5000.0
    allowed_zones = {"Residential", "Commercial"}

    study_area = SpatialObject(
        box(121.050, 14.648, 121.060, 14.658)
    )

    # 3. Vector analysis
    total_area = total_active_area(parcels)

    above_threshold = parcels_above_threshold(
        parcels,
        threshold
    )

    zone_counts = count_by_zone(parcels)

    candidates = development_candidates(
        parcels,
        min_area=threshold,
        allowed_zones=allowed_zones
    )

    study_area_candidates = intersecting_parcels(
        candidates,
        study_area
    )

    # 4. Load raster data
    with open("data/suitability_grid.json", "r", encoding="utf-8") as file:
        raster_data = json.load(file)

    slope_grid = raster_data["slope_deg"]
    flood_grid = raster_data["flood_m"]
    max_slope = raster_data["criteria"]["max_slope_deg"]
    max_flood = raster_data["criteria"]["max_flood_m"]

    # 5. Raster analysis
    suitability_grid = classify_suitability_grid(
        slope_grid,
        flood_grid,
        max_slope,
        max_flood
    )

    suitable_cell_count = count_suitable_cells(suitability_grid)

    # 6. Create output directory
    os.makedirs("output", exist_ok=True)

    # 7. Create JSON report
    report = {
        "vector": {
            "parcel_count": len(parcels),
            "total_active_area_sqm": total_area,
            "zone_counts": zone_counts,
            "above_threshold_ids": [
                parcel.parcel_id for parcel in above_threshold
            ],
            "candidate_ids": [
                parcel.parcel_id for parcel in candidates
            ],
            "study_area_candidate_ids": [
                parcel.parcel_id for parcel in study_area_candidates
            ],
        },
        "raster": {
            "rows": len(suitability_grid),
            "cols": len(suitability_grid[0]),
            "suitable_cell_count": suitable_cell_count,
            "suitability_grid": suitability_grid,
        },
    }

    with open("output/lab4_report.json", "w", encoding="utf-8") as file:
        json.dump(report, file, indent=2)

    # 8. Create vector preview
    fig, ax = plt.subplots()

    for parcel in parcels:
        geometry = parcel.geometry

        if geometry.geom_type == "Polygon":
            x, y = geometry.exterior.xy
            ax.plot(x, y, linewidth=0.5)

    for parcel in candidates:
        geometry = parcel.geometry

        if geometry.geom_type == "Polygon":
            x, y = geometry.exterior.xy
            ax.plot(x, y, linewidth=1.5)

    study_geometry = study_area.geometry
    x, y = study_geometry.exterior.xy
    ax.plot(x, y, linewidth=2)

    ax.set_title("Lab 4 Vector Analysis Preview")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")

    plt.savefig(
        "output/lab4_vector_preview.png",
        dpi=150,
        bbox_inches="tight"
    )
    plt.close()

    # 9. Create raster preview
    fig, ax = plt.subplots()

    display_grid = []

    for row in suitability_grid:
        display_row = []

        for cell in row:
            if cell is None:
                display_row.append(float("nan"))
            else:
                display_row.append(cell)

        display_grid.append(display_row)

    ax.imshow(
        display_grid,
        interpolation="nearest",
        vmin=0,
        vmax=1
    )

    ax.set_title("Lab 4 Raster Suitability Preview")
    ax.set_xlabel("Column")
    ax.set_ylabel("Row")

    plt.savefig(
        "output/lab4_raster_preview.png",
        dpi=150,
        bbox_inches="tight"
    )
    plt.close()

    # 10. Print runner outputs
    print(f"Total parcels: {len(parcels)}")
    print(f"Development candidates: {len(candidates)}")
    print(
        f"Candidates inside study area: "
        f"{len(study_area_candidates)}"
    )
    print(f"Suitable raster cells: {suitable_cell_count}")


if __name__ == "__main__":
    main()