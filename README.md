# 📈 Dashboard Ekonomi & Politik Provinsi (Demo)

## About Project

This dashboard is an interactive demo to explore the relationship between **economic indicators** and **political indicators** at the provincial level.

Built with **Streamlit** and **Plotly**, this project aims to:

- Visualize how **GDP per capita**, **unemployment rate**, and **inflation** vary across provinces.
- Compare **trust in government** and **political participation index** between provinces and across years.
- Provide simple **time series views** (e.g., 2023 vs 2024) for each province.
- Serve as a **portfolio project** to demonstrate skills in:
  - Data cleaning & merging (ekonomi + politik dalam satu file gabungan)
  - Exploratory Data Analysis (EDA)
  - Interactive dashboard development with Streamlit

Main features:

- 🔀 Dataset selector (gabungan / ekonomi / politik)
- 📊 Bar charts per province (per year or compared across years)
- ⏱️ Time series charts by province (economic & political indicators)
- 🧭 Sidebar controls for year and province filtering


## About Dataset

The dashboard uses a combined dataset that contains both **economic** and **political** variables for each province and year.

Example columns:

- **Key identifiers**
  - `tahun` – year (e.g. 2023, 2024)
  - `provinsi` – province name

- **Economic indicators**
  - `gdp_per_capita` – GDP per capita for each province
  - `tingkat_pengangguran` – unemployment rate (in %)
  - `inflasi` – inflation rate (in %)

- **Political indicators**
  - `trust_government` – index of citizens’ trust in government (e.g. scale 0–100)
  - `political_participation_index` – index of political participation (e.g. scale 0–100)

The data has been:

- Cleaned and merged from separate economic and political sources into **one unified CSV file**.
- Structured to support:
  - Comparison across provinces for a given year.
  - Comparison across years (2023 vs 2024) for a given province.
  - Combined analysis of economic and political indicators in the same view.


### Link Demo: https://dashboardidn-demo.streamlit.app/
