import pandas as pd
import plotly.express as px
import streamlit as st

# Load the data
data = pd.read_csv('dataset.csv')  # Replace with your actual file name

# Data Cleaning and Transformation
data['jumlah_kg'] = data['jumlah_kg'].astype(float)
data['nama_provinsi'] = data['nama_provinsi'].astype(str)
data['nama_kabupaten_kota'] = data['nama_kabupaten_kota'].astype(str)

# Grouping data by provinces
province_summary = data.groupby("nama_provinsi")["jumlah_kg"].sum().reset_index()

# Streamlit Dashboard Setup
st.title("Interactive Data Visualization Dashboard")

# Interactive Bar Chart - Total Kilograms by Province
st.header("Total Kilograms by Province")
fig_province = px.bar(
    province_summary,
    x="nama_provinsi",
    y="jumlah_kg",
    labels={"jumlah_kg": "Total Kilograms", "nama_provinsi": "Province"},
    title="Total Kilograms by Province",
    template="plotly_white"
)
st.plotly_chart(fig_province)

# Filter Data by Province
st.sidebar.header("Filter Options")
selected_province = st.sidebar.selectbox(
    "Select Province", options=data['nama_provinsi'].unique()
)

filtered_data = data[data['nama_provinsi'] == selected_province]

# Detailed View by Regency/City in Selected Province
st.header(f"Kilograms by Regency/City in {selected_province}")
fig_city = px.bar(
    filtered_data,
    x="nama_kabupaten_kota",
    y="jumlah_kg",
    labels={"jumlah_kg": "Kilograms", "nama_kabupaten_kota": "Regency/City"},
    title=f"Kilograms by Regency/City in {selected_province}",
    template="plotly_white"
)
st.plotly_chart(fig_city)

# Optional: Geographic Map Visualization (requires actual coordinates)
if 'latitude' in data.columns and 'longitude' in data.columns:
    st.header("Geographic Map of Selected Province")
    map_fig = px.scatter_geo(
        filtered_data,
        lat='latitude',
        lon='longitude',
        text='nama_kabupaten_kota',
        size='jumlah_kg',
        title=f"Geographic Map of {selected_province}",
        template="plotly_white",
        projection="mercator"
    )
    st.plotly_chart(map_fig)
else:
    st.write("No geographic coordinates found in the dataset for mapping.")
