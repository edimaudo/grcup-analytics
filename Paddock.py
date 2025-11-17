from utils import *
from data import *

st.title(APP_NAME)
st.header(PRE_RACE_HEADER)


# side bar here
with st.sidebar:
        racename_options = st.selectbox('Race Track',RACE_TRACK_NAME)
        race_number_options=st.selectbox("Race Number",RACE_NUMBERS)

# Get data
data_info = select_race(racename_options,race_number_options)
## output order --> file_analysis, file_best10, final_lap_ms, file_weather, file_lap_end, 
#                   file_result_provisional,file_result_provisional_class, 
##                  file_results_official,file_results_official_class, file_lap_start


analysis_df = data_info[0] ## analysis_df = pd.read_csv('23_AnalysisEnduranceWithSections_Race 1_Anonymized.CSV', sep=';')
best_laps_df = data_info[1] ## = pd.read_csv('99_Best 10 Laps By Driver_Race 1_Anonymized.CSV', sep=';')
lap_ms_df = data_info[2]
weather_df = data_info[3] ##= pd.read_csv('26_Weather_Race 1_Anonymized.CSV', sep=';')
lap_end_df = data_info[4]
result_provisional_df = data_info[5]
result_provisional_class_df = data_info[6]
result_official_df = data_info[7]
result_official_class_df = data_info[8]
lap_start_df = data_info[9]

# ============================================================================
# PRE-EVENT ANALYSIS VISUALIZATIONS
# ============================================================================

def create_weather_timeline():
    """5. Weather Conditions Timeline"""
    weather_df['TIME'] = pd.to_datetime(weather_df['TIME_UTC_STR'])
    
    fig = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        subplot_titles=('Temperature', 'Humidity & Pressure', 'Wind Speed'),
        vertical_spacing=0.08
    )
    
    # Temperature
    fig.add_trace(go.Scatter(
        x=weather_df['TIME'], y=weather_df['AIR_TEMP'],
        name='Air Temp', line=dict(color='orange', width=2)
    ), row=1, col=1)
    
    fig.add_trace(go.Scatter(
        x=weather_df['TIME'], y=weather_df['TRACK_TEMP'],
        name='Track Temp', line=dict(color='red', width=2)
    ), row=1, col=1)
    
    # Humidity & Pressure
    fig.add_trace(go.Scatter(
        x=weather_df['TIME'], y=weather_df['HUMIDITY'],
        name='Humidity', line=dict(color='blue', width=2),
        yaxis='y3'
    ), row=2, col=1)
    
    fig.add_trace(go.Scatter(
        x=weather_df['TIME'], y=weather_df['PRESSURE'],
        name='Pressure', line=dict(color='purple', width=2),
        yaxis='y4'
    ), row=2, col=1)
    
    # Wind Speed
    fig.add_trace(go.Scatter(
        x=weather_df['TIME'], y=weather_df['WIND_SPEED'],
        name='Wind Speed', line=dict(color='green', width=2),
        fill='tozeroy'
    ), row=3, col=1)
    
    fig.update_yaxes(title_text="Temperature (°C)", row=1, col=1)
    fig.update_yaxes(title_text="Humidity (%)", row=2, col=1)
    fig.update_yaxes(title_text="Wind Speed (km/h)", row=3, col=1)
    fig.update_xaxes(title_text="Time", row=3, col=1)
    
    fig.update_layout(
        height=900,
        title_text="Weather Conditions During Race",
        showlegend=True,
        hovermode='x unified'
    )
    
    return fig

def create_wind_polar():
    """6. Wind Speed & Direction Polar Plot"""
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=weather_df['WIND_SPEED'],
        theta=weather_df['WIND_DIRECTION'],
        mode='markers',
        marker=dict(
            size=10,
            color=weather_df['WIND_SPEED'],
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title="Wind Speed<br>(km/h)")
        ),
        text=weather_df['TIME_UTC_STR'],
        hovertemplate='Wind Speed: %{r:.2f} km/h<br>Direction: %{theta}°<br>%{text}<extra></extra>'
    ))
    
    fig.update_layout(
        title="Wind Speed and Direction Pattern",
        polar=dict(
            radialaxis=dict(title="Wind Speed (km/h)", angle=90),
            angularaxis=dict(direction="clockwise", rotation=90)
        ),
        height=700
    )
    
    return fig