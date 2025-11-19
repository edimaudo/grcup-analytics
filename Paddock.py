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
        RACE_CAR_DRIVERS = result_official_df['NUMBER']
        race_car_driver_options = st.selectbox("Race card driver",RACE_CAR_DRIVERS)

# Data clean up
analysis_df['LAP_TIME_SECONDS'] = analysis_df['LAP_TIME'].apply(laptime_to_seconds)
analysis_df['S1_SECONDS'] = analysis_df['S1_SECONDS'].astype(float)
analysis_df['S2_SECONDS'] = analysis_df['S2_SECONDS'].astype(float)
analysis_df['S3_SECONDS'] = analysis_df['S3_SECONDS'].astype(float)
best_laps_df['AVERAGE'] = best_laps_df['AVERAGE'].apply(laptime_to_seconds)

def create_pace_degradation_comparison(N_drivers=5):
    """Pace Degradation Model - Lap Time vs Lap Number (Top N Comparison)"""
    
    # Get top N drivers to focus the comparison
    top_drivers = result_official_df.nsmallest(N_drivers, 'POSITION')['NUMBER'].tolist()
    
    df_pace_gf = analysis_df[
        (analysis_df['FLAG_AT_FL'] == 'GF') & 
        (analysis_df['LAP_NUMBER'] > 2) &
        (analysis_df['NUMBER'].isin(top_drivers))
    ].dropna(subset=['LAP_TIME_SECONDS']).copy()
    df_pace_gf = df_pace_gf.rename(columns={'LAP_TIME_SECONDS': 'LAP_TIME_S'})

    fig = go.Figure()
    colors = px.colors.qualitative.Plotly
    
    for idx, driver in enumerate(top_drivers):
        df_driver = df_pace_gf[df_pace_gf['NUMBER'] == driver].copy()
        
        if len(df_driver) >= 5: # Need at least 5 points for a reliable fit
            X = df_driver['LAP_NUMBER'].values.reshape(-1, 1)
            y = df_driver['LAP_TIME_S'].values
            
            model = LinearRegression()
            model.fit(X, y)
            deg_rate = model.coef_[0] * 1000 # ms per lap

            # 1. Line Plot (Degradation Model) - Prominent trend line only
            fig.add_trace(go.Scatter(
                x=df_driver['LAP_NUMBER'], 
                y=model.predict(X),
                mode='lines',
                line=dict(color=colors[idx % len(colors)], width=3),
                name=f'Car #{driver} Fit (+{deg_rate:.1f} ms/lap)',
                hovertemplate="Lap %{x}<br>Fit Time: %{y:.3f}s<extra></extra>"
            ))
            
    fig.update_layout(
        title=f'Pace Degradation Model - Lap Time Fall-off (Top {N_drivers} Drivers)',
        xaxis_title='Lap Number',
        yaxis_title='Lap Time (Seconds) - Lower is Faster',
        height=600,
        hovermode='x unified'
    )
    return fig

def create_coeff_field_rank():
    """Tire Degradation Rate (Horizontal Bar Chart)"""
    
    deg_coefficients = {}
    df_pace_gf = analysis_df[(analysis_df['FLAG_AT_FL'] == 'GF') & (analysis_df['LAP_NUMBER'] > 2)].dropna(subset=['LAP_TIME_SECONDS']).copy()
    df_pace_gf = df_pace_gf.rename(columns={'LAP_TIME_SECONDS': 'LAP_TIME_S'})

    for driver in df_pace_gf['NUMBER'].unique():
        df_driver = df_pace_gf[df_pace_gf['NUMBER'] == driver]
        if len(df_driver) >= 5:
            X = df_driver['LAP_NUMBER'].values
            y = df_driver['LAP_TIME_S'].values
            slope, _, _, _, _ = linregress(X, y)
            deg_coefficients[driver] = slope * 1000 # Degradation rate in ms/lap

    df_coeff = pd.Series(deg_coefficients).to_frame(name='Deg_Rate_ms_per_lap')
    # Sort by fastest (smallest) degradation rate first, then reverse for plotting
    df_coeff = df_coeff.sort_values(by='Deg_Rate_ms_per_lap', ascending=True).iloc[::-1]

    fig = go.Figure(go.Bar(
        y=[f"Car #{num}" for num in df_coeff.index],
        x=df_coeff['Deg_Rate_ms_per_lap'],
        orientation='h',
        marker_color=np.where(df_coeff['Deg_Rate_ms_per_lap'] > 0, 'lightcoral', 'lightgreen'),
        text=[f'{r:.1f} ms/lap' for r in df_coeff['Deg_Rate_ms_per_lap']],
        textposition='outside'
    ))
    
    # Add a vertical line at 0 ms/lap (no degradation)
    fig.add_vline(x=0, line_dash="dash", line_color="grey")

    fig.update_layout(
        title='Tire Degradation Rate (ms/lap)',
        xaxis_title='Degradation Rate (milliseconds per lap)',
        yaxis_title='Driver',
        height=40 * len(df_coeff) + 100 if len(df_coeff) < 20 else 800, # dynamic height
        showlegend=False
    )
    return fig


