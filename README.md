## 2. Algorithm Planning

### Vector Analysis Algorithm

Input: Parcel data from `parcels_shapely_ready.json`, an area threshold, a development area threshold, allowed zones, and a study-area polygon.

Output: Total active parcel area, parcels that meet the area threshold, number of parcels per zone, development candidates, and parcels that intersect the study area.

PSEUDOCODE

START

Load the parcel records from the JSON file.

Create a Parcel object for each record.

Set total_active_area to 0.

Set threshold_parcels to an empty list.

Set zone_counts to an empty dictionary.

Set development_candidates to an empty list.

Set intersecting_parcels to an empty list.

FOR each parcel:

    IF the parcel is active:
        Add its area_sqm to total_active_area.
    END IF

    IF the parcel area is greater than or equal to the chosen area threshold:
        Add the parcel to threshold_parcels.
    END IF

    Get the parcel zone.
    Increase the count for that zone by 1.

    IF the parcel is active AND
       the zone is one of the allowed zones AND
       the area is at least the development area threshold:
        Add the parcel to development_candidates.
    END IF

    IF the parcel intersects the study-area polygon:
        Add the parcel to intersecting_parcels.
    END IF

END FOR

Return total_active_area, threshold_parcels, zone_counts,
development_candidates, and intersecting_parcels.

END