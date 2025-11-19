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


fig1 = create_fastest_lap_distribution()
st.plotly_chart(fig1)

fig3 = create_dnf_analysis()
st.plotly_chart(fig3)

