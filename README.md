# 💧 Water Quality Dashboard

An interactive Streamlit dashboard for exploring water quality readings collected by an
autonomous surface vehicle in Biscayne Bay, Miami.

**Live app:** https://YOUR-APP-NAME.streamlit.app
**Repository:** https://github.com/YOUR-USERNAME/water-quality-dashboard

Built for CIS 3590 – Internship-Ready Software Development (Prof. Gregory Reis),
Florida International University.

---

## Purpose

Raw sensor CSVs are unreadable. This app turns them into something a non-technical
user can actually interrogate: filter the readings, pick any parameter, see it
plotted over time, compare two parameters against each other, map where each reading
was taken, and get a plain-English summary of what the numbers say.

---

## Dataset

**File:** `data/biscayneBay_waterquality.csv`
**Source:** water quality survey of Biscayne Bay, Miami, FL, collected by an
autonomous surface vehicle.

Each row is one timestamped sensor reading. Typical columns:

| Column | Description |
|---|---|
| `Time` | Timestamp of the reading |
| `Latitude` / `Longitude` | GPS position of the vehicle |
| `Temperature (c)` | Water temperature in Celsius |
| `Salinity (ppt)` | Salinity in parts per thousand |
| `Total Water Column (m)` | Depth of the water column in meters |
| `ODO (mg/L)` | Optical dissolved oxygen |
| `pH` | Acidity of the water |

You can also upload your own CSV from the sidebar. Any numeric column is
automatically detected and made available in every chart.

---

## Features

- **CSV upload** – use the bundled dataset or bring your own
- **Row-range slider** – narrow the analysis to a slice of the run
- **Column multiselect** – choose which columns appear in the data table
- **Dynamic Plotly charts** – line chart, scatter plot, and 3D bay-floor plot, all
  driven by dropdowns, with titles, axis labels, and legends
- **Interactive map** – vehicle track plotted on a real map, colored by any parameter
- **Insights tab** – automatic summary statistics and a correlation matrix

---

## Running it locally

```bash
git clone https://github.com/YOUR-USERNAME/water-quality-dashboard.git
cd water-quality-dashboard

python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS / Linux:
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

If `streamlit run` is not recognized, use:

```bash
python -m streamlit run app.py
```

The app opens at http://localhost:8501

---

## User instructions

1. Open the app. The Biscayne Bay dataset loads automatically.
2. **Sidebar** – upload your own CSV, or drag the slider to narrow the range of
   readings. Toggle the descriptive statistics on or off.
3. **Overview** – read what the dataset contains and how many readings are in view.
4. **Data** – pick the columns you care about and inspect the raw table.
5. **Charts** – choose a parameter for the line chart; choose X, Y, and a color
   parameter for the scatter plot.
6. **Maps** – pick what to color the vehicle track by and adjust the zoom.
7. **Insights** – pick a parameter to see its summary stats, and read the
   correlation matrix to spot which parameters move together.

---

## Project management

This project was built using AGILE. The product backlog, sprint breakdown, daily
standup log, and retrospective are documented in [`docs/AGILE.md`](docs/AGILE.md),
and tracked on the repository's GitHub Projects board and Issues.

---

## Tech stack

Python · Streamlit · pandas · Plotly Express · GitHub · Streamlit Community Cloud