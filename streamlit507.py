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

st.set_page_config(layout="wide")

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



select = st.selectbox('Select a hospital',ny_df['hospital_name'])

#get the state selected in the selectbox
Hospital_data = ny_df[ny_df['hospital_name'] == select]


st.header('New York Hospital Data')
st.dataframe(Hospital_data)

Hospital_data.style.set_properties(**{'border': '1.3px solid green',
                          'color': 'magenta'})
st.subheader('Map of NY Hospital Locations')

hospitals_ny_gps = ny_df['location'].str.strip('()').str.split(' ', expand=True).rename(columns={0: 'Point', 1:'lon', 2:'lat'}) 	
hospitals_ny_gps['lon'] = hospitals_ny_gps['lon'].str.strip('(')
hospitals_ny_gps = hospitals_ny_gps.dropna()
hospitals_ny_gps['lon'] = pd.to_numeric(hospitals_ny_gps['lon'])
hospitals_ny_gps['lat'] = pd.to_numeric(hospitals_ny_gps['lat'])

st.map(hospitals_ny_gps)


inpatientcompare = nyinpatient.groupby("provider_name")["total_discharges", "average_covered_charges", "average_total_payments", "average_medicare_payments"].mean()

inpatientcompare.info()
inpatientcompare = inpatientcompare.reset_index()

outpatientcompare = nyoutpatient.groupby("provider_name")["outpatient_services", "average_estimated_submitted_charges", "average_total_payments"].mean()

outpatientcompare.info()
outpatientcompare = outpatientcompare.reset_index()

col1, col2 = st.columns(2)

with col1:

    st.header('Inpatient Data Comparison (SB and NONSB)')

    fig = px.bar(inpatientcompare, x="provider_name", y=["total_discharges", "average_covered_charges", "average_total_payments", "average_medicare_payments"], barmode='group', height=400)
    st.plotly_chart(fig)


with col2:
    
    st.header('Outpatient Data Comparison (SB and NONSB)')

    fig1 = px.bar(outpatientcompare, x="provider_name", y=["outpatient_services", "average_estimated_submitted_charges", "average_total_payments"], barmode='group', height=400)
    st.plotly_chart(fig1)


col1, col2 = st.columns(2)

with col1:
    
    st.header('Inpatient DRG Costs at SB Hospital')

    dataframe_pivot1 = sb_inpatient.pivot_table(index=['drg_definition'],values=['average_total_payments'],aggfunc='mean')
    st.dataframe(dataframe_pivot1)

with col2:

    st.header('Outpatient DRG Costs at SB Hospital')
    
    dataframe_pivot2 = sb_outpatient.pivot_table(index=['apc'],values=['average_total_payments'],aggfunc='mean')
    st.dataframe(dataframe_pivot2)


col1, col2 = st.columns(2)

with col1:
    st.header('Hospital Ownership in NY')
    bar1 = ny_df['hospital_ownership'].value_counts().reset_index()
    st.dataframe(bar1)


    st.header('PIE Chart: Ownership')
    fig3 = px.pie(bar1, values='hospital_ownership', names='index')
    st.plotly_chart(fig3)

with col2:
    st.header('Hospital Type in NY')
    bar2 = ny_df['hospital_type'].value_counts().reset_index()
    st.dataframe(bar2)


    st.header('PIE Chart: Type')
    fig4 = px.pie(bar2, values='hospital_type', names='index')
    st.plotly_chart(fig4)
    
    

st.header('Hospital Location by City')
bar3 = ny_df['city'].value_counts().reset_index()
st.dataframe(bar3)



