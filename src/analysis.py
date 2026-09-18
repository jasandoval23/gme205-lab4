def total_active_area(parcels):
    total = 0

    for parcel in parcels:
        if parcel.is_active:
            total += parcel.area_sqm

    return total


def parcels_above_threshold(parcels, threshold):
    result = []

    for parcel in parcels:
        if parcel.area_sqm >= threshold:
            result.append(parcel)

    return result


def count_by_zone(parcels):
    counts = {}

    for parcel in parcels:
        zone = parcel.zone

        if zone not in counts:
            counts[zone] = 0

        counts[zone] += 1

    return counts


def is_development_candidate(parcel, min_area, allowed_zones):
    if not parcel.is_active:
        return False

    if parcel.zone not in allowed_zones:
        return False

    if parcel.area_sqm < min_area:
        return False

    return True


def development_candidates(parcels, min_area, allowed_zones):
    candidates = []

    for parcel in parcels:
        if is_development_candidate(parcel, min_area, allowed_zones):
            candidates.append(parcel)

    return candidates


def intersecting_parcels(parcels, study_area):
    result = []

    for parcel in parcels:
        if parcel.intersects(study_area):
            result.append(parcel)

    return result


def classify_suitability_grid(slope_grid, flood_grid, max_slope, max_flood):
    if len(slope_grid) != len(flood_grid):
        raise ValueError("Slope and flood grids must have the same number of rows")

    suitability_grid = []

    for row_index in range(len(slope_grid)):
        if len(slope_grid[row_index]) != len(flood_grid[row_index]):
            raise ValueError("Slope and flood grids must have the same dimensions")

        suitability_row = []

        for col_index in range(len(slope_grid[row_index])):
            slope = slope_grid[row_index][col_index]
            flood = flood_grid[row_index][col_index]

            if slope is None or flood is None:
                suitability_row.append(None)
            elif slope <= max_slope and flood <= max_flood:
                suitability_row.append(1)
            else:
                suitability_row.append(0)

        suitability_grid.append(suitability_row)

    return suitability_grid


def count_suitable_cells(suitability_grid):
    count = 0

    for row in suitability_grid:
        for cell in row:
            if cell == 1:
                count += 1

    return count