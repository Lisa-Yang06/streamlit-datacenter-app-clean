# Data Center Site Selection & Optimization Model

## Overview

This project develops a hybrid machine learning framework for U.S. county-level data center site selection. It jointly models economic profitability and environmental sustainability, enabling data-driven infrastructure planning through predictive modeling and multi-objective optimization.

## Problem Statement

Data center deployment requires balancing financial viability with environmental responsibility. This project addresses the trade-off by:

- Predicting county-level profitability
- Quantifying environmental suitability
- Enabling interactive weight-based decision exploration

## Data & Scale

- Geographic resolution: U.S. county level
- Data sources: energy grid composition, land cover, climate metrics, infrastructure variables, economic indicators
- Integrated multi-source geospatial datasets
- Scalable to thousands of county-level observations

## Machine Learning Framework

- Supervised learning models:
  - Random Forest
  - XGBoost
  - Logistic Regression
  - Support Vector Machines
- Active learning for improved label efficiency
- SHAP-based feature importance analysis for interpretability
- Cross-model comparison for predictive robustness

## Methodology

1. Geospatial data scraping and preprocessing (GeoPandas, Selenium)
2. Feature engineering and normalization
3. Model training and evaluation
4. Multi-objective weighted scoring
5. Interactive visualization via Streamlit dashboard

## Interactive Application

Built a Streamlit web application with dynamic geospatial visualization (Folium), allowing users to:

- Adjust weights between profitability and environmental suitability
- View real-time county-level composite scores
- Explore trade-offs across the U.S. map

## Impact

- Demonstrates integration of geospatial analytics with machine learning
- Provides interpretable, decision-support modeling for large-scale infrastructure placement
- Enables transparent trade-off analysis between sustainability and profitability

## Tech Stack

Python · GeoPandas · Pandas · NumPy · XGBoost · Scikit-learn · SHAP · Selenium · Streamlit · Folium
