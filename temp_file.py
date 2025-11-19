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