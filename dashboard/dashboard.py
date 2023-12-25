import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
merged_data = pd.read_csv("dashboard//main_data.csv")
merged_data['timestamp'] = pd.to_datetime(merged_data['timestamp'])

# Hitung rata-rata konsentrasi gas di seluruh stasiun
average_gas_concentration = merged_data[['SO2', 'NO2', 'CO', 'O3']].mean()

# Tampilkan rata-rata konsentrasi gas di seluruh stasiun menggunakan diagram batang (menggunakan Plotly Express)
fig_average_gas_concentration = px.bar(x=average_gas_concentration.index,
                                       y=average_gas_concentration.values,
                                       labels={'x': 'Gas', 'y': 'Rata-Rata Konsentrasi'},
                                       title='Rata-Rata Konsentrasi Gas di Seluruh Stasiun')

# Tampilkan plot menggunakan Streamlit
st.plotly_chart(fig_average_gas_concentration)

# Hitung total konsentrasi gas untuk setiap stasiun
total_gas_concentration_by_station = merged_data.groupby('station')[['SO2', 'NO2', 'CO', 'O3']].sum()

# Hitung total konsentrasi gas di seluruh stasiun
total_gas_concentration_all_stations = total_gas_concentration_by_station.sum(axis=1)

# Temukan stasiun dengan total konsentrasi gas terbesar
station_with_highest_total_pollution = total_gas_concentration_all_stations.idxmax()

# Tampilkan total konsentrasi gas di seluruh stasiun menggunakan diagram batang (menggunakan Plotly Express)
fig_total_gas_concentration = px.bar(x=total_gas_concentration_all_stations.index,
                                     y=total_gas_concentration_all_stations.values,
                                     labels={'x': 'Stasiun', 'y': 'Total Konsentrasi Gas'},
                                     title='Total Konsentrasi Gas di Seluruh Stasiun',
                                     color=total_gas_concentration_all_stations.values,
                                     color_continuous_scale='Viridis')

# Tampilkan plot menggunakan Streamlit
st.plotly_chart(fig_total_gas_concentration)

st.write(f"Stasiun dengan total konsentrasi gas terbesar: {station_with_highest_total_pollution}")

# Ekstrak jam dari timestamp
merged_data['hour'] = merged_data['timestamp'].dt.hour

# Opsi 1: Filter data berdasarkan stasiun yang dipilih oleh pengguna
selected_station = st.sidebar.selectbox('Pilih Stasiun', merged_data['station'].unique())
wanshouxigong_data = merged_data[merged_data['station'] == selected_station]

# Pilih kolom yang akan divisualisasikan (contoh: CO)
selected_column = 'CO'

# Temukan jam dengan konsentrasi maksimum untuk stasiun yang dipilih
max_hour_per_station = wanshouxigong_data.groupby(['hour'])[selected_column].idxmax()
max_hour_data = wanshouxigong_data.loc[max_hour_per_station]

# Visualisasi jam dengan konsentrasi maksimum menggunakan Plotly Express
fig_max_hour_concentration = px.line(max_hour_data, x='hour', y=selected_column,
                                     labels={'hour': 'Jam', selected_column: f'Konsentrasi {selected_column}'},
                                     title=f'Jam dengan Konsentrasi Maksimum {selected_column} di Stasiun {selected_station}',
                                     line_shape='linear', render_mode='auto')

# Tampilkan plot menggunakan Streamlit
st.plotly_chart(fig_max_hour_concentration)

# Opsi 2: Ekstrak tahun
merged_data['year'] = merged_data['timestamp'].dt.year
selected_value = 'year'

# Temukan jam atau tahun dengan konsentrasi maksimum untuk stasiun yang dipilih
max_value_per_station = wanshouxigong_data.groupby([selected_value])[selected_column].idxmax()
max_value_data = wanshouxigong_data.loc[max_value_per_station]

# Visualisasi jam atau tahun dengan konsentrasi maksimum menggunakan Plotly Express
fig_max_value_year = px.line(max_value_data, x=selected_value, y=selected_column,
                             labels={selected_value: selected_value.capitalize(),
                                     selected_column: f'Konsentrasi {selected_column}'},
                             title=f'{selected_value.capitalize()} dengan Konsentrasi Maksimum {selected_column} di Stasiun {selected_station}')

# Tampilkan plot menggunakan Streamlit
st.plotly_chart(fig_max_value_year)

# Opsi 3: Ekstrak bulan
merged_data['month'] = merged_data['timestamp'].dt.month
selected_value = 'month'

# Temukan jam atau bulan dengan konsentrasi maksimum untuk stasiun yang dipilih
max_value_per_station = wanshouxigong_data.groupby([selected_value])[selected_column].idxmax()
max_value_data = wanshouxigong_data.loc[max_value_per_station]

# Visualisasi jam atau bulan dengan konsentrasi maksimum menggunakan Plotly Express
fig_max_value_month = px.line(max_value_data, x=selected_value, y=selected_column,
                              labels={selected_value: selected_value.capitalize(),
                                      selected_column: f'Konsentrasi {selected_column}'},
                              title=f'{selected_value.capitalize()} dengan Konsentrasi Maksimum {selected_column} di Stasiun {selected_station}')

# Tampilkan plot menggunakan Streamlit
st.plotly_chart(fig_max_value_month)
