from shapely.geometry import box

from src.spatial import Parcel
from src.analysis import (
    total_active_area,
    parcels_above_threshold,
    count_by_zone,
    development_candidates,
    intersecting_parcels,
    classify_suitability_grid,
    count_suitable_cells,
)


def make_parcel(parcel_id, zone, active, area, geometry):
    return Parcel(
        parcel_id,
        geometry,
        {
            "zone": zone,
            "is_active": active,
            "area_sqm": area,
        },
    )


def test_parcel_from_dict():
    record = {
        "parcel_id": "P001",
        "zone": "Residential",
        "is_active": True,
        "area_sqm": 5000,
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [121.050, 14.648],
                [121.051, 14.648],
                [121.051, 14.649],
                [121.050, 14.649],
                [121.050, 14.648],
            ]],
        },
    }

    parcel = Parcel.from_dict(record)

    assert parcel.parcel_id == "P001"
    assert parcel.zone == "Residential"
    assert parcel.is_active is True
    assert parcel.area_sqm == 5000
    assert parcel.geometry.geom_type == "Polygon"


def test_total_active_area_excludes_inactive():
    parcels = [
        make_parcel("P1", "Residential", True, 5000, box(0, 0, 1, 1)),
        make_parcel("P2", "Commercial", False, 3000, box(2, 2, 3, 3)),
    ]

    assert total_active_area(parcels) == 5000


def test_parcels_above_threshold_includes_exact_threshold():
    parcels = [
        make_parcel("P1", "Residential", True, 5000, box(0, 0, 1, 1)),
        make_parcel("P2", "Residential", True, 4999, box(2, 2, 3, 3)),
    ]

    result = parcels_above_threshold(parcels, 5000)

    assert [p.parcel_id for p in result] == ["P1"]


def test_count_by_zone():
    parcels = [
        make_parcel("P1", "Residential", True, 5000, box(0, 0, 1, 1)),
        make_parcel("P2", "Residential", True, 6000, box(2, 2, 3, 3)),
        make_parcel("P3", "Commercial", True, 7000, box(4, 4, 5, 5)),
    ]

    assert count_by_zone(parcels) == {
        "Residential": 2,
        "Commercial": 1,
    }


def test_development_candidates_rejects_each_reason():
    parcels = [
        make_parcel("ACTIVE_OK", "Residential", True, 5000, box(0, 0, 1, 1)),
        make_parcel("INACTIVE", "Residential", False, 6000, box(2, 2, 3, 3)),
        make_parcel("BAD_ZONE", "Industrial", True, 6000, box(4, 4, 5, 5)),
        make_parcel("TOO_SMALL", "Commercial", True, 4999, box(6, 6, 7, 7)),
    ]

    result = development_candidates(
        parcels,
        min_area=5000,
        allowed_zones={"Residential", "Commercial"},
    )

    assert [p.parcel_id for p in result] == ["ACTIVE_OK"]


def test_intersecting_parcels():
    parcels = [
        make_parcel("INSIDE", "Residential", True, 5000, box(0, 0, 2, 2)),
        make_parcel("OUTSIDE", "Residential", True, 5000, box(5, 5, 6, 6)),
    ]

    study_area = make_parcel(
        "STUDY",
        "Study",
        True,
        0,
        box(1, 1, 3, 3),
    )

    result = intersecting_parcels(parcels, study_area)

    assert [p.parcel_id for p in result] == ["INSIDE"]


def test_classify_suitability_grid():
    slope = [
        [10, 20],
        [15, None],
    ]

    flood = [
        [0.3, 0.2],
        [0.5, None],
    ]

    result = classify_suitability_grid(
        slope,
        flood,
        max_slope=15,
        max_flood=0.5,
    )

    assert result == [
        [1, 0],
        [1, None],
    ]


def test_count_suitable_cells():
    grid = [
        [1, 0, None],
        [1, 1, 0],
    ]

    assert count_suitable_cells(grid) == 3