def create_pace_degradation_comparison_driver(driver_number):
    """Viz 1: Pace Degradation Model - Driver vs. Average Trend Comparison.
    
    Compares the target driver's degradation trend line against the overall field average.
    """
    
    # Base filtered data for ALL drivers (Green Flag laps, after lap 2)
    df_pace_gf = analysis_df[
        (analysis_df['FLAG_AT_FL'] == 'GF') & 
        (analysis_df['LAP_NUMBER'] > 2)
    ].dropna(subset=['LAP_TIME_SECONDS']).copy()
    df_pace_gf = df_pace_gf.rename(columns={'LAP_TIME_SECONDS': 'LAP_TIME_S'})

    fig = go.Figure()
    
    # --- 1. Calculate and Plot AVERAGE Degradation Trend ---
    
    # Use all eligible laps for the average model
    X_avg = df_pace_gf['LAP_NUMBER'].values.reshape(-1, 1)
    y_avg = df_pace_gf['LAP_TIME_S'].values
    
    # Only calculate if enough data exists
    if len(df_pace_gf) >= 5:
        model_avg = LinearRegression()
        model_avg.fit(X_avg, y_avg)
        avg_deg_rate = model_avg.coef_[0] * 1000 # ms per lap
        
        # Determine the full lap number range for the average line
        min_lap = df_pace_gf['LAP_NUMBER'].min()
        max_lap = df_pace_gf['LAP_NUMBER'].max()
        lap_range = np.linspace(min_lap, max_lap, 100).reshape(-1, 1)
        
        fig.add_trace(go.Scatter(
            x=lap_range.flatten(), 
            y=model_avg.predict(lap_range),
            mode='lines',
            line=dict(color='grey', width=3, dash='dash'),
            name=f'Average Driver Fit (+{avg_deg_rate:.1f} ms/lap)',
            hovertemplate="Lap %{x}<br>Fit Time: %{y:.3f}s<extra></extra>"
        ))
    else:
        avg_deg_rate = np.nan
    
    # --- 2. Calculate and Plot TARGET Driver's Trend ---
    
    df_driver = df_pace_gf[df_pace_gf['NUMBER'] == driver_number].copy()
    
    if len(df_driver) >= 5:
        X_target = df_driver['LAP_NUMBER'].values.reshape(-1, 1)
        y_target = df_driver['LAP_TIME_S'].values
        
        model_target = LinearRegression()
        model_target.fit(X_target, y_target)
        target_deg_rate = model_target.coef_[0] * 1000 # ms per lap

        fig.add_trace(go.Scatter(
            x=df_driver['LAP_NUMBER'], 
            y=model_target.predict(X_target),
            mode='lines',
            line=dict(color='red', width=5), # Highlighted line
            name=f'Car #{driver_number} Fit (+{target_deg_rate:.1f} ms/lap)',
            hovertemplate="Lap %{x}<br>Fit Time: %{y:.3f}s<extra></extra>"
        ))
        
    fig.update_layout(
        title=f'Car #{driver_number} Pace Degradation Trend vs. Field Average',
        xaxis_title='Lap Number',
        yaxis_title='Lap Time (Seconds) - Lower is Faster',
        height=600,
        hovermode='x unified'
    )
    return fig



