from utils import *
from data import *

st.title(APP_NAME)
st.header(DRIVER_HEADER)

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

# Data clean up
analysis_df['LAP_TIME_SECONDS'] = analysis_df['LAP_TIME'].apply(laptime_to_seconds)
analysis_df['S1_SECONDS'] = analysis_df['S1_SECONDS'].astype(float)
analysis_df['S2_SECONDS'] = analysis_df['S2_SECONDS'].astype(float)
analysis_df['S3_SECONDS'] = analysis_df['S3_SECONDS'].astype(float)
best_laps_df['AVERAGE'] = best_laps_df['AVERAGE'].apply(laptime_to_seconds)

def create_lap_time_consistency():
    """1. Lap Time Consistency Analysis"""
    # Filter out outliers (first lap, pit laps)
    clean_data = analysis_df[
        (analysis_df['LAP_NUMBER'] > 1) & 
        (analysis_df['LAP_TIME_SECONDS'].notna()) &
        (analysis_df['LAP_TIME_SECONDS'] < 150) &
        (analysis_df['LAP_TIME_SECONDS'] > 110)
    ].copy()
    
    # Get top 10 finishers
    top_10 = result_official_df.nsmallest(10, 'POSITION')['NUMBER'].tolist()
    clean_data = clean_data[clean_data['NUMBER'].isin(top_10)]
    
    fig = go.Figure()
    
    for num in top_10:
        driver_data = clean_data[clean_data['NUMBER'] == num]
        if len(driver_data) > 0:  # Check if there's data
            fig.add_trace(go.Box(
                y=driver_data['LAP_TIME_SECONDS'],
                name=f"Car #{num}",
                boxmean='sd'
            ))
    
    fig.update_layout(
        title="Lap Time Consistency - Top 10 Finishers",
        yaxis_title="Lap Time (seconds)",
        xaxis_title="Car Number",
        height=600,
        showlegend=False,
        hovermode='x unified'
    )
    
    return fig

def create_sector_heatmap():
    """2. Sector Performance Heatmap"""
    # Calculate average sector times for top 15
    top_15 = result_official_df.nsmallest(15, 'POSITION')['NUMBER'].tolist()
    clean_data = analysis_df[
        (analysis_df['LAP_NUMBER'] > 5) & 
        (analysis_df['NUMBER'].isin(top_15))
    ].copy()
    
    sector_avg = clean_data.groupby('NUMBER').agg({
        'S1_SECONDS': 'mean',
        'S2_SECONDS': 'mean',
        'S3_SECONDS': 'mean'
    }).round(3)
    
    fig = go.Figure(data=go.Heatmap(
        z=sector_avg.values,
        x=['Sector 1', 'Sector 2', 'Sector 3'],
        y=[f"Car #{num}" for num in sector_avg.index],
        colorscale='RdYlGn_r',
        text=sector_avg.values,
        texttemplate='%{text:.3f}s',
        textfont={"size": 10},
        colorbar=dict(title="Avg Time (s)")
    ))
    
    fig.update_layout(
        title="Average Sector Times - Top 15 Drivers",
        xaxis_title="Sector",
        yaxis_title="Driver",
        height=700
    )
    
    return fig

