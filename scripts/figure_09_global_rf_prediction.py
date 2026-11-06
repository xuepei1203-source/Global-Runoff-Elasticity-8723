import pandas as pd
import numpy as np
import geopandas as gpd
import xarray as xr
import rasterio
from rasterio.features import rasterize
from rasterio.transform import from_origin
from rasterio.warp import reproject, Resampling
from sklearn.ensemble import RandomForestRegressor
import joblib
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap  # Custom green colour scale
import os
import gc
from pathlib import Path

# Resolve the GitHub project root from the scripts directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent
FIGURE_DIR = PROJECT_ROOT / "outputs" / "figures"
FIGURE_DIR.mkdir(parents=True, exist_ok=True)

# =========================
# External input paths
# =========================
drainage_gpkg = r"D:\Data\data\250609\hydro\global_drainage_density_L4_final.gpkg"
drainage_field = "drainage_density"
sub_area_tif = r"D:\Data\data\250710\global_subarea_level4_0.25deg.tif"  # Catchment area raster
luh2_dir = r"D:\Data\data\250724\LUH2_tif"  # LUH2 raster directory
gpcc_nc = r"D:\Data\GPCC\full_data_monthly_v2022_1981_1990_025.nc"

# Project output directories
out_dir = str(PROJECT_ROOT / "outputs" / "results")
os.makedirs(out_dir, exist_ok=True)

# Environmental driver rasters
driver_tifs = {
    "PET": r"D:\Data\data\250724\ERA5LAND\global_mean_PET_1950_2015.tif",
    "Temperature": r"D:\Data\data\250724\ERA5LAND\global_mean_temp_1950_2015.tif",
    "SoilWaterV1": r"D:\Data\data\250724\ERA5LAND\global_mean_soilwaterV1_1950_2015.tif",
    "SoilWaterV4": r"D:\Data\data\250724\ERA5LAND\global_mean_soilwaterV4_1950_2015.tif",
    "Snowmelt": r"D:\Data\data\250724\ERA5LAND\snowmelt_1950_2015_average.tif",
    "TerrainSlope": r"D:\Onedrive\world_data\20250414\global_mean_terrain_slope.tif",
    "SaturatedKsat": r"D:\Data\SoilKsatDB\Global_Ksat_1Km_s0....0cm_v1.0.tif",
}

# LUH2 land-use variables
luh2_vars = [
    "urban", "primf", "secdn", "c3ann", "c4ann",
    "c3per", "c4per", "c3nfx", "pastr", "range", "secmb", "secma"
]

# =========================
# 1. Load the reference raster
# =========================
template = list(driver_tifs.values())[0]
with rasterio.open(template) as src:
    height, width = src.height, src.width
    transform, crs = src.transform, src.crs
    profile = src.profile.copy()

print(f"Target raster size: {height} x {width}")

# =========================
# 2. Create the GPCC land mask and resample it
# =========================
land_nc = xr.open_dataset(gpcc_nc)
landmask = ~np.isnan(land_nc['precip'].isel(time=0).values)
landmask = landmask.astype(float)
landmask[landmask == 0] = np.nan
print("GPCC land mask created")

gpcc_lat = land_nc['lat'].values
gpcc_lon = land_nc['lon'].values
src_transform = from_origin(
    gpcc_lon.min(),
    gpcc_lat.max(),
    np.abs(gpcc_lon[1] - gpcc_lon[0]),
    np.abs(gpcc_lat[1] - gpcc_lat[0])
)

resampled_landmask = np.empty((height, width), dtype=np.float32)
reproject(
    source=landmask,
    destination=resampled_landmask,
    src_transform=src_transform,
    src_crs="EPSG:4326",
    dst_transform=transform,
    dst_crs="EPSG:4326",
    resampling=Resampling.nearest
)

landmask = np.where(resampled_landmask > 0, 1, np.nan)
print("Land mask resampled, shape:", landmask.shape)

# =========================
# 3. Load training data and identify features
# =========================
df = pd.read_csv(PROJECT_ROOT / "data" / "processed" / "input_features.csv")

print("CSV columns:", df.columns.tolist())

# Drop Up_area when present
if 'Up_area' in df.columns:
    df = df.drop(columns=['Up_area'])
    print("Dropped Up_area column")

exclude_columns = ['lon', 'lat', 'gsim.no', 'n_years', 'elasticity']
feature_names = [col for col in df.columns if col not in exclude_columns]

# Exclude primn and secdf
feature_names = [name for name in feature_names if name not in ['primn', 'secdf']]

print(f"Number of training features: {len(feature_names)}")
print(f"Feature names: {feature_names}")

# =========================
# 4. Load environmental rasters and build the feature stack
# =========================
features_dict = {}

# Load existing environmental drivers
for name, tif_path in driver_tifs.items():
    try:
        with rasterio.open(tif_path) as src:
            if src.height == height and src.width == width:
                data = src.read(1)
            else:
                data = np.empty((height, width), dtype=np.float32)
                reproject(
                    source=rasterio.band(src, 1),
                    destination=data,
                    src_transform=src.transform,
                    src_crs=src.crs,
                    dst_transform=transform,
                    dst_crs=crs,
                    resampling=Resampling.nearest
                )
        features_dict[name] = data
        print(f"Loaded {name}, shape: {data.shape}")
    except Exception as e:
        print(f"Error loading {name}: {e}")
        features_dict[name] = np.full((height, width), np.nan, dtype=np.float32)

# Load LUH2 land-use rasters
print("Loading LUH2 raster files...")
luh2_files = [f for f in os.listdir(luh2_dir) if f.endswith('.tif')]
print(f"Found {len(luh2_files)} LUH2 raster files:")
for file in luh2_files:
    print(f"  - {file}")

