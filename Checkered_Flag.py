from utils import *
from data import *

st.title(APP_NAME)
st.header(POST_RACE_HEADER)

with st.sidebar:
        racename_options = st.selectbox('Race Track',RACE_TRACK_NAME)
        race_number_options=st.selectbox("Race Number",RACE_NUMBERS)

        # Get data
        data_info = select_race(racename_options,race_number_options)
        analysis_df = data_info[0] 
        best_laps_df = data_info[1] 
        lap_ms_df = data_info[2]
        weather_df = data_info[3] 
        lap_end_df = data_info[4]
        result_provisional_df = data_info[5]
        result_provisional_class_df = data_info[6]
        result_official_df = data_info[7]
        result_official_class_df = data_info[8]
        lap_start_df = data_info[9]

# Data clean up
analysis_df['LAP_TIME_SECONDS'] = analysis_df['LAP_TIME'].apply(laptime_to_seconds)
analysis_df['S1_SECONDS'] = analysis_df['S1_SECONDS'].astype(float)
analysis_df['S2_SECONDS'] = analysis_df['S2_SECONDS'].astype(float)
analysis_df['S3_SECONDS'] = analysis_df['S3_SECONDS'].astype(float)
best_laps_df['AVERAGE'] = best_laps_df['AVERAGE'].apply(laptime_to_seconds)

#Fastest Lap Distribution - Histogram showing when drivers set their fastest laps
def create_fastest_lap_distribution():
    """Fastest Lap Distribution by Lap Number"""
    result_official_df['FL_LAPNUM'] = pd.to_numeric(result_official_df['FL_LAPNUM'], errors='coerce')
    
    fig = go.Figure(go.Histogram(
        x=result_official_df['FL_LAPNUM'].dropna(),
        nbinsx=23,
        marker_color='indianred',
        opacity=0.75
    ))
    
    fig.update_layout(
        title="When Did Drivers Set Their Fastest Lap?",
        xaxis_title="Lap Number",
        yaxis_title="Number of Drivers",
        height=500,
        bargap=0.1
    )
    
    return fig

#DNF Analysis - Bar chart of incomplete races
def create_dnf_analysis():
    """9. DNF and Completion Analysis (Dynamic Race Distance)"""
    
    total_race_laps = result_official_df['LAPS'].max()
    df_res = result_official_df.copy()
    
    # Define 'Completed' as finishing the total race laps (or close to it, depending on rules, but here we use max)
    df_res['COMPLETED'] = df_res['LAPS'].apply(lambda x: 'Completed' if x >= total_race_laps else 'DNF')
    
    dnf_data = df_res[df_res['COMPLETED'] == 'DNF'].copy()
    
    fig = go.Figure()
    
    if dnf_data.empty:
        fig.add_annotation(text="No DNFs (All cars completed full distance)", 
                           xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False)
    else:
        fig.add_trace(go.Bar(
            x=[f"Car #{num}" for num in dnf_data['NUMBER']],
            y=dnf_data['LAPS'],
            marker_color='coral',
            text=dnf_data['LAPS'],
            textposition='outside',
            name='Laps Completed'
        ))
    
    fig.add_hline(y=total_race_laps, line_dash="dash", line_color="green", 
                  annotation_text=f"Full Race Distance ({total_race_laps} laps)")
    
    fig.update_layout(
        title=f"DNF Analysis - Cars Not Completing {total_race_laps} Laps",
        xaxis_title="Car Number",
        yaxis_title="Laps Completed",
        height=500,
        showlegend=False
    )
    
    return fig


