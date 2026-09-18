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

## 3. Required Challenges

### Challenge 1 – Change the Policy Without Rewriting the Algorithm

I ran `development_candidates()` using two different parameter sets while keeping the function implementation unchanged.

First run:
- Minimum area: 5000.0 sqm
- Allowed zones: Residential and Commercial
- Development candidates: 45
- Candidates inside study area: 9

Second run:
- Minimum area: 10000.0 sqm
- Allowed zones: Residential and Commercial
- Development candidates: 18
- Candidates inside study area: 4

Changing the parameters changed the results without requiring changes to the analysis function itself. This shows that the development policy can be changed through inputs rather than by rewriting the algorithm.

### Challenge 2 – Compose, Do Not Duplicate

The study-area result is produced by composing existing analysis functions. First, `development_candidates()` identifies parcels that satisfy the development rules. The resulting candidates are then passed to `intersecting_parcels()` to identify which candidates intersect the study area.

This avoids repeating the active, zone, area, and intersection rules in one large conditional block.

### Challenge 3 – Bad vs Good Refactor

An example of a less structured approach would be putting the active, zone, area, and intersection checks inside one large nested conditional block.

The final version separates the development rule into `is_development_candidate()` and uses `development_candidates()` to apply that rule to the parcels. The intersection check is also handled separately by `intersecting_parcels()`.

This makes each function responsible for one part of the analysis and makes the logic easier to test and reuse.

### Challenge 4 – Transfer the Algorithmic Pattern

The vector and raster analyses both use repetition and selection, but the repeated structure is different.

For vector data, the program loops through Parcel objects and applies analysis rules to each object. The Parcel object is responsible for its geometry and parcel attributes.

For raster data, the program uses nested loops because a raster is represented as rows and columns of cells. Each cell is classified based on the slope and flood values.

The overall pattern is similar: inspect an input, apply a rule, and produce a result. The main difference is the representation of the data.

## 4. Reflection

### 1. Algorithm

For my vector analysis, I worked on identifying development candidates from the parcel data. Writing the algorithm and pseudocode first helped me break the problem into smaller steps before coding. It also helped me see which parts needed loops and which parts needed conditions. Because of this, I was able to separate the analysis into different functions instead of putting everything in one block.

### 2. Control Flow

Sequence can be seen in the order of loading the data, setting the parameters, running the analysis, and creating the outputs. Selection is used when the program checks conditions, such as whether a parcel is active, in an allowed zone, or large enough. Repetition is used when going through the parcels. For the raster, repetition happens through the rows and the cells in each row.

### 3. Responsibility

I kept geometry-related behavior in `SpatialObject` and `Parcel` because these classes represent the spatial objects. For example, the `intersects()` method deals with the geometry of the object. The analysis rules are in `analysis.py` because they describe what should be done with the data. I think separating these responsibilities makes the code easier to understand and test.

### 4. Conditional Structure

The development-candidate logic is separated into `is_development_candidate()` instead of putting all the conditions into one deeply nested block. The function checks if the parcel is active, if its zone is allowed, and if its area meets the minimum requirement. It returns `False` when a requirement is not met. This keeps `development_candidates()` simple because it only needs to apply the rule to each parcel.

### 5. Area Meaning

The exercise uses `area_sqm` because this is the area attribute provided in the parcel data and it represents the parcel area in square meters. I should not directly treat `geometry.area` as square meters because the parcel geometry is based on longitude and latitude coordinates. The geometry's area value would not automatically have square-meter units.

### 6. Vector vs Raster

For the vector data, the program repeats over the `Parcel` objects, with each iteration processing one parcel. For the raster data, the program uses a nested loop because the raster is represented as rows and columns of cells. The basic idea is still similar: go through the data, check the required conditions, and produce a result. The main difference is how the data is represented.

### 7. Scale

If there were one million parcels, the same separation between the object model, analysis functions, and runner would still be useful. However, the way the data is loaded and processed might need to be improved because of the larger amount of data. For a 10,000 × 10,000 raster, the nested-loop approach still follows the same algorithm, but processing time and memory would become bigger concerns. The overall structure could stay, but the implementation would need to be more efficient.