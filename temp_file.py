import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np

# Load the data files
# Note: Update these paths to match your file locations
results_df = pd.read_csv('03_Results_Anonymized.CSV', sep=';')
analysis_df = pd.read_csv('23_AnalysisEnduranceWithSections_Race 1_Anonymized.CSV', sep=';')
weather_df = pd.read_csv('26_Weather_Race 1_Anonymized.CSV', sep=';')
best_laps_df = pd.read_csv('99_Best 10 Laps By Driver_Race 1_Anonymized.CSV', sep=';')

# Clean column names (remove spaces)
analysis_df.columns = analysis_df.columns.str.strip()
weather_df.columns = weather_df.columns.str.strip()
results_df.columns = results_df.columns.str.strip()

# Convert lap times to seconds for analysis
def laptime_to_seconds(laptime_str):
    """Convert lap time string (MM:SS.mmm) to seconds"""
    try:
        if pd.isna(laptime_str) or laptime_str == '0' or laptime_str == '':
            return None
        parts = str(laptime_str).split(':')
        if len(parts) == 2:
            minutes = int(parts[0])
            seconds = float(parts[1])
            return minutes * 60 + seconds
        return float(laptime_str)
    except:
        return None

# Apply conversion
analysis_df['LAP_TIME_SECONDS'] = analysis_df['LAP_TIME'].apply(laptime_to_seconds)
analysis_df['S1_SECONDS'] = analysis_df['S1_SECONDS'].astype(float)
analysis_df['S2_SECONDS'] = analysis_df['S2_SECONDS'].astype(float)
analysis_df['S3_SECONDS'] = analysis_df['S3_SECONDS'].astype(float)



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

# ============================================================================
# GENERATE ALL VISUALIZATIONS
# ============================================================================

if __name__ == "__main__":
    print("Generating Racing Data Visualizations...")
    

    
    fig4 = create_best_laps_comparison()
    fig4.write_html("4_best_laps_comparison.html")
    print("✓ Best 10 Laps Comparison")
    
    # Pre-Event Analysis
    print("\n=== PRE-EVENT ANALYSIS ===")
    fig5 = create_weather_timeline()
    fig5.write_html("5_weather_timeline.html")
    print("✓ Weather Timeline")
    
    fig6 = create_wind_polar()
    fig6.write_html("6_wind_polar.html")
    print("✓ Wind Polar Plot")
    
    # Post-Event Analysis
    print("\n=== POST-EVENT ANALYSIS ===")
    fig7 = create_fastest_lap_distribution()
    fig7.write_html("7_fastest_lap_distribution.html")
    print("✓ Fastest Lap Distribution")
    
    fig8 = create_gap_analysis()
    fig8.write_html("8_gap_analysis.html")
    print("✓ Gap Analysis")
    
    fig9 = create_dnf_analysis()
    fig9.write_html("9_dnf_analysis.html")
    print("✓ DNF Analysis")
    
    fig10 = create_performance_vs_weather()
    fig10.write_html("10_performance_vs_weather.html")
    print("✓ Performance vs Weather")
    
    print("\n✅ All visualizations generated successfully!")
    print("HTML files saved in current directory.")