import pandas as pd

def detect_lat_lon_columns(df):
    lat_candidates = ["lat", "latitude", "Lat", "Latitude"]
    lon_candidates = ["lon", "lng", "long", "longitude", "Lon", "Longitude"]

    lat_col = None
    lon_col = None

    for col in df.columns:
        if col in lat_candidates:
            lat_col = col
        if col in lon_candidates:
            lon_col = col

    return lat_col, lon_col

def generate_filters(df, lat_col, lon_col):
    filter_cols = [col for col in df.columns if col not in [lat_col, lon_col]]

    for col in filter_cols:
        if df[col].dtype == "object":
            options = st.multiselect(f"Filter {col}", df[col].unique())
            if options:
                df = df[df[col].isin(options)]
        else:
            min_val = float(df[col].min())
            max_val = float(df[col].max())
            selected = st.slider(f"Range for {col}", min_val, max_val, (min_val, max_val))
            df = df[(df[col] >= selected[0]) & (df[col] <= selected[1])]

    return df
