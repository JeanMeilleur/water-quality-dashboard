import streamlit as st
import pandas as pd            # data manipulation
import plotly.express as px    # data visualization
from pathlib import Path       # safe file paths (works on Windows, Mac, Linux, and the cloud)

# to run: streamlit run app.py
# if it doesn't work, try: python -m streamlit run app.py

# ----------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------
st.set_page_config(
    page_title="Water Quality Dashboard",
    page_icon="💧",
    layout="wide"
)

# relative path -> works locally AND on Streamlit Community Cloud
DEFAULT_CSV = Path(__file__).parent / "data" / "biscayneBay_waterquality.csv"


# ----------------------------------------------------------
# DATA LOADING
# ----------------------------------------------------------
@st.cache_data
def load_data(source):
    """Read the CSV, clean the column names, parse the Time column."""
    df = pd.read_csv(source)
    df.columns = df.columns.str.strip()          # kill accidental spaces in headers

    if "Time" in df.columns:
        df["Time"] = pd.to_datetime(df["Time"], errors="coerce")

    return df


def numeric_columns(df):
    """Return only the columns that can actually be plotted on an axis."""
    return df.select_dtypes(include="number").columns.tolist()


# ----------------------------------------------------------
# HEADER
# ----------------------------------------------------------
st.title("💧 Water Quality Dashboard")
st.header("CIS 3590 - Internship-Ready Software Development")
st.subheader("Prof. Gregory Reis")

st.divider()


# ----------------------------------------------------------
# SIDEBAR - USER INPUT
# ----------------------------------------------------------
st.sidebar.header("File Upload")
st.sidebar.info("Upload a CSV file with water quality data, "
                "or leave empty to use the Biscayne Bay sample dataset.")

uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    df = load_data(uploaded_file)
    source_name = uploaded_file.name
else:
    df = load_data(DEFAULT_CSV)
    source_name = DEFAULT_CSV.name

num_cols = numeric_columns(df)

if not num_cols:
    st.error("This CSV has no numeric columns to plot. Upload a different file.")
    st.stop()

st.sidebar.divider()

# --- interactive widget: row range slider ---
st.sidebar.header("Filters")
row_range = st.sidebar.slider(
    "Select the range of readings to analyze",
    min_value=0,
    max_value=len(df) - 1,
    value=(0, len(df) - 1),
    step=1
)
df = df.iloc[row_range[0]:row_range[1] + 1]

# --- interactive widget: checkbox ---
show_stats = st.sidebar.checkbox("Show descriptive statistics", value=True)

st.sidebar.divider()
st.sidebar.caption(f"Loaded: **{source_name}**")
st.sidebar.caption(f"Rows in view: **{len(df)}**")


# ----------------------------------------------------------
# SECTIONS (TABS)
# ----------------------------------------------------------
overview, tables, plots, maps, insights = st.tabs([
    "Overview",
    "Data",
    "Charts",
    "Maps",
    "Insights"
])


# ----------------------------------------------------------
# OVERVIEW
# ----------------------------------------------------------
with overview:
    st.subheader("What this app does")
    st.write(
        "This dashboard lets you explore water quality readings collected by an "
        "autonomous surface vehicle in Biscayne Bay, Miami. Each row is a single "
        "sensor reading tagged with a timestamp and a GPS coordinate. "
        "Use the sidebar to upload your own CSV or to narrow the range of readings, "
        "then move through the tabs to inspect the raw data, plot any parameter, "
        "map the vehicle track, and read the automatic insights."
    )

    st.subheader("Dataset snapshot")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total readings", len(df))
    col2.metric("Columns", df.shape[1])
    col3.metric("Numeric parameters", len(num_cols))

    if "Time" in df.columns and df["Time"].notna().any():
        st.caption(
            f"Readings span from **{df['Time'].min()}** to **{df['Time'].max()}**."
        )

    st.subheader("How to use it")
    st.markdown(
        """
        1. **Sidebar** – upload a CSV or keep the default Biscayne Bay dataset.
        2. **Data** – view the raw table and pick which columns you want to see.
        3. **Charts** – choose any parameter and plot it over time or against another parameter.
        4. **Maps** – see where in the bay each reading was taken, colored by the parameter you pick.
        5. **Insights** – read the automatically generated summary of the filtered data.
        """
    )


# ----------------------------------------------------------
# DATA DISPLAY
# ----------------------------------------------------------
with tables:
    st.subheader("Raw Data")

    # --- interactive widget: multiselect ---
    selected_columns = st.multiselect(
        "Select the columns to display",
        options=df.columns.tolist(),
        default=df.columns.tolist()
    )

    if selected_columns:
        st.dataframe(df[selected_columns], use_container_width=True)
        st.caption("Raw data filtered by the columns and row range you selected.")
    else:
        st.warning("Select at least one column to display the table.")

    if show_stats:
        st.subheader("Descriptive Statistics")
        st.dataframe(df.describe(), use_container_width=True)
        st.caption(
            "Count, mean, standard deviation, min, quartiles and max "
            "for every numeric parameter in the current selection."
        )


