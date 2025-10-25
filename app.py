import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster, HeatMap
from streamlit_folium import st_folium
import plotly.express as px

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="MapCortex",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- SIDEBAR ---
st.sidebar.title("🗺 MapCortex Dashboard")
st.sidebar.markdown("Interactive data visualization with maps & charts")
st.sidebar.markdown("---")

# Page navigation
page = st.sidebar.selectbox("📄 Select Page", ["Home", "Map View", "Charts & Analytics", "Dataset Summary", "About / Help"])

# Dataset upload
st.sidebar.subheader("📂 Upload CSV")
uploaded_file = st.sidebar.file_uploader("Choose CSV file", type=["csv"])
df = None
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.sidebar.success(f"Loaded {df.shape[0]} rows × {df.shape[1]} columns")

# Filters (collapsible)
if df is not None:
    with st.sidebar.expander("🔍 Filter Data", expanded=False):
        numeric_cols = df.select_dtypes(include='number').columns.tolist()
        cat_cols = df.select_dtypes(include='object').columns.tolist()

        numeric_filters = {}
        cat_filters = {}

        if numeric_cols:
            st.markdown("**Numeric Filters**")
            for col in numeric_cols:
                min_val, max_val = float(df[col].min()), float(df[col].max())
                numeric_filters[col] = st.slider(f"{col}", min_val, max_val, (min_val, max_val))

        if cat_cols:
            st.markdown("**Categorical Filters**")
            for col in cat_cols:
                options = df[col].dropna().unique().tolist()
                cat_filters[col] = st.multiselect(f"{col}", options, default=options)

        apply_filters = st.button("Apply Filters")

st.sidebar.markdown("---")
st.sidebar.subheader("ℹ About / Help")
st.sidebar.info("Upload CSV → Filter → Visualize maps & charts")

# --- FILTER FUNCTION ---
def filter_dataframe(df):
    filtered_df = df.copy()
    for col, val in numeric_filters.items():
        filtered_df = filtered_df[(filtered_df[col] >= val[0]) & (filtered_df[col] <= val[1])]
    for col, val in cat_filters.items():
        filtered_df = filtered_df[filtered_df[col].isin(val)]
    return filtered_df

if df is not None and 'apply_filters' in locals() and apply_filters:
    df = filter_dataframe(df)
    st.success(f"Filtered data: {df.shape[0]} rows × {df.shape[1]} columns")

# --- PAGE CONTENT ---
if page == "Home":
    st.title("🏠 Welcome to MapCortex")
    from PIL import Image
    img = Image.open(r"C:\Users\Khushi Singh\Desktop\MapCortex\assets\pexels-pixabay-265087.jpg")
    st.image(img, use_container_width=True)

    st.markdown("""
    Interactive dashboard to visualize geospatial and numeric data.

    **Features**:
    - Maps with clustering & heatmaps
    - Dynamic filters (numeric + categorical)
    - Charts & analytics
    - Dataset summary
    """)
    if df is not None:
        with st.expander("Preview Data (first 10 rows)", expanded=True):
            st.dataframe(df.head(10))

elif page == "Map View":
    st.title("🗺 Map View")
    if df is not None:
        if 'latitude' in df.columns and 'longitude' in df.columns:
            map_center = [df['latitude'].mean(), df['longitude'].mean()]

            st.subheader("Map with Marker Clustering")
            m = folium.Map(location=map_center, zoom_start=5)
            MarkerCluster(df[['latitude', 'longitude']].values.tolist()).add_to(m)
            st_folium(m, width=900, height=500)

            st.subheader("Heatmap")
            hm = folium.Map(location=map_center, zoom_start=5)
            HeatMap(df[['latitude', 'longitude']].values.tolist()).add_to(hm)
            st_folium(hm, width=900, height=500)
        else:
            st.warning("Dataset must have 'latitude' and 'longitude' columns for maps.")
    else:
        st.info("Upload a CSV file to visualize maps.")

elif page == "Charts & Analytics":
    st.title("📊 Charts & Analytics")
    if df is not None and numeric_cols:
        col1, col2 = st.columns(2)
        with col1:
            x_axis = st.selectbox("X-axis", numeric_cols)
        with col2:
            y_axis = st.selectbox("Y-axis", numeric_cols)

        fig = px.scatter(df, x=x_axis, y=y_axis, color=numeric_cols[0])
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Histogram")
        hist_col = st.selectbox("Select column for histogram", numeric_cols, key="hist")
        fig_hist = px.histogram(df, x=hist_col)
        st.plotly_chart(fig_hist, use_container_width=True)
    else:
        st.info("Upload CSV with numeric columns for charts.")

elif page == "Dataset Summary":
    st.title("📄 Dataset Summary")
    if df is not None:
        with st.expander("Preview first 50 rows", expanded=True):
            st.dataframe(df.head(50))

        st.subheader("Columns & Types")
        st.dataframe(pd.DataFrame(df.dtypes, columns=["Type"]))

        st.subheader("Statistics")
        st.dataframe(df.describe())

        st.subheader("Missing Values")
        st.dataframe(df.isnull().sum())
    else:
        st.info("Upload CSV to see summary.")

elif page == "About / Help":
    st.title("ℹ About MapCortex")
    st.markdown("""
    **MapCortex** is a Streamlit app for interactive geospatial & numeric data visualization.

    - Upload CSV files
    - Filter data dynamically
    - Explore maps, heatmaps, charts, and summaries
    """)