def create_top_finishers(N_drivers=5):
    """Top N Race Finishers"""
    # Filter for the Top 10 positions
    df_top = result_official_df[result_official_df['POSITION'] <= N_drivers].copy()
    
    # Sort by Position so #1 is at the top (after we reverse the axis)
    df_top = df_top.sort_values('POSITION', ascending=True)
    
    # Convert 'TOTAL_TIME' to seconds for the bar length logic
    # (Uses the existing 'laptime_to_seconds' function defined in your code)
    df_top['TOTAL_TIME_SECONDS'] = df_top['TOTAL_TIME'].apply(laptime_to_seconds)
    
    fig = go.Figure(go.Bar(
        x=df_top['TOTAL_TIME_SECONDS'],
        # Create a descriptive Y-axis label combining Position and Car Number
        y=[f"P{pos} - Car #{num}" for pos, num in zip(df_top['POSITION'], df_top['NUMBER'])],
        orientation='h',
        text=df_top['TOTAL_TIME'], # Display the formatted time string on the bar
        textposition='auto',
        marker_color='royalblue'
    ))
    
    fig.update_layout(
        title=f"Top {N_drivers} Race Finishers",
        xaxis_title="Total Time (Seconds)",
        yaxis_title="Position - Car Number",
        height=600,
        # Reverse Y-axis so Position 1 is at the top
        yaxis=dict(autorange="reversed")
    )
    
    return fig

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


def _prepare_weather_lap_data():
    """Helper: Prepares and merges lap and weather data for models (Viz 2 and Viz 4 Residuals)."""
    
    # 1. Prepare average weather data (Track Temp)
    df_weather_clean = weather_df[['TIME_UTC_STR', 'TRACK_TEMP']].dropna().copy()
    # Assuming 'TIME_UTC_STR' is parsable to extract HH:MM for merge
    try:
        df_weather_clean['TIME_KEY'] = df_weather_clean['TIME_UTC_STR'].apply(
            lambda x: datetime.strptime(str(x).split(' ')[1], '%H:%M:%S').strftime('%H:%M')
        )
    except:
        # Fallback for different time formats
        df_weather_clean['TIME_KEY'] = df_weather_clean['TIME_UTC_STR'].apply(
            lambda x: str(x).split(' ')[-1][:5] if pd.notna(x) else np.nan
        )

    df_avg_weather = df_weather_clean.groupby('TIME_KEY')['TRACK_TEMP'].mean().reset_index()

    # 2. Prepare lap data
    df_lap_data = analysis_df[['NUMBER', 'LAP_NUMBER', 'FLAG_AT_FL', 'HOUR', 'LAP_TIME_SECONDS']].copy()
    df_lap_data = df_lap_data.rename(columns={'LAP_TIME_SECONDS': 'LAP_TIME_S'})
    
    try:
        df_lap_data.loc[:, 'HOUR_KEY'] = df_lap_data['HOUR'].apply(
            lambda x: datetime.strptime(str(x).split(' ')[-1].split('.')[0], '%H:%M:%S').strftime('%H:%M') if pd.notna(x) else np.nan
        )
    except:
        df_lap_data.loc[:, 'HOUR_KEY'] = df_lap_data['HOUR'].apply(
            lambda x: str(x).split(' ')[-1][:5] if pd.notna(x) else np.nan
        )

    # 3. Final Merge and Filter
    df_model_data = pd.merge(df_lap_data, df_avg_weather, left_on='HOUR_KEY', right_on='TIME_KEY', how='left')
    df_model_data = df_model_data[
        (df_model_data['FLAG_AT_FL'] == 'GF') & 
        (df_model_data['LAP_NUMBER'] > 2)
    ].dropna(subset=['LAP_TIME_S', 'TRACK_TEMP']).copy()
    
    return df_model_data

try:
    fig1 = create_weather_timeline()
    st.plotly_chart(fig1)
except Exception as e:
    st.error(f"Error loading Weather Conditions Timeline: {e}")

# Wind Polars
try:
    fig2 = create_wind_polar()
    st.plotly_chart(fig2)
except Exception as e:
    st.error(f"Error loading Wind Polar Plot: {e}")

try:
    fig3 = create_top_finishers(N_drivers=5)
    st.plotly_chart(fig3)
except Exception as e:
    st.error(f"Error loading top finishers: {e}")

try:
    fig4 = create_fastest_lap_distribution()
    st.plotly_chart(fig4)
except Exception as e:
    st.error(f"Error loading fastest lap: {e}")

try:
    fig5 = create_dnf_analysis()
    st.plotly_chart(fig5)
except Exception as e:
    st.error(f"Error loading DNF analysis: {e}")