for var in luh2_vars:
    if var in feature_names:
        matching_files = [f for f in luh2_files if f.startswith(f"luh2_{var}_") or var in f.lower()]
        if matching_files:
            tif_path = os.path.join(luh2_dir, matching_files[0])
            try:
                print(f"Loading: {matching_files[0]}")
                with rasterio.open(tif_path) as src:
                    if src.height == height and src.width == width:
                        data = src.read(1)
                    else:
                        data = np.empty((height, width), dtype=np.float32)
                        reproject(
                            source=rasterio.band(src, 1),
                            destination=data,
                            src_transform=src.transform,
                            src_crs=src.crs,
                            dst_transform=transform,
                            dst_crs=crs,
                            resampling=Resampling.nearest
                        )
                features_dict[var] = data
                print(f"Loaded LUH2 {var}, shape: {data.shape}")
            except Exception as e:
                print(f"Error loading LUH2 {var}: {e}")
                features_dict[var] = np.full((height, width), np.nan, dtype=np.float32)
        else:
            print(f"Missing raster for {var}; filling with NaN")
            features_dict[var] = np.full((height, width), np.nan, dtype=np.float32)
    else:
        print(f"Skipping {var}: not in feature list")

# Rasterize drainage density
try:
    drainage_gdf = gpd.read_file(drainage_gpkg)
    drainage_raster = rasterize(
        [(geom, value) for geom, value in zip(drainage_gdf.geometry, drainage_gdf[drainage_field])],
        out_shape=(height, width),
        transform=transform,
        fill=np.nan,
        all_touched=True
    )
    features_dict['Drainage_Density'] = drainage_raster
    print("Drainage density raster loaded")
except Exception as e:
    print(f"Error loading drainage density: {e}")
    features_dict['Drainage_Density'] = np.full((height, width), np.nan, dtype=np.float32)

# Load catchment area raster
try:
    with rasterio.open(sub_area_tif) as src:
        if src.height == height and src.width == width:
            sub_area_data = src.read(1)
        else:
            sub_area_data = np.empty((height, width), dtype=np.float32)
            reproject(
                source=rasterio.band(src, 1),
                destination=sub_area_data,
                src_transform=src.transform,
                src_crs=src.crs,
                dst_transform=transform,
                dst_crs=crs,
                resampling=Resampling.nearest
            )
    features_dict['Sub_area'] = sub_area_data
    print(f"Loaded Sub_area, shape: {sub_area_data.shape}")
except Exception as e:
    print(f"Error loading Sub_area: {e}")
    features_dict['Sub_area'] = np.full((height, width), np.nan, dtype=np.float32)

# Build feature stack in training feature order
features_list = []
for feature_name in feature_names:
    if feature_name in features_dict:
        features_list.append(features_dict[feature_name])
    else:
        print(f"Missing feature {feature_name}; filling with NaN")
        features_list.append(np.full((height, width), np.nan, dtype=np.float32))

features_stack = np.stack(features_list, axis=0)
print(f"Feature stack ready, shape: {features_stack.shape}")

# =========================
# 5. Train the random forest and predict
# =========================
y = df['elasticity']
X = df[feature_names]

rf = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
rf.fit(X, y)
joblib.dump(rf, os.path.join(out_dir, "rf_model_elasticity.pkl"))
print("RF model trained and saved")

# Predict in blocks
pred_map = np.full((height, width), np.nan, dtype=np.float32)
block_size = 500

for i in range(0, height, block_size):
    i_end = min(i + block_size, height)
    for j in range(0, width, block_size):
        j_end = min(j + block_size, width)

        block_features = features_stack[:, i:i_end, j:j_end]
        block_shape = block_features.shape[1:]
        X_block = block_features.reshape(block_features.shape[0], -1).T

        predictions_block = rf.predict(X_block)
        pred_block = predictions_block.reshape(block_shape)

        landmask_block = landmask[i:i_end, j:j_end]
        pred_block = pred_block * landmask_block

        pred_map[i:i_end, j:j_end] = pred_block

        print(f"Processed block: {i}-{i_end}, {j}-{j_end}")

# =========================
# 6. Save GeoTIFF and plot
# =========================

# Save prediction raster
profile.update(dtype=rasterio.float32, count=1, compress='LZW')
tif_path = os.path.join(out_dir, "global_elasticity_prediction.tif")
with rasterio.open(tif_path, 'w', **profile) as dst:
    dst.write(pred_map.astype(np.float32), 1)

# Custom green gradient, matching the original figure
base = plt.cm.get_cmap("YlGn")
green_cmap = LinearSegmentedColormap.from_list(
    "GreenGrad",
    base(np.linspace(0.15, 0.85, 256))
)

# =========================
# Plot with a horizontal colour bar
# =========================
plt.figure(figsize=(14, 7))
plt.imshow(
    pred_map,
    cmap=green_cmap,   # Original green colour scale
    vmin=0,
    vmax=np.nanpercentile(pred_map[~np.isnan(pred_map)], 99)
)
plt.axis('off')

cbar = plt.colorbar(
    orientation='horizontal',
    fraction=0.05,
    pad=0.04,
)
cbar.set_label("Runoff Elasticity", fontsize=14)

# Save figure as PNG
output_dir = str(FIGURE_DIR)
os.makedirs(output_dir, exist_ok=True)

plt.savefig(os.path.join(output_dir, "figure_09_global_rf_prediction.png"),
            dpi=300, bbox_inches='tight')

plt.close()
print("Figure 9 PNG saved")