def create_pace_evolution():
    """3. Pace Evolution Throughout Race"""
    top_5 = result_official_df.nsmallest(5, 'POSITION')['NUMBER'].tolist()
    
    fig = go.Figure()
    
    colors = px.colors.qualitative.Set1
    
    for idx, num in enumerate(top_5):
        driver_data = analysis_df[
            (analysis_df['NUMBER'] == num) & 
            (analysis_df['LAP_NUMBER'] > 1) &
            (analysis_df['LAP_TIME_SECONDS'] < 150)
        ].sort_values('LAP_NUMBER')
        
        fig.add_trace(go.Scatter(
            x=driver_data['LAP_NUMBER'],
            y=driver_data['LAP_TIME_SECONDS'],
            mode='lines+markers',
            name=f"Car #{num}",
            line=dict(width=2, color=colors[idx]),
            marker=dict(size=6)
        ))
    
    fig.update_layout(
        title="Lap Time Evolution - Top 5 Finishers",
        xaxis_title="Lap Number",
        yaxis_title="Lap Time (seconds)",
        height=600,
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    return fig

def create_best_laps_comparison():
    """4. Best 10 Laps Average Comparison (Horizontal Bar Chart)"""
    top_15 = best_laps_df.nsmallest(15, 'AVERAGE')
    
    # 1. FIX: Reverse the order of the DataFrame so the fastest car (smallest average)
    #    appears at the top of the horizontal bar chart.
    top_15 = top_15.iloc[::-1] 
    
    # Calculate time in seconds for plotting
    average_seconds = top_15['AVERAGE'].apply(laptime_to_seconds)
    
    fig = go.Figure(go.Bar(
        # Y-axis (vertical) is Driver number
        y=[f"Car #{num}" for num in top_15['NUMBER']],
        # X-axis (horizontal) is Average time in seconds
        x=average_seconds,
        orientation='h', 
        # Display the original time string on the bars
        text=top_15['AVERAGE'],
        textposition='outside'
    ))
    
    fig.update_layout(
        title="Average of Best 10 Laps - Top 15 Drivers",
        # X-AXIS FIX: Reverse the X-axis so that smaller/faster times are visually to the right
        xaxis_title="Average Time (seconds) - Lower is Faster",
        yaxis_title="Driver",
        xaxis=dict(autorange="reversed"),
        height=600,
        showlegend=False
    )
    
    return fig

def create_performance_frontier():
    """5. Driver DNA - Performance Frontier (Corner Entry vs. Exit)"""
    # Filter for 'Good/Fast' laps (GF)
    df_gf = analysis_df[analysis_df['FLAG_AT_FL'] == 'GF'].copy()

    # Define the micro-sectors
    CORNER_ENTRY = 'IM1a_time'
    CORNER_EXIT = 'IM1_time'

    # Convert time strings to seconds using the available laptime_to_seconds function
    for col in [CORNER_ENTRY, CORNER_EXIT]:
        # This will create 'IM1a_time_S' and 'INT_1_time_S'
        df_gf.loc[:, col + '_S'] = df_gf[col].apply(laptime_to_seconds)

    # Filter for necessary columns and drop rows where time conversion failed
    df_pf_dna = df_gf[['NUMBER', CORNER_ENTRY + '_S', CORNER_EXIT + '_S']].dropna()
    
    # Create Plotly Express Scatter Plot
    fig = px.scatter(
        df_pf_dna,
        x=CORNER_ENTRY + '_S',
        y=CORNER_EXIT + '_S',
        # Color by Car Number (as a categorical variable)
        color=df_pf_dna['NUMBER'].astype(str),
        opacity=0.6,
        hover_name=df_pf_dna['NUMBER'].apply(lambda x: f"Car #{x}"),
        hover_data={
            'NUMBER': False,
            CORNER_ENTRY + '_S': ':.3f',
            CORNER_EXIT + '_S': ':.3f',
        },
        labels={
            CORNER_ENTRY + '_S': 'Corner Entry Time (IM1a Time)',
            CORNER_EXIT + '_S': 'Corner Exit Time (IM1 Time)',
            'color': 'Car Number'
        }
    )

    fig.update_layout(
        title="Driver DNA - Performance Frontier (Corner Entry vs. Exit)",
        xaxis_title="Corner Entry Time (IM1a Time - Lower is Faster)",
        yaxis_title="Corner Exit Time (IM1 Time - Lower is Faster)",
        height=600,
        # Invert Y-axis as lower time is faster (common for racing data)
        yaxis=dict(autorange="reversed"),
        legend_title="Car Number"
    )
    
    return fig

def create_micro_sector_heatmap():
    """7. Average Micro-Sector Performance Heatmap (Cornering DNA)"""
    df_gf = analysis_df[analysis_df['FLAG_AT_FL'] == 'GF'].copy()
    
    # Use top 15 drivers, consistent with the existing sector heatmap
    top_15 = result_official_df.nsmallest(15, 'POSITION')['NUMBER'].tolist()
    df_gf = df_gf[df_gf['NUMBER'].isin(top_15)].copy()

    # Define the micro-sectors from the original radar chart logic
    micro_sectors_t = ['IM1a_time', 'IM1_time', 'IM2a_time', 'IM2_time', 'IM3a_time']
    df_dna = df_gf[['NUMBER'] + micro_sectors_t].copy()
    
    ms_cols_s = []
    for col in micro_sectors_t:
        new_col = col + '_S'
        # Convert micro-sector times to seconds
        df_dna.loc[:, new_col] = df_dna[col].apply(laptime_to_seconds)
        ms_cols_s.append(new_col)
    
    # Calculate average micro-sector time per driver
    df_avg = df_dna.groupby('NUMBER')[ms_cols_s].mean().round(3).dropna()
    
    # Rename columns for clear axis labels
    column_mapping = {col: col.replace('_time_S', '').replace('_time', '') for col in ms_cols_s}
    df_avg.rename(columns=column_mapping, inplace=True)
    
    fig = go.Figure(data=go.Heatmap(
        z=df_avg.values,
        x=df_avg.columns.tolist(),
        y=[f"Car #{num}" for num in df_avg.index],
        # 'RdYlGn_r' is reversed: Red is slow, Green is fast (lower time)
        colorscale='RdYlGn_r', 
        text=df_avg.values,
        texttemplate='%{text:.3f}s',
        textfont={"size": 10},
        colorbar=dict(title="Avg Time (s)")
    ))
    
    fig.update_layout(
        title="Average Micro-Sector Times - Top 15 Drivers (Cornering Performance)",
        xaxis_title="Micro-Sector",
        yaxis_title="Driver",
        height=700,
        xaxis=dict(tickangle=-45)
    )
    
    return fig

def create_pace_ema_comparison(alpha=0.2):
    """8. Pace Trend Comparison (EMA) - Top 5 Finishers"""
    
    top_5 = result_official_df.nsmallest(5, 'POSITION')['NUMBER'].tolist()
    
    # Filter data for top 5 drivers and clean up lap times
    df_trend = analysis_df[
        analysis_df['NUMBER'].isin(top_5) &
        (analysis_df['FLAG_AT_FL'] == 'GF') &
        (analysis_df['LAP_NUMBER'] > 2) & # Start after pit exit/early laps
        (analysis_df['LAP_TIME_SECONDS'].notna())
    ].copy()

    fig = go.Figure()
    colors = px.colors.qualitative.Set1
    
    for idx, num in enumerate(top_5):
        df_driver = df_trend[df_trend['NUMBER'] == num].sort_values('LAP_NUMBER')
        
        if len(df_driver) > 0:
            # Calculate Exponentially Smoothed Lap Time (EMA)
            df_driver.loc[:, 'LAP_TIME_EMA'] = df_driver['LAP_TIME_SECONDS'].ewm(alpha=alpha, adjust=False).mean()
            
            # 1. Plot Actual Lap Times (as light markers for context)
            fig.add_trace(go.Scatter(
                x=df_driver['LAP_NUMBER'],
                y=df_driver['LAP_TIME_SECONDS'],
                mode='markers',
                marker=dict(color=colors[idx % len(colors)], opacity=0.3, size=4),
                name=f"Car #{num} (Actual)",
                showlegend=False, # Hide actual lap times from legend
                hovertemplate="Lap %{x}<br>Actual Time: %{y:.3f}s<extra></extra>"
            ))

            # 2. Plot EMA trend line (prominent line)
            fig.add_trace(go.Scatter(
                x=df_driver['LAP_NUMBER'],
                y=df_driver['LAP_TIME_EMA'],
                mode='lines',
                name=f"Car #{num} (EMA, $\\alpha={alpha}$)",
                line=dict(width=3, color=colors[idx % len(colors)]),
                hovertemplate="Lap %{x}<br>EMA Time: %{y:.3f}s<extra></extra>"
            ))

    fig.update_layout(
        title=f"Pace Trend Comparison (Exponential Moving Average) - Top 5 Finishers",
        xaxis_title="Lap Number",
        yaxis_title="Lap Time (seconds)",
        height=600,
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    return fig


fig1 = create_lap_time_consistency()
st.plotly_chart(fig1)
fig2 = create_sector_heatmap()
st.plotly_chart(fig2)
fig3 = create_pace_evolution()
st.plotly_chart(fig3)
fig4 = create_best_laps_comparison()
st.plotly_chart(fig4)
fig5 = create_performance_frontier()
st.plotly_chart(fig5)
fig6 = create_micro_sector_heatmap()
st.plotly_chart(fig6)
fig7 = create_pace_ema_comparison()
st.plotly_chart(fig7)

