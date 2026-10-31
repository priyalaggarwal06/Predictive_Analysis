# Punjab Monsoon Rainfall Analysis

A five-objective machine-learning project using IMD subdivision rainfall data. It studies Punjab's June–September (JJAS) rainfall using rainfall data from Punjab and seven neighbouring subdivisions.

## Live Demo

[Open the Punjab Monsoon Rainfall Dashboard]https://predictiveanalysis-1.streamlit.app/

## Project objectives

| # | Objective | Method | Purpose |
|---|---|---|---|
| 1 | Rainfall estimation | Multiple Linear Regression and degree-2 Polynomial Regression | Estimate Punjab JJAS rainfall using rainfall from seven neighbouring subdivisions. |
| 2 | Drought detection | RBF Support Vector Machine (SVM) | Classify drought and non-drought years. A drought year has Punjab JJAS rainfall below the 25th percentile. |
| 3 | Rainfall-pattern clustering | K-Means (`k=4`) and hierarchical clustering | Group subdivisions by average monthly rainfall patterns and inspect the dendrogram. |
| 4 | Improved prediction | Decision Tree, Random Forest (bagging), and Gradient Boosting | Compare model performance and examine feature importance. |
| 5 | PCA and neural network | PCA (7 features to 3 components) and MLP | Test whether reducing the input features affects prediction performance. |

## Recorded results

These are results from the project's current test split. Results may differ if the data or test split changes.

| Objective | Recorded result |
|---|---|
| 1 | Multiple Linear Regression: R² ≈ 0.573, MAE ≈ 71.9 mm. The degree-2 Polynomial model performed worse on this split. |
| 2 | SVM accuracy ≈ 0.739. The confusion matrix should also be checked because drought recall was low. |
| 3 | K-Means produced four clusters for the 36 subdivisions. The dendrogram provides a hierarchical clustering comparison. |
| 4 | Random Forest: R² ≈ 0.572, MAE ≈ 70.4 mm; Gradient Boosting: R² ≈ 0.558; single Decision Tree: R² ≈ −0.222. |
| 5 | PCA (3 components) + MLP: R² ≈ 0.494; MLP without PCA: R² ≈ −0.342. |

A negative R² means that, on this test split, the model performed worse than predicting the test-set average. These are retrospective educational results, not official rainfall or drought forecasts.

## Recommended project structure

```text
punjab_rainfall_project/
├── data/
│   ├── raw/                         # Original IMD CSV
│   └── processed/
│       ├── cleaned_rainfall.csv
│       ├── punjab_dataset.csv       # Punjab + seven neighbours
│       └── subdivision_pattern.csv  # 36 subdivisions × 12 months
├── models/                          # Trained models and comparison CSV files
├── reports/
│   └── figures/                     # EDA and objective plots
├── notebooks/                       # EDA and objective notebooks
├── objectives/                      # Objective Python scripts, if used
├── streamlit_app/
│   └── app.py                       # Dashboard source code
├── punjab_data_prep.py
├── requirements.txt
└── README.md
```

The dashboard also supports the earlier layout: `data/punjab_dataset.csv` and figures in `images/`. Model files should be in the project-level `models/` folder.

Important model and result files:

```text
models/obj1_linear.pkl
models/obj1_poly.pkl
models/obj1_comparison.csv
models/obj2_svm.pkl
models/obj3_kmeans_clusters.csv
models/obj4_decision.pkl
models/obj4_random.pkl
models/obj4_gradient.pkl
models/obj4_comparison.csv
models/obj5_mlp_no_pca.pkl
models/obj5_mlp_pca.pkl
models/obj5_comparison.csv
```

Expected dashboard figures include:

```text
obj1_actual_vs_pred.png
obj2_svm_cm.png
obj3_kmeans_pattern.png
obj3_dendrogram.png
obj4_ensemble_compare.png
obj4_feature_importance.png
obj5_pca_variance.png
obj5_mlp_compare.png
```

Put the figures in `reports/figures/` or, for the earlier layout, in `images/`.

## Install dependencies

Open a terminal in the project folder. On Windows, use PowerShell:

```powershell
py -m pip install -r requirements.txt
```

This installs the packages listed in `requirements.txt`, including Streamlit if it is listed there. To install Streamlit separately:

```powershell
py -m pip install streamlit
```

If the `py` command is not available, use `python -m pip` instead.

## Prepare data and train models

Run these commands from the project root, using the filenames and folders in your project:

```powershell
py punjab_data_prep.py
py objectives/objective1_estimation.py
py objectives/objective2_svm_drought.py
py objectives/objective3_clustering.py
py objectives/objective4_randomforest.py
py objectives/objective5_pca_mlp.py
```

The preparation script creates the Punjab JJAS dataset and the monthly subdivision-pattern dataset. The objective scripts train and save models, comparison tables, and figures. If your input data is not in the path expected by a script, update that path first.

## Run the dashboard

After installing Streamlit, run this command from the project root:

```powershell
py -m streamlit run streamlit_app/app.py
```

Streamlit will display a local address, usually `http://localhost:8501`. Open that address in your browser. To stop the app, press **Ctrl+C** in the terminal.

The dashboard presents the five objectives, plots, model-result tables, and an expandable interactive estimator. The estimator uses whichever of these trained models are available:

```text
obj1_linear.pkl
obj4_random.pkl
obj5_mlp_pca.pkl
obj2_svm.pkl
```

If a graph or results table is missing, check that the file exists in the expected folder and its filename matches the name used by the app. If a model file is missing, run its objective script first.

## Data and interpretation notes

- The prediction target is Punjab JJAS rainfall in millimetres.
- The seven input features are JJAS rainfall for Haryana, Himachal Pradesh, Jammu & Kashmir, West Rajasthan, East Rajasthan, West Uttar Pradesh, and Uttarakhand.
- The current drought threshold is approximately **349.1 mm**, the 25th percentile of Punjab JJAS rainfall.
- The models use historical data and should be treated as educational estimates, not operational forecasts.
- For drought detection, review precision, recall, and the confusion matrix—not accuracy alone.