# ----------------------------------------------------------
# CHARTS
# ----------------------------------------------------------
with plots:
    st.subheader("Line Chart - one parameter over time")

    parameter = st.selectbox(
        "Select a parameter",
        options=num_cols,
        index=0
    )

    x_axis = "Time" if "Time" in df.columns else df.index

    fig1 = px.line(
        df,
        x=x_axis,
        y=parameter,
        title=f"{parameter} over Time",
        labels={"Time": "Time of reading", parameter: parameter},
        markers=True
    )
    fig1.update_layout(
        xaxis_title="Time of reading",
        yaxis_title=parameter,
        legend_title_text="Parameter",
        hovermode="x unified"
    )
    st.plotly_chart(fig1, use_container_width=True)
    st.caption(
        f"Each point is one reading of **{parameter}**. "
        "Spikes or drops usually mean the vehicle crossed into a different water mass."
    )

    st.divider()

    st.subheader("Scatter Plot - compare two parameters")

    col_x, col_y, col_c = st.columns(3)
    with col_x:
        x_param = st.selectbox("X axis", options=num_cols, index=0, key="x_param")
    with col_y:
        y_param = st.selectbox(
            "Y axis",
            options=num_cols,
            index=1 if len(num_cols) > 1 else 0,
            key="y_param"
        )
    with col_c:
        color_param = st.selectbox(
            "Color by",
            options=num_cols,
            index=2 if len(num_cols) > 2 else 0,
            key="color_param"
        )

    fig2 = px.scatter(
        df,
        x=x_param,
        y=y_param,
        color=color_param,
        title=f"{x_param} vs {y_param}",
        labels={x_param: x_param, y_param: y_param, color_param: color_param},
        color_continuous_scale="viridis"
    )
    fig2.update_layout(
        xaxis_title=x_param,
        yaxis_title=y_param,
        legend_title_text=color_param,
        coloraxis_colorbar_title=color_param
    )
    st.plotly_chart(fig2, use_container_width=True)
    st.caption(
        f"The color scale on the right is the legend for **{color_param}**. "
        "A tight diagonal cloud means the two parameters move together."
    )

    st.divider()

    st.subheader("3D Visualization of the Bay Floor")

    if {"Longitude", "Latitude", "Total Water Column (m)"}.issubset(df.columns):
        depth_color = st.selectbox(
            "Color the bay floor by",
            options=num_cols,
            index=0,
            key="depth_color"
        )

        fig3 = px.scatter_3d(
            df,
            x="Longitude",
            y="Latitude",
            z="Total Water Column (m)",
            color=depth_color,
            title="3D Visualization of the Bay Floor",
            labels={
                "Longitude": "Longitude",
                "Latitude": "Latitude",
                "Total Water Column (m)": "Depth (m)"
            },
            color_continuous_scale="viridis"
        )
        fig3.update_scenes(zaxis_autorange="reversed")   # depth grows downward
        fig3.update_layout(legend_title_text=depth_color)
        st.plotly_chart(fig3, use_container_width=True)
        st.caption(
            "The Z axis is reversed so deeper readings sit lower, "
            "which makes the plot read like the actual bay floor."
        )
    else:
        st.info(
            "This chart needs the columns Longitude, Latitude and "
            "Total Water Column (m). They are not in the current dataset."
        )


# ----------------------------------------------------------
# MAPS
# ----------------------------------------------------------
with maps:
    st.subheader("Vehicle Track on a Map")

    if {"Latitude", "Longitude"}.issubset(df.columns):
        map_param = st.selectbox(
            "Color the track by",
            options=num_cols,
            index=0,
            key="map_param"
        )

        zoom_level = st.slider("Zoom level", min_value=10, max_value=18, value=16)

        first_map = px.scatter_map(
            df,
            lat="Latitude",
            lon="Longitude",
            title="Vehicle Track on a Map",
            center={
                "lat": float(df["Latitude"].mean()),
                "lon": float(df["Longitude"].mean())
            },
            zoom=zoom_level,
            color=map_param,
            color_continuous_scale="viridis",
            hover_data=num_cols[:4]
        )
        first_map.update_layout(
            legend_title_text=map_param,
            coloraxis_colorbar_title=map_param,
            margin={"r": 0, "t": 40, "l": 0, "b": 0}
        )
        st.plotly_chart(first_map, use_container_width=True)
        st.caption(
            f"Every dot is one reading, placed at the GPS coordinate where it was "
            f"taken and colored by **{map_param}**. The map is centered on the "
            "average position of the readings currently in view."
        )
    else:
        st.info("This map needs Latitude and Longitude columns in the dataset.")


# ----------------------------------------------------------
# INSIGHTS
# ----------------------------------------------------------
with insights:
    st.subheader("Automatic Insights")

    insight_param = st.selectbox(
        "Analyze a parameter",
        options=num_cols,
        index=0,
        key="insight_param"
    )

    series = df[insight_param].dropna()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Average", f"{series.mean():.2f}")
    col2.metric("Minimum", f"{series.min():.2f}")
    col3.metric("Maximum", f"{series.max():.2f}")
    col4.metric("Std. deviation", f"{series.std():.2f}")

    st.write(
        f"Across the **{len(series)}** readings currently selected, "
        f"**{insight_param}** averages **{series.mean():.2f}** and swings "
        f"between **{series.min():.2f}** and **{series.max():.2f}**. "
        f"A standard deviation of **{series.std():.2f}** tells you how stable "
        "the parameter was during the run: the smaller it is, the more uniform "
        "the water the vehicle passed through."
    )

    st.divider()

    st.subheader("Correlation between parameters")

    corr = df[num_cols].corr()

    fig4 = px.imshow(
        corr,
        text_auto=".2f",
        title="Correlation Matrix of Numeric Parameters",
        labels={"color": "Correlation"},
        color_continuous_scale="RdBu",
        zmin=-1,
        zmax=1
    )
    fig4.update_layout(
        xaxis_title="Parameter",
        yaxis_title="Parameter",
        coloraxis_colorbar_title="Correlation"
    )
    st.plotly_chart(fig4, use_container_width=True)
    st.caption(
        "Values near +1 (blue) move together, values near -1 (red) move in "
        "opposite directions, and values near 0 are unrelated. "
        "Temperature and salinity are the pair worth checking first."
    )