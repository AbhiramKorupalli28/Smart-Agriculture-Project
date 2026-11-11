# Raw data sources

## Executed datasets

1. `crop_prediction_india.csv` — 49,999 rows, 10 columns, 4,121,879 bytes. Publicly available in the GitHub repository [Crop-Yield-Prediction-based-on-Indian-Agriculture](https://github.com/AbhishekKandoi/Crop-Yield-Prediction-based-on-Indian-Agriculture). Fields: state, district, year, season, crop, temperature, humidity, soil moisture, area, production. The repository states that the data is used for Indian crop prediction; the file is included in the repository under its published terms.
2. `crop_recommendation.csv` — 2,200 rows, 8 columns, 150,034 bytes. Same repository. Fields: N, P, K, temperature, humidity, pH, rainfall, and crop label. Used for crop classification and clustering experiments.

## Investigated but not downloaded in this environment

- CATCrops primary dataset: Kaggle reports a 32.49 GB dataset with 332k files and 5.64m columns. It contains Sentinel-2 L2A time series, parcel shapefiles, parcel metadata, mappings, and HDF5 files. Download requires Kaggle access/API credentials or browser download.
- Cornell/ICRISAT District-Level Database: 571 districts, 20 Indian states, 1966–2020, 74 datasets, 1,030 variables, and more than 11 million data points. Use the project page for access instructions.
- DES Agriculture APY reports: official Government of India area, production, and yield reporting portal.
- FAOSTAT: international production statistics covering food and agriculture domains. Use the official download interface for bulk files.

No simulated records are included in the executed analysis.
