# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 02:23:55 2021

@author: natha
"""
#### PART ONE - Loading the Data, cleaning and transforming the data, initial EDA
import pandas as pd
import numpy as np

df_hospital = pd.read_csv("https://raw.githubusercontent.com/hantswilliams/AHI_DataSci_507/main/Deployment_Streamlit/hospital_info.csv")
df_inpatient = pd.read_csv("https://raw.githubusercontent.com/hantswilliams/AHI_DataSci_507/main/Deployment_Streamlit/inpatient_2015.csv")
df_outpatient = pd.read_csv("https://raw.githubusercontent.com/hantswilliams/AHI_DataSci_507/main/Deployment_Streamlit/outpatient_2015.csv")

pip install pandas-profiling

from pandas_profiling import ProfileReport

profile1 = ProfileReport(df_hospital, explorative=True)
profile1.to_file("/Users/natha/Downloads/profiling_df_hospital.html")

profile2 = ProfileReport(df_outpatient, explorative=True)
profile2.to_file("/Users/natha/Downloads/profiling_df_outpatient.html")

profile3 = ProfileReport(df_inpatient, explorative=True)
profile3.to_file("/Users/natha/Downloads/profiling_df_inpatient.html")

pip install sweetviz
import sweetviz as sv

sweet_report1 = sv.analyze(df_hospital)
sweet_report1.show_html('/Users/natha/Downloads/sweet_report_df_hospital.html')

sweet_report2 = sv.analyze(df_outpatient)
sweet_report2.show_html('/Users/natha/Downloads/sweet_report_df_outpatient.html')

sweet_report3 = sv.analyze(df_inpatient)
sweet_report3.show_html('/Users/natha/Downloads/sweet_report_df_inpatient.html')

conda install -c conda-forge dtale
import dtale

d = dtale.show(df_hospital, ignore_duplicate=True)
d.open_browser()

d = dtale.show(df_outpatient, ignore_duplicate=True)
d.open_browser()

d = dtale.show(df_inpatient, ignore_duplicate=True)
d.open_browser()

## Cleaning the data

pip install pyjanitor
from janitor import clean_names, remove_empty

df_hospital_2 = clean_names(df_hospital)
df_hospital_2 = remove_empty(df_hospital_2)

df_inpatient_2 = clean_names(df_inpatient)
df_inpatient_2 = remove_empty(df_inpatient_2)

df_outpatient_2 = clean_names(df_outpatient)
df_outpatient_2 = remove_empty(df_outpatient_2)

df_hospital_2.to_csv('/Users/natha/Downloads/df_hospital_2.csv', index=False, encoding='utf-8-sig')
df_inpatient_2.to_csv('/Users/natha/Downloads/df_inpatient_2.csv', index=False, encoding='utf-8-sig')
df_outpatient_2.to_csv('/Users/natha/Downloads/df_outpatient_2.csv', index=False, encoding='utf-8-sig')

# Fiiling missing values, duplicates
df_hospital_2.isnull()
df_hospital_2.isna().any()
df_hospital_2.isna().any().sum()
df_hospital_2 = df_hospital_2.fillna(0)

df_hospital_2.duplicated()
df_hospital_2.drop_duplicates(subset=None, keep='first', inplace=False, ignore_index=False)
df_hospital_2 = df_hospital_2.drop_duplicates(subset=None, keep='first', inplace=False, ignore_index=False)

### Q1: How does Stony Brook compare to the rest of NY

## Creating dataframes for only NY hospitals (SB and nonSB) and exploratory data analysis

ny_df = df_hospital_2[(df_hospital_2.state == "NY")]
sb_hospital = ny_df[ny_df['provider_id'] == '330393']
nonsb_hospital = ny_df[ny_df['provider_id'] != '330393']

ny_df.to_csv('/Users/natha/Downloads/ny_df.csv', index=False, encoding='utf-8-sig')


# Hospital EDA

ny_df['meets_criteria_for_meaningful_use_of_ehrs'] = ny_df['meets_criteria_for_meaningful_use_of_ehrs'].astype(bool)
ny_df['hospital_overall_rating_footnote'] = ny_df['hospital_overall_rating_footnote'].astype('str')
ny_df['mortality_national_comparison_footnote'] = ny_df['mortality_national_comparison_footnote'].astype('float64')
ny_df['safety_of_care_national_comparison_footnote'] = ny_df['safety_of_care_national_comparison_footnote'].astype('str')
ny_df['readmission_national_comparison_footnote'] = ny_df['readmission_national_comparison_footnote'].astype('str')
ny_df['patient_experience_national_comparison_footnote'] = ny_df['patient_experience_national_comparison_footnote'].astype('str')
ny_df['effectiveness_of_care_national_comparison_footnote'] = ny_df['effectiveness_of_care_national_comparison_footnote'].astype('str')
ny_df['timeliness_of_care_national_comparison_footnote'] = ny_df['timeliness_of_care_national_comparison_footnote'].astype('str')
ny_df['efficient_use_of_medical_imaging_national_comparison_footnote'] = ny_df['efficient_use_of_medical_imaging_national_comparison_footnote'].astype('str')
ny_df['location'] = ny_df['location'].astype('str')

ny_df_analysis = sv.analyze(ny_df)
ny_df_analysis.show_html('/Users/natha/Downloads/sweet_report_ny_df.html')

## NY Inpatient Data (SB and nonSB) dataframes and exploratory data analysis

nyinpatient = df_inpatient_2[(df_inpatient_2.provider_state == "NY")]
nyinpatient.loc[nyinpatient.provider_name != "UNIVERSITY HOSPITAL ( STONY BROOK )", "provider_name"] = "nonsb"

sb_inpatient = nyinpatient[nyinpatient['provider_name'] == 'UNIVERSITY HOSPITAL ( STONY BROOK )']
sb_inpatient.to_csv('/Users/natha/Downloads/sb_patient.csv', index=False, encoding='utf-8-sig')

nonsb_nyinpatient = nyinpatient[nyinpatient['provider_name'] != 'UNIVERSITY HOSPITAL ( STONY BROOK )']

nyinpatient.to_csv('/Users/natha/Downloads/nyinpatient.csv', index=False, encoding='utf-8-sig')


# Inpatient EDA for comparison
sb_inpatient_analysis = sv.analyze(sb_inpatient)
sb_inpatient_analysis.show_html('/Users/natha/Downloads/sweet_report_df_inpatient_sb.html')

my_report = sv.compare([sb_inpatient, "Inpatient_SB"], [nonsb_nyinpatient, "Inpatient_NonSB"])
my_report.show_html('/Users/natha/Downloads/sweet_report_inpatient_compare.html')

## NY Outpatient Data (SB and nonSB) dataframes and exploratory data analysis

nyoutpatient = df_outpatient_2[(df_outpatient_2.provider_state == "NY")]
nyoutpatient.loc[nyoutpatient.provider_name != "University Hospital ( Stony Brook )", "provider_name"] = "nonsb"

sb_outpatient = nyoutpatient[nyoutpatient['provider_name'] == 'University Hospital ( Stony Brook )']
sb_outpatient.to_csv('/Users/natha/Downloads/sb_outpatient.csv', index=False, encoding='utf-8-sig')

nonsb_nyoutpatient = nyoutpatient[nyoutpatient['provider_name'] != 'University Hospital ( Stony Brook )']

nyoutpatient.to_csv('/Users/natha/Downloads/nyoutpatient.csv', index=False, encoding='utf-8-sig')


#Outpatient EDA for comparison
my_report2 = sv.compare([sb_outpatient, "Outpatient_SB"], [nonsb_nyoutpatient, "Outpatient_NonSB"])
my_report2.show_html('/Users/natha/Downloads/sweet_report_outpatient_compare.html')


### Q2: Stony Brook most expensive inpatient DRG?

dataframe_pivot1 = sb_inpatient.pivot_table(index=['provider_name','drg_definition'],values=['average_total_payments'],aggfunc='mean')
dataframe_pivot1

### Q3: Stony Brook most expensive outpatient DRG?

dataframe_pivot2 = sb_outpatient.pivot_table(index=['provider_name','apc'],values=['average_total_payments'],aggfunc='mean')
dataframe_pivot2