def create_coeff_field_rank_driver(driver_number):
    """Driver vs. Average Degradation Rate.
    
    Highlights the target driver and adds a vertical line for the field average degradation.
    """
    
    deg_coefficients = {}
    # Filter for valid, clean laps (GF laps, after lap 2)
    df_pace_gf = analysis_df[
        (analysis_df['FLAG_AT_FL'] == 'GF') & 
        (analysis_df['LAP_NUMBER'] > 2)
    ].dropna(subset=['LAP_TIME_SECONDS']).copy()
    df_pace_gf = df_pace_gf.rename(columns={'LAP_TIME_SECONDS': 'LAP_TIME_S'})

    for driver in df_pace_gf['NUMBER'].unique():
        df_driver = df_pace_gf[df_pace_gf['NUMBER'] == driver]
        if len(df_driver) >= 5:
            X = df_driver['LAP_NUMBER'].values
            y = df_driver['LAP_TIME_S'].values
            slope, _, _, _, _ = linregress(X, y)
            deg_coefficients[driver] = slope * 1000 # Degradation rate in ms/lap

    df_coeff = pd.Series(deg_coefficients).to_frame(name='Deg_Rate_ms_per_lap')
    # Sort by fastest (smallest) degradation rate first, then reverse for plotting
    df_coeff = df_coeff.sort_values(by='Deg_Rate_ms_per_lap', ascending=True).iloc[::-1]

    # Calculate Average Degradation Rate
    avg_deg_rate = df_coeff['Deg_Rate_ms_per_lap'].mean()
    
    # DETERMINE MARKER COLOR (SIMPLIFIED FOR CLARITY):
    # Target Driver = Red/Orange, All others = Neutral Grey/Blue
    marker_colors = [
        'red' if num == driver_number else 'lightblue'
        for num in df_coeff.index
    ]

    fig = go.Figure(go.Bar(
        y=[f"Car #{num}" for num in df_coeff.index],
        x=df_coeff['Deg_Rate_ms_per_lap'],
        orientation='h',
        marker=dict(color=marker_colors),
        text=[f'{r:.1f} ms/lap' for r in df_coeff['Deg_Rate_ms_per_lap']],
        textposition='outside',
        name='Driver Degradation Rate'
    ))
    
    # Add vertical line at 0 ms/lap
    fig.add_vline(x=0, line_dash="dash", line_color="grey", 
                  annotation_text="Ideal (0 ms/lap)", annotation_position="top left", 
                  annotation=dict(font_size=12))
    
    # Add vertical line for Average Degradation Rate
    fig.add_vline(
        x=avg_deg_rate, 
        line_dash="dot", 
        line_color="blue", 
        annotation_text=f"Average ({avg_deg_rate:.1f} ms/lap)",
        annotation_position="bottom right",
        annotation=dict(font_size=12)
    )

    fig.update_layout(
        title=f'Tire Degradation Rate Field Rank (Car #{driver_number} Highlighted)',
        xaxis_title='Degradation Rate (milliseconds per lap) - Lower is Better',
        yaxis_title='Driver',
        height=40 * len(df_coeff) + 100 if len(df_coeff) < 20 else 800,
        showlegend=False
    )
    return fig

# Output
tab1, tab2 = st.tabs(["Overview", "Driver Comparison"])
with tab1:
    # Pace Degradation Model
    try:
        fig_deg = create_pace_degradation_comparison(N_drivers=5)
        st.plotly_chart(fig_deg)
    except Exception as e:
        st.error(f"Error loading Pace Degradation Model: {e}")

    # Tire degradation
    try:
        fig_rank = create_coeff_field_rank()
        st.plotly_chart(fig_rank)
    except Exception as e:
        st.error(f"Error loading Degradation Rank: {e}")

with tab2:        
    try:
        fig_deg_driver = create_pace_degradation_comparison_driver(race_car_driver_options)
        st.plotly_chart(fig_deg_driver)
    except Exception as e:
        st.error(f"Error loading Pace Degradation Model: {e}")

    try:
        fig_rank_driver = create_coeff_field_rank_driver(race_car_driver_options)
        st.plotly_chart(fig_rank_driver)
    except Exception as e:
        st.error(f"Error loading Degradation Rank: {e}")

