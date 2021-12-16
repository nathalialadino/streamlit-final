# -*- coding: utf-8 -*-
"""
Created on Wed Dec 15 19:27:59 2021

@author: natha
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import time


st.title('Hospital data analysis')

@st.cache
def load_hospitals():
    ny_df = pd.read_csv('https://raw.githubusercontent.com/nathalialadino/Streamlit-Final-Nathalia/main/ny_df.csv')
    return ny_df

@st.cache
def load_inatpatient():
    nyinpatient = pd.read_csv('https://raw.githubusercontent.com/nathalialadino/Streamlit-Final-Nathalia/main/nyinpatient.csv')
    return nyinpatient

@st.cache
def load_outpatient():
    nyoutpatient = pd.read_csv('https://raw.githubusercontent.com/nathalialadino/Streamlit-Final-Nathalia/main/nyoutpatient.csv')
    return nyoutpatient

ny_df = load_hospitals()
nyinpatient = load_inatpatient()
nyoutpatient = load_outpatient()

st.header('New York Hospital Data')
st.dataframe(ny_df)

st.header('New York Inpatient Data')
st.dataframe(nyinpatient)

st.header('New York Outpatient Data')
st.dataframe(nyoutpatient)


st.sidebar.checkbox("Show Analysis by different hospitals", True, key=1)
select = st.sidebar.selectbox('Select a hospital',nyinpatient['provider_name'])

#get the state selected in the selectbox
state_data = nyinpatient[nyinpatient['provider_name'] == select]



nyinpatient.loc[nyinpatient.provider_name != "UNIVERSITY HOSPITAL ( STONY BROOK )", "provider_name"] = "nonsb"
inpatientcompare = nyinpatient.groupby("provider_name")["total_discharges", "average_covered_charges", "average_total_payments", "average_medicare_payments"].mean()

inpatientcompare.info()
inpatientcompare = inpatientcompare.reset_index()

st.header('Inpatient Data Comparison (SB and NONSB)')

fig = px.bar(inpatientcompare, x="provider_name", y=["total_discharges", "average_covered_charges", "average_total_payments", "average_medicare_payments"], barmode='group', height=400)
# st.dataframe(df) # if need to display dataframe
st.plotly_chart(fig)

