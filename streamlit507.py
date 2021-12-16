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


st.title('Hospital Data Visualizations')

@st.cache
def load_hospitals():
    ny_df = pd.read_csv('https://raw.githubusercontent.com/nathalialadino/Streamlit-Final-Nathalia/main/ny_df.csv')
    return ny_df

@st.cache
def load_inpatient():
    nyinpatient = pd.read_csv('https://raw.githubusercontent.com/nathalialadino/streamlit-final/main/nyinpatient.csv')
    return nyinpatient

@st.cache
def load_outpatient():
    nyoutpatient = pd.read_csv('https://raw.githubusercontent.com/nathalialadino/streamlit-final/main/nyoutpatient.csv')
    return nyoutpatient

@st.cache
def load_sb_inpatient():
    sb_inpatient = pd.read_csv('https://raw.githubusercontent.com/nathalialadino/streamlit-final/main/sb_patient.csv')
    return sb_inpatient

@st.cache
def load_sb_outpatient():
    sb_outpatient = pd.read_csv('https://raw.githubusercontent.com/nathalialadino/streamlit-final/main/sb_outpatient.csv')
    return sb_outpatient

ny_df = load_hospitals()
nyinpatient = load_inpatient()
nyoutpatient = load_outpatient()
sb_inpatient = load_sb_inpatient()
sb_outpatient = load_sb_outpatient()


st.header('New York Hospital Data')
st.dataframe(ny_df)


inpatientcompare = nyinpatient.groupby("provider_name")["total_discharges", "average_covered_charges", "average_total_payments", "average_medicare_payments"].mean()

inpatientcompare.info()
inpatientcompare = inpatientcompare.reset_index()

st.header('Inpatient Data Comparison (SB and NONSB)')

fig = px.bar(inpatientcompare, x="provider_name", y=["total_discharges", "average_covered_charges", "average_total_payments", "average_medicare_payments"], barmode='group', height=400)
st.plotly_chart(fig)


outpatientcompare = nyoutpatient.groupby("provider_name")["outpatient_services", "average_estimated_submitted_charges", "average_total_payments"].mean()

outpatientcompare.info()
outpatientcompare = outpatientcompare.reset_index()

st.header('Outpatient Data Comparison (SB and NONSB)')

fig1 = px.bar(outpatientcompare, x="provider_name", y=["outpatient_services", "average_estimated_submitted_charges", "average_total_payments"], barmode='group', height=400)
st.plotly_chart(fig1)

st.subheader('Inpatient DRG Costs at SB Hospital')

dataframe_pivot1 = sb_inpatient.pivot_table(index=['drg_definition'],values=['average_total_payments'],aggfunc='mean')
st.dataframe(dataframe_pivot1)

st.subheader('Outpatient DRG Costs at SB Hospital')
dataframe_pivot2 = sb_outpatient.pivot_table(index=['apc'],values=['average_total_payments'],aggfunc='mean')
st.dataframe(dataframe_pivot2)

dataframe_pivot1, dataframe_pivot2 = st.columns(2)
