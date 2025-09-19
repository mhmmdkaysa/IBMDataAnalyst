import pandas as pd
import dash
# from dash import html # Dihapus karena sudah diimpor di bawah
from dash import dcc, html # Menggabungkan import dari dash
from dash.dependencies import Input, Output
# State dan no_update tidak digunakan, bisa dihapus jika mau
# import plotly.graph_objects as go 
import plotly.express as px
# import datetime as dt # Tidak digunakan secara langsung

# 1. PERBAIKAN: Impor yang lebih bersih

# Membuat aplikasi
app = dash.Dash(__name__)

# Hapus layout dan jangan tampilkan exception sampai callback dieksekusi
app.config.suppress_callback_exceptions = True

# Membaca data wildfire ke dalam pandas dataframe
df = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/Historical_Wildfires.csv')

# Ekstrak tahun dan bulan dari kolom tanggal
df['Month'] = pd.to_datetime(df['Date']).dt.month_name()
df['Year'] = pd.to_datetime(df['Date']).dt.year

# --- Bagian Layout dari Dash ---
app.layout = html.Div(children=[
    # Judul Dashboard
    html.H1('Australia Wildfire Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 26}),

    # Div luar untuk kontrol dan output
    html.Div([
        # Div untuk kontrol (Region dan Year)
        html.Div([
            # Kontrol untuk Region
            html.H2('Select Region:', style={'margin-right': '2em'}),
            dcc.RadioItems([
                {"label": "New South Wales", "value": "NSW"},
                {"label": "Northern Territory", "value": "NT"},
                {"label": "Queensland", "value": "QL"},
                {"label": "South Australia", "value": "SA"},
                {"label": "Tasmania", "value": "TA"},
                {"label": "Victoria", "value": "VI"},
                {"label": "Western Australia", "value": "WA"}
            ],
            value="NSW",  # Menetapkan value, bukan hanya string
            id='region',
            inline=True),
        ]),
        
        # Kontrol untuk Year
        html.Div([
            html.H2('Select Year:', style={'margin-right': '2em'}),
            dcc.Dropdown(df.Year.unique(), value=2005, id='year')
        ]),

        # 2. PERBAIKAN: Menghapus style yang error dan merapikan struktur Div
        # Div untuk menampung output plot
        html.Div([
            html.Div([], id='plot1'),
            html.Div([], id='plot2')
        ], style={'display': 'flex', 'flex-direction': 'row'}) # Contoh style yang benar
    ]),
])

# --- Bagian Callback ---
@app.callback(
    [Output(component_id='plot1', component_property='children'),
     Output(component_id='plot2', component_property='children')],
    [Input(component_id='region', component_property='value'),
     Input(component_id='year', component_property='value')]
)
def reg_year_display(input_region, input_year):
    # Filter data berdasarkan region dan tahun yang dipilih
    region_data = df[df['Region'] == input_region]
    y_r_data = region_data[region_data['Year'] == input_year]

    # Plot 1 - Rata-rata Area Kebakaran per Bulan (Pie Chart)
    est_data = y_r_data.groupby('Month')['Estimated_fire_area'].mean().reset_index()
    fig1 = px.pie(est_data, values='Estimated_fire_area', names='Month',
                  title=f"{input_region}: Monthly Average Estimated Fire Area in {input_year}")

    # Plot 2 - Rata-rata Jumlah Piksel per Bulan (Bar Chart)
    veg_data = y_r_data.groupby('Month')['Count'].mean().reset_index()
    fig2 = px.bar(veg_data, x='Month', y='Count',
                  title=f'{input_region}: Average Count of Pixels for Vegetation Fires in {input_year}')

    return [dcc.Graph(figure=fig1),
            dcc.Graph(figure=fig2)]

# --- Menjalankan Aplikasi ---
if __name__ == '__main__':
    # 3. PERBAIKAN: Menggunakan run_server dengan debug=True untuk pengembangan
    app.run(debug=True)