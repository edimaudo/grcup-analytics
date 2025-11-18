from utils import *


# Load data
@st.cache_data
def load_data(DATA_URL):
    """Loads files based on file type (CSV only)."""
    data = pd.read_csv(DATA_URL, sep=';', skipinitialspace=True)
    return data

# Race data
RACE_TRACK_NAME = ["Barber Motorsports Park","Circuit of the Americas",
                   "Indianapolis",#'Road America',
                   #'Sebring',
                   'Sonoma']#,'Virginia International Raceway']
RACE_NUMBERS = ['Race 1']#,'Race 2']

def select_race(racename,race_number):
    """Select race data based on race name and number."""
    if racename == "Barber Motorsports Park":
        if racename == "Race 1":
            file_result_provisional = load_data('data/barber/Race 1/03_Provisional Results_Race 1_Anonymized.CSV')
            file_result_provisional_class = load_data('data/barber/Race 1/05_Provisional Results by Class_Race 1_Anonymized.CSV')
            file_results_official_class = load_data('data/barber/Race 1/05_Results by Class GR Cup Race 1 Official_Anonymized.CSV')
            file_results_official = None
            file_analysis = load_data('data/barber/Race 1/23_AnalysisEnduranceWithSections_Race 1_Anonymized.CSV')
            file_weather = load_data('data/barber/Race 1/26_Weather_Race 1_Anonymized.CSV')
            file_best10 = load_data('data/barber/Race 1/99_Best 10 Laps By Driver_Race 1_Anonymized.CSV')
            file_lap_end = load_data('data/barber/Race 1/R1_barber_lap_end.csv')
            file_lap_start = load_data('data/barber/Race 1/R1_barber_lap_start.csv')
            final_lap_ms = load_data('data/barber/Race 1/R1_barber_lap_time.csv')
        else:
            file_result_provisional = load_data('data/barber/Race 2/03_Provisional Results_Race 2_Anonymized.CSV')
            file_results_official = load_data('data/barber/Race 2/03_Results GR Cup Race 2 Official_Anonymized.CSV')
            file_results_official_class = None
            file_result_provisional_class = load_data('data/barber/Race 2/05_Provisional Results by Class_Race 2_Anonymized.CSV')
            file_analysis = load_data('data/barber/Race 2/23_AnalysisEnduranceWithSections_Race 2_Anonymized.CSV')
            file_weather = load_data('data/barber/Race 2/26_Weather_Race 2_Anonymized.CSV')
            file_best10 = load_data('data/barber/Race 2/99_Best 10 Laps By Driver_Race 2_Anonymized.CSV')
            file_lap_end = load_data('data/barber/Race 2/R2_barber_lap_end.csv')
            file_lap_start = load_data('data/barber/Race 2/R2_barber_lap_start.csv')
            final_lap_ms = load_data('data/barber/Race 2/R2_barber_lap_time.csv')

    elif racename == "Circuit of the Americas":
        if race_number == "Race 1":
            file_results_official = load_data('data/COTA/Race 1/00_Results GR Cup Race 1 Official_Anonymized.CSV')
            file_results_official_class = None
            file_result_provisional = load_data('data/COTA/Race 1/03_Provisional Results_Race 1_Anonymized.CSV')
            file_result_provisional_class = load_data('data/COTA/Race 1/05_Provisional Results by Class_Race 1_Anonymized.CSV')
            file_analysis = load_data('data/COTA/Race 1/23_AnalysisEnduranceWithSections_Race 1_Anonymized.CSV')
            file_weather = load_data('data/COTA/Race 1/26_Weather_Race 1_Anonymized.CSV')
            file_best10 = load_data('data/COTA/Race 1/99_Best 10 Laps By Driver_Race 1_Anonymized.CSV')
            file_lap_end = load_data('data/COTA/Race 1/COTA_lap_end_time_R1.csv')
            file_lap_start = load_data('data/COTA/Race 1/COTA_lap_start_time_R1.csv')
            final_lap_ms = load_data('data/COTA/Race 1/COTA_lap_time_R1.csv')
        else:
            file_results_official = None
            file_results_official_class = None
            file_result_provisional = load_data('data/COTA/Race 2/03_Provisional Results_ Race 2_Anonymized.CSV')
            file_result_provisional_class = load_data('data/COTA/Race 2/05_Provisional Results by Class_ Race 2_Anonymized.CSV')
            file_analysis = load_data('data/COTA/Race 2/23_AnalysisEnduranceWithSections_ Race 2_Anonymized.CSV')
            file_weather = load_data('data/COTA/Race 2/26_Weather_ Race 2_Anonymized.CSV')
            file_best10 = load_data('data/COTA/Race 2/99_Best 10 Laps By Driver_ Race 2_Anonymized.CSV')
            file_lap_end = load_data('data/COTA/Race 2/COTA_lap_end_time_R2.csv')
            file_lap_start = load_data('data/COTA/Race 2/COTA_lap_start_time_R2.csv')
            final_lap_ms = load_data('data/COTA/Race 2/COTA_lap_time_R2.csv')
    elif racename == "Indianapolis":
        if race_number == "Race 1":
            file_results_official = load_data('data/indianapolis/Race 1/03_GR Cup Race 1 Official Results.CSV')
            file_result_provisional = load_data('data/indianapolis/Race 1/03_Provisional Results_Race 1.CSV')
            file_results_official_class = load_data('data/indianapolis/Race 1/05_GR Cup Race 1 Official Results by Class.CSV')
            file_result_provisional_class = load_data('data/indianapolis/Race 1/05_Provisional Results by Class_Race 1.CSV')
            file_analysis = load_data('data/indianapolis/Race 1/23_AnalysisEnduranceWithSections_Race 1.CSV')
            file_weather = load_data('data/indianapolis/Race 1/26_Weather_Race 1.CSV')
            file_best10 = load_data('data/indianapolis/Race 1/99_Best 10 Laps By Driver_Race 1.CSV')
            file_lap_end = load_data('data/indianapolis/Race 1/R1_indianapolis_motor_speedway_lap_end.csv')
            file_lap_start = load_data('data/indianapolis/Race 1/R1_indianapolis_motor_speedway_lap_start.csv')
            final_lap_ms = load_data('data/indianapolis/Race 1/R1_indianapolis_motor_speedway_lap_time.csv')
        else:
            file_results_official = load_data('data/indianapolis/Race 2/03_GR Cup Race 2 Official Results.CSV')
            file_result_provisional = load_data('data/indianapolis/Race 2/03_Provisional Results_Race 2.CSV')
            file_results_official_class = load_data('data/indianapolis/Race 2/05_GR Cup Race 2 Official Results by Class.CSV')
            file_result_provisional_class = load_data('data/indianapolis/Race 2/05_Provisionals Results by Class_Race 2.CSV')
            file_analysis = load_data('data/indianapolis/Race 2/23_AnalysisEnduranceWithSections_Race 2.CSV')
            file_weather = load_data('data/indianapolis/Race 2/26_Weather_Race 2.CSV')
            file_best10 = load_data('data/indianapolis/Race 2/99_Best 10 Laps By Driver_Race 2.CSV')
            file_lap_end = load_data('data/indianapolis/Race 2/R2_indianapolis_motor_speedway_lap_end.csv')
            file_lap_start = load_data('data/indianapolis/Race 2/R2_indianapolis_motor_speedway_lap_start.csv')
            final_lap_ms = load_data('data/indianapolis/Race 2/R2_indianapolis_motor_speedway_lap_time.csv')
    elif racename == "Road America":
        if race_number == "Race 1":
            file_results_official = None
            file_result_provisional = load_data('data/Road America/Race 1/03_Provisional Results_Race 1_Anonymized.CSV')
            file_result_provisional_class = load_data('data/Road America/Race 1/05_Provisional Results by Class_Race 1_Anonymized.CSV')
            file_results_official_class = load_data('data/Road America/Race 1/05_Results by Class GR Cup Race 1 Official_Anonymized.CSV')
            file_analysis = load_data('data/Road America/Race 1/23_AnalysisEnduranceWithSections_Race 1_Anonymized.CSV')
            file_weather = load_data('data/Road America/Race 1/26_Weather_Race 1_Anonymized.CSV')
            file_best10 = load_data('data/Road America/Race 1/99_Best 10 Laps By Driver_Race 1_Anonymized.CSV')
            file_lap_end = load_data('data/Road America/Race 1/road_america_lap_end_R1.csv')
            file_lap_start = load_data('data/Road America/Race 1/road_america_lap_start_R1.csv')
            final_lap_ms = load_data('data/Road America/Race 1/road_america_lap_time_R1.csv')
        else: 
            file_results_official = None
            file_result_provisional = load_data('data/Road America/Race 2/03_Provisional Results_Race 2_Anonymized.CSV')
            file_results_official = load_data('data/Road America/Race 2/03_Results GR Cup Race 2 Official_Anonymized.CSV')
            file_result_provisional_class = load_data('data/Road America/Race 2/05_Provisional Results by Class_Race 2_Anonymized.CSV')
            file_analysis = load_data('data/Road America/Race 2/23_AnalysisEnduranceWithSections_Race 2_Anonymized.CSV')
            file_weather = load_data('data/Road America/Race 2/26_Weather_Race 2_Anonymized.CSV')
            file_best10 = load_data('data/Road America/Race 2/99_Best 10 Laps By Driver_Race 2_Anonymized.CSV')
            file_lap_end = load_data('data/Road America/Race 2/road_america_lap_end_R2.csv')
            file_lap_start = load_data('data/Road America/Race 2/road_america_lap_start_R2.csv')
            final_lap_ms = load_data('data/Road America/Race 2/road_america_lap_time_R2.csv')
    elif racename == "Sebring":
        if race_number == "Race 1":
            file_results_official = None
            file_results_official_class = None
            file_result_provisional = load_data('data/Sebring/Race 1/03_Provisional Results_Race 1_Anonymized.CSV')
            file_result_provisional_class = load_data('data/Sebring/Race 1/05_Provisional Results by Class_Race 1_Anonymized.CSV')
            file_analysis = load_data('data/Sebring/Race 1/23_AnalysisEnduranceWithSections_Race 1_Anonymized.CSV')
            file_weather = load_data('data/Sebring/Race 1/26_Weather_Race 1_Anonymized.CSV')
            file_best10 = load_data('data/Sebring/Race 1/99_Best 10 Laps By Driver_Race 1_Anonymized.CSV')
            file_lap_end = load_data('data/Sebring/Race 1/sebring_lap_end_time_R1.csv')
            file_lap_start = load_data('data/Sebring/Race 1/sebring_lap_start_time_R1.csv')
            final_lap_ms = load_data('data/Sebring/Race 1/sebring_lap_time_R1.csv')
        else:  
            file_results_official = load_data('data/Sebring/Race 2/00_Results GR Race 2 Official_Anonymized.CSV')
            file_results_official_class = None
            file_result_provisional = load_data('data/Sebring/Race 2/03_Provisional Results_Race 2_Anonymized.CSV')
            file_result_provisional_class = load_data('data/Sebring/Race 2/05_Provisional Results by Class_Race 2_Anonymized.CSV')
            file_analysis = load_data('data/Sebring/Race 2/23_AnalysisEnduranceWithSections_Race 2_Anonymized.CSV')
            file_weather = load_data('data/Sebring/Race 2/26_Weather_Race 2_Anonymized.CSV')
            file_best10 = load_data('data/Sebring/Race 2/99_Best 10 Laps By Driver_Race 2_Anonymized.CSV')
            file_lap_end = load_data('data/Sebring/Race 2/sebring_lap_end_time_R2.csv')
            file_lap_start = load_data('data/Sebring/Race 2/sebring_lap_start_time_R2.csv')
            final_lap_ms = load_data('data/Sebring/Race 2/sebring_lap_time_R2.csv')        
    elif racename == "Sonoma":
        if race_number == "Race 1":
            file_results_official = load_data('data/Sonoma/Race 1/03_Results_Anonymized.CSV')
            file_results_official_class = load_data('data/Sonoma/Race 1/05_Results by Class_Race 1_Anonymized.CSV')
            file_result_provisional_class = None
            file_result_provisional = None
            file_analysis = load_data('data/Sonoma/Race 1/23_AnalysisEnduranceWithSections_Race 1_Anonymized.CSV')
            file_weather = load_data('data/Sonoma/Race 1/26_Weather_Race 1_Anonymized.CSV')
            file_best10 = load_data('data/Sonoma/Race 1/99_Best 10 Laps By Driver_Race 1_Anonymized.CSV')
            file_lap_end = load_data('data/Sonoma/Race 1/sonoma_lap_end_time_R1.csv')
            file_lap_start = load_data('data/Sonoma/Race 1/sonoma_lap_start_time_R1.csv')
            final_lap_ms = load_data('data/Sonoma/Race 1/sonoma_lap_time_R1.csv')
        else:
            file_result_provisional = load_data('data/Sonoma/Race 2/03_Provisional_Results_Race 2_Anonymized.CSV')
            file_results_official = load_data('data/Sonoma/Race 2/03_Results_Anonymized.CSV')
            file_results_official_class = None
            file_result_provisional_class = load_data('data/Sonoma/Race 2/05_Provisional_Results by Class_Race 2_Anonymized.CSV')
            file_analysis = load_data('data/Sonoma/Race 2/23_AnalysisEnduranceWithSections_Race 2_Anonymized.CSV')
            file_best10 = load_data('data/Sonoma/Race 2/99_Best 10 Laps By Driver_Race 2_Anonymized.CSV')
            file_lap_end = load_data('data/Sonoma/Race 2/sonoma_lap_end_time_R2.csv')
            file_lap_start = load_data('data/Sonoma/Race 2/sonoma_lap_start_time_R2.csv')
            final_lap_ms = load_data('data/Sonoma/Race 2/sonoma_lap_time_R2.csv')
    elif racename == "Virginia International Raceway":
        if race_number == "Race 1":
            file_result_provisional = load_data('data/VIR/Race 1/03_Provisional Results_Race 1_Anonymized.CSV')
            file_result_provisional_class = load_data('data/VIR/Race 1/05_Provisional Results by Class_Race 1_Anonymized.CSV')
            file_results_official = None
            file_results_official_class = load_data('data/VIR/Race 1/05_Results by Class GR Cup Race 1 Official_Anonymized.CSV')
            file_analysis = load_data('data/VIR/Race 1/23_AnalysisEnduranceWithSections_Race 1_Anonymized.CSV')
            file_weather = load_data('data/VIR/Race 1/26_Weather_Race 1_Anonymized.CSV')
            file_best10 = load_data('data/VIR/Race 1/99_Best 10 Laps By Driver_Race 1_Anonymized.CSV')
            file_lap_end = load_data('data/VIR/Race 1/vir_lap_end_R1.csv')
            file_lap_start = load_data('data/VIR/Race 1/vir_lap_start_R1.csv')
            final_lap_ms = load_data('data/VIR/Race 1/vir_lap_time_R1.csv')
        else:
            file_result_provisional = load_data('data/VIR/Race 2/03_Provisional Results_Race 2_Anonymized.CSV')
            file_results_official = load_data('data/VIR/Race 2/03_Results GR Cup Race 2 Official_Anonymized.CSV')
            file_result_provisional_class = load_data('data/VIR/Race 2/05_Provisional Results by Class_Race 2_Anonymized.CSV')
            file_results_official_class = None
            file_analysis = load_data('data/VIR/Race 2/23_AnalysisEnduranceWithSections_Race 2_Anonymized.CSV')
            file_weather = load_data('data/VIR/Race 2/26_Weather_Race 2_Anonymized.CSV')
            file_best10 = load_data('data/VIR/Race 2/99_Best 10 Laps By Driver_Race 2_Anonymized.CSV')
            file_lap_end = load_data('data/VIR/Race 2/vir_lap_end_R2.csv')
            file_lap_start = load_data('data/VIR/Race 2/vir_lap_start_R2.csv')
            final_lap_ms = load_data('data/VIR/Race 2/vir_lap_time_R2.csv')
    


    return [file_analysis, file_best10, final_lap_ms, file_weather, file_lap_end, file_result_provisional,
            file_result_provisional_class, 
            file_results_official,file_results_official_class, file_lap_start]


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

def time_to_seconds(time_str):
    """Converts a time string (M:SS.ms or H:MM:SS.ms) or float/int to total seconds (float)."""
    if pd.isna(time_str):
        return np.nan

    if isinstance(time_str, (int, float)):
        return float(time_str)

    time_str = str(time_str).strip().replace(' ', '')
    parts = time_str.split(':')

    try:
        if len(parts) == 3:
            # H:MM:SS.ms
            h, m, s = map(float, parts)
            return h * 3600 + m * 60 + s
        elif len(parts) == 2:
            # M:SS.ms
            m, s = map(float, parts)
            return m * 60 + s
        elif len(parts) == 1:
            # SS.ms
            return float(parts[0])
    except ValueError:
        return np.nan
    return np.nan

def ms_to_seconds(ms):
    """Converts milliseconds to seconds (float)."""
    return ms / 1000.0 if not pd.isna(ms) else np.nan

def extract_driver_num(vid):
    """Extracts the numeric driver number from vehicle_id (e.g., 'GR86-062-012' -> 62)."""
    if 'GR86-' in vid:
        try:
            return int(vid.split('GR86-')[1].split('-')[0])
        except:
            return np.nan
    return np.nan