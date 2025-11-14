"""
Libraries
"""
import streamlit as st
import pandas as pd
import numpy as np
import datetime
import os, os.path
import warnings
import random
import plotly.express as px
import plotly.graph_objects as go
#import geopandas as gpd
#import folium
import pickle
#from pycaret.classification import *
#import pymysql
import json
import datetime
import time
import numpy as np
import statistics
#import xgboost
#import pmdarima as pm
from google import genai
import ssl
#from dotenv import load_dotenv, dotenv_values 
#load_dotenv() 

"""
App Information
"""
APP_NAME = 'GR CUP Analytics'
ABOUT_HEADER = 'About'
DRIVER_HEADER = 'Driver Insights'
PRE_RACE_HEADER = "Pre Event Analytics"
POST_RACE_HEADER = 'Post Event Analytics'
APP_FILTERS = 'Filters'
NO_DATA_INFO = 'No data available to display based on the filters'

warnings.simplefilter(action='ignore', category=FutureWarning)
st.set_page_config(
    page_title=APP_NAME,
    layout="wide"
)