from utils import *
from data import *

st.title(APP_NAME)
st.header(POST_RACE_HEADER)

#Fastest Lap Distribution - Histogram showing when drivers set their fastest laps
#Gap Analysis - Waterfall chart showing time gaps between positions
#DNF Analysis - Bar chart of incomplete races
#Performance vs Weather - Scatter plot correlating lap times with track temperature

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
# POST-EVENT ANALYSIS VISUALIZATIONS
# ============================================================================

def create_fastest_lap_distribution():
    """7. Fastest Lap Distribution by Lap Number"""
    results_df['FL_LAPNUM'] = pd.to_numeric(results_df['FL_LAPNUM'], errors='coerce')
    
    fig = go.Figure(go.Histogram(
        x=results_df['FL_LAPNUM'].dropna(),
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

def create_gap_analysis():
    """8. Gap to Winner Analysis"""
    completed_laps = results_df[results_df['LAPS'] == 23].copy()
    completed_laps['GAP_SECONDS'] = completed_laps['GAP_FIRST'].apply(
        lambda x: laptime_to_seconds(x) if isinstance(x, str) and ':' in str(x) else 0
    )
    
    fig = go.Figure(go.Waterfall(
        x=[f"P{i}" for i in range(1, len(completed_laps) + 1)],
        y=[0] + completed_laps['GAP_SECONDS'].diff().fillna(0).tolist()[1:],
        text=[f"Car #{num}" for num in completed_laps['NUMBER']],
        textposition="outside",
        connector={"line": {"color": "rgb(63, 63, 63)"}},
        decreasing={"marker": {"color": "lightgreen"}},
        increasing={"marker": {"color": "salmon"}},
        totals={"marker": {"color": "blue"}}
    ))
    
    fig.update_layout(
        title="Cumulative Gap Between Positions",
        xaxis_title="Position",
        yaxis_title="Gap Increment (seconds)",
        height=600,
        showlegend=False
    )
    
    return fig

def create_dnf_analysis():
    """9. DNF and Completion Analysis"""
    results_df['COMPLETED'] = results_df['LAPS'].apply(lambda x: 'Completed' if x == 23 else 'DNF')
    dnf_data = results_df[results_df['COMPLETED'] == 'DNF'].copy()
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=[f"Car #{num}" for num in dnf_data['NUMBER']],
        y=dnf_data['LAPS'],
        marker_color='coral',
        text=dnf_data['LAPS'],
        textposition='outside',
        name='Laps Completed'
    ))
    
    fig.add_hline(y=23, line_dash="dash", line_color="green", 
                  annotation_text="Full Race Distance (23 laps)")
    
    fig.update_layout(
        title="DNF Analysis - Laps Completed",
        xaxis_title="Car Number",
        yaxis_title="Laps Completed",
        height=500,
        showlegend=False
    )
    
    return fig

def create_performance_vs_weather():
    """10. Lap Time vs Track Temperature"""
    # Merge lap data with weather (approximate by time)
    analysis_df['ELAPSED_SECONDS'] = analysis_df['ELAPSED'].apply(laptime_to_seconds)
    
    # Get top 5 drivers average lap times per lap
    top_5 = results_df.nsmallest(5, 'POSITION')['NUMBER'].tolist()
    lap_temps = []
    
    for lap_num in range(1, 24):
        lap_data = analysis_df[
            (analysis_df['LAP_NUMBER'] == lap_num) & 
            (analysis_df['NUMBER'].isin(top_5)) &
            (analysis_df['LAP_TIME_SECONDS'] < 150)
        ]
        if len(lap_data) > 0:
            avg_time = lap_data['LAP_TIME_SECONDS'].mean()
            # Get approximate track temp for this lap
            weather_idx = min(lap_num, len(weather_df) - 1)
            track_temp = weather_df.iloc[weather_idx]['TRACK_TEMP']
            lap_temps.append({'lap': lap_num, 'avg_time': avg_time, 'track_temp': track_temp})
    
    df_temp = pd.DataFrame(lap_temps)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df_temp['track_temp'],
        y=df_temp['avg_time'],
        mode='markers',
        marker=dict(
            size=12,
            color=df_temp['lap'],
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title="Lap Number")
        ),
        text=[f"Lap {lap}" for lap in df_temp['lap']],
        hovertemplate='Track Temp: %{x:.1f}°C<br>Avg Lap Time: %{y:.2f}s<br>%{text}<extra></extra>'
    ))
    
    # Add trend line
    z = np.polyfit(df_temp['track_temp'], df_temp['avg_time'], 1)
    p = np.poly1d(z)
    fig.add_trace(go.Scatter(
        x=df_temp['track_temp'],
        y=p(df_temp['track_temp']),
        mode='lines',
        line=dict(color='red', dash='dash'),
        name='Trend'
    ))
    
    fig.update_layout(
        title="Average Lap Time vs Track Temperature (Top 5 Drivers)",
        xaxis_title="Track Temperature (°C)",
        yaxis_title="Average Lap Time (seconds)",
        height=600,
        showlegend=True
    )
    
    return fig