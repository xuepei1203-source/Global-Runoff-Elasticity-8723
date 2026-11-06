# Input data (not included)

Place processed CSV files in `data/processed/`:

- `input_features_normalized.csv` — normalized predictors and annual elasticity (Figures 1, 3, 4, 5, 6, 7, S1).
- `station_elasticity_seasonal_1950_2015_min40years.csv` — station `lat`, `lon`, `season`, `elasticity` (Figures 2, 5, 6).
- `elasticity_perturbation_10percent.csv` — station coordinates and columns ending in `delta(+10%)` (Figure 8).
- `input_features.csv` — **non-normalized** training predictors and elasticity (Figure 9).

Figure 9 also requires raw raster/vector inputs under `data/raw/`:

- `ERA5LAND/`: PET, temperature, shallow/deep soil water, snowmelt TIFFs.
- `terrain/global_mean_terrain_slope.tif`.
- `SoilKsatDB/`: actual Ksat TIFF (update placeholder path in Figure 9).
- `LUH2_tif/`: one intended TIFF for each land-use predictor.
- `hydro/global_drainage_density_L4_final.gpkg`.
- `global_subarea_level4_0.25deg.tif`.
- `GPCC/full_data_monthly_v2022_1981_1990_025.nc`.

Check licensing and source acknowledgements before redistributing any input.
Figure 9 may need substantial RAM because all predictors are assembled into a
full global raster stack before block-wise prediction.

**Important:** Do not upload `data/raw/` or `data/processed/` to GitHub until
sharing permissions and file sizes have been reviewed. Both are gitignored.
