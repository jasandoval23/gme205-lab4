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


def development_candidates(parcels, min_area, allowed_zones):
    candidates = []

    for parcel in parcels:
        if parcel.is_active and parcel.zone in allowed_zones and parcel.area_sqm >= min_area:
            candidates.append(parcel)

    return candidates


def intersecting_parcels(parcels, study_area):
    result = []

    for parcel in parcels:
        if parcel.intersects(study_area):
            result.append(parcel)

    return result