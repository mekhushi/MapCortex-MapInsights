import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import os

st.set_page_config(
    page_title="DataMap",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.sidebar.title("🗺 DataMap Dashboard")
st.sidebar.markdown("Interactive data visualization with charts & dataset summary")
st.sidebar.markdown("---")

page = st.sidebar.selectbox(
    "📄 Select Page",
    ["Home", "Charts & Analytics", "Dataset Summary", "About / Help"]
)

st.sidebar.subheader("📂 Upload CSV")
uploaded_file = st.sidebar.file_uploader("Choose CSV file", type=["csv"])
df = None
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.sidebar.success(f"Loaded {df.shape[0]} rows × {df.shape[1]} columns")

numeric_filters = {}
cat_filters = {}

if df is not None:
    with st.sidebar.expander("🔍 Filter Data", expanded=False):
        numeric_cols = df.select_dtypes(include='number').columns.tolist()
        cat_cols = df.select_dtypes(include='object').columns.tolist()

        if numeric_cols:
            st.markdown("**Numeric Filters**")
            for col in numeric_cols:
                min_val, max_val = round(float(df[col].min()), 2), round(float(df[col].max()), 2)
                if min_val != max_val:
                    numeric_filters[col] = st.slider(f"{col}", min_val, max_val, (min_val, max_val))
                else:
                    st.write(f"{col} has a single value: {min_val}")
                    numeric_filters[col] = (min_val, max_val)

        if cat_cols:
            st.markdown("**Categorical Filters**")
            for col in cat_cols:
                options = df[col].dropna().unique().tolist()
                cat_filters[col] = st.multiselect(f"{col}", options, default=options)

        apply_filters = st.button("Apply Filters")

st.sidebar.markdown("---")
st.sidebar.subheader("ℹ About / Help")
st.sidebar.info("Upload CSV → Filter → Visualize charts & dataset summary")

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

if page == "Home":
    st.title("🏠 Welcome to DataMap")
    img_path = os.path.join("assets", "pexels-pixabay-265087.jpg")
    if os.path.exists(img_path):
        img = Image.open(img_path)
        st.image(img, use_container_width=True)
    else:
        st.warning("Home page image not found. Place image in the `assets` folder.")

    st.markdown("""
    Interactive dashboard to visualize numeric data and gain insights.

    **Features**:
    - Dynamic numeric & categorical filters
    - Charts & analytics
    - Dataset summary
    """)

    if df is not None:
        with st.expander("Preview Data (first 10 rows)", expanded=True):
            st.dataframe(df.head(10))

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
    st.title("ℹ About DataMap")
    st.markdown("""
    **DataMap** is an interactive dashboard for numeric data visualization.

    - Upload CSV files and explore datasets
    - Apply dynamic numeric and categorical filters
    - Visualize data through interactive charts
    - Quickly gain insights from your data
    """)

