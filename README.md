# Global Runoff Elasticity

**Research code | Private working repository**

This repository contains Python scripts used to produce figures for a study of global runoff elasticity, its relationships with environmental drivers, seasonal variation, perturbation responses, and spatial prediction. The figure workflows draw on observations from **8,723 river catchments** and associated hydroclimatic, terrain, soil, and land-use datasets.

The repository currently includes **nine main-figure scripts** and **one supplementary-figure script**.

## Repository structure

```text
Global-Runoff-Elasticity/
├── scripts/                 # Python figure-generation scripts
├── data/
│   ├── processed/           # Local input CSV files (not committed)
│   └── raw/                 # Optional local raw data (not committed)
├── outputs/
│   ├── figures/             # Generated figure images
│   ├── results/             # Derived tables and GeoTIFF outputs
│   └── models/              # Model artefacts, where applicable
├── requirements.txt
└── README.md
```

> Some scripts reference large raster, NetCDF, or vector datasets at absolute paths on the author's computer. These paths must be updated to match your local data locations. The repository is not a self-contained data distribution.

## Figure scripts

| Figure | Script | Description |
| --- | --- | --- |
| Figure 1 | `scripts/figure_01_global_runoff_elasticity.py` | Spatial distribution of observed annual runoff elasticity |
| Figure 2 | `scripts/figure_02_seasonal_runoff_elasticity.py` | Seasonal runoff elasticity maps |
| Figure 3 | `scripts/figure_03_gam_environmental_drivers.py` | Univariate GAM relationships with environmental drivers |
| Figure 4 | `scripts/figure_04_gam_driver_importance.py` | Multivariable GAM driver importance |
| Figure 5 | `scripts/figure_05_seasonal_gam_relationships.py` | Seasonal univariate GAM relationships |
| Figure 6 | `scripts/figure_06_seasonal_gam_importance.py` | Seasonal GAM driver importance |
| Figure 7 | `scripts/figure_07_global_dominant_drivers.py` | Spatial patterns of dominant GAM factors |
| Figure 8 | `scripts/figure_08_gam_perturbation_maps.py` | Maps of precomputed GAM perturbation responses |
| Figure 9 | `scripts/figure_09_global_rf_prediction.py` | Random Forest prediction of global gridded runoff elasticity |
| Figure S1 | `scripts/supplementary_figure_s01_spatially_weighted_gam.py` | Spatially weighted GAM analysis |

## Installation

Create a Python environment and install the required packages:

```bash
python -m venv .venv
```

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Alternatively, install the dependencies from `requirements.txt` in an existing Conda environment.

## Data requirements

The scripts use processed catchment-level CSV files and, for some figures, additional geospatial inputs. Depending on the figure, these include climate reanalysis, precipitation, soil, terrain, land-use, and drainage datasets.

Place the required processed CSV files in `data/processed/`. Check the file paths near the beginning of each script and adjust any external input paths before running. See [`data/README.md`](data/README.md) for additional input guidance.

**Research input datasets are not included in this repository.** Their availability and redistribution permissions should be checked with the original providers.

## Running the figures

From the repository root, run a script using Python:

```bash
python scripts/figure_01_global_runoff_elasticity.py
python scripts/figure_09_global_rf_prediction.py
python scripts/supplementary_figure_s01_spatially_weighted_gam.py
```

Scripts may also be launched from Jupyter using the same Python environment. Generated PNG figures are intended to be stored in `outputs/figures/`, with derived results in `outputs/results/` and model files in their script-configured output directories.

For Figure 9, the script saves:

- `outputs/figures/figure_09_global_rf_prediction.png`
- `outputs/results/global_elasticity_prediction.tif`
- `outputs/results/rf_model_elasticity.pkl`

## Methods and interpretation notes

- The GAM figure scripts use different model specifications. Univariate and multivariable GAM results should not be interpreted as interchangeable.
- Figures 7 and S1 identify dominant factors using fitted model contributions; these are not causal attribution estimates.
- Figure 8 visualises precomputed perturbation results. Its upstream perturbation-generation workflow is not included in this figure-script collection.
- Figure 9 trains a Random Forest using catchment-level predictors and applies it to gridded environmental data. Consistent units, feature order, and temporal aggregation are essential. The figure script does not implement an independent spatial validation experiment.
- Figure 9 uses GPCC precipitation-data availability as a spatial mask, rather than a dedicated geographic land mask.

## Reproducibility status

All nine main figure scripts and the supplementary figure script have been run successfully in the author's local research environment. Successful execution does **not**, by itself, establish pixel-by-pixel agreement with previously produced figures or independent scientific validation. Exact reproduction requires the original input datasets, compatible package versions, and verification of the generated outputs.

## Repository status and citation

This is a **private working repository** for research code and manuscript-related figure generation. Please do not redistribute unpublished research materials or restricted datasets. Publication details, a formal citation, and an archival release can be added when appropriate.

## License

No open-source license has been selected. All rights reserved unless otherwise specified by the repository owner.
