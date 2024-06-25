import pandas as pd
import streamlit as st
import altair as alt
import plotly.express as px
import urllib.parse
import plotly.graph_objects as go
import datetime
from streamlit_space import space
import numpy as np
import plotly as plt

with st.sidebar:
    st.markdown("Author: **:blue[HUA NGUYEN GIA HAN]**")
    st.write("Date: ", datetime.date(2024, 5, 30))
    st.text("Description: This project understands how the student's performance (test scores) is affected by other variables such as Gender, Ethnicity, Parental level of education, Lunch and Test preparation course.")

with st.container():
    st.subheader("x")
    st.title("x")
    st.write("x" ) 

st.title("Score")
st.markdown("I analyze the :blue[student study performance] data set available on the internet")

st.divider()

sp = pd.read_csv('C:/Users/vyvil/Documents/study_performance.csv')

st.header("Original data set")

st.text("This is a data frame with 1,000 observations on 9 variables.")

st.markdown(
"""
- *Description*: xxxxxxxxxxxxxxxxxxxxxxxxxxxx.
- *Variables*:
    1. **gender**: sex of students -> (Male/female)
    2. **race/ethnicity**: ethnicity of students -> (Group A, B,C, D,E)
    3. **parental_level_of_education**: parents' final education ->(bachelor's degree,some college,master's degree,associate's degree,- high school)
    4. **lunch**: having lunch before test (standard or free/reduced)
    5. **test_preparation_course**: complete or not complete before test
    6. **math_score**: math score
    7. **reading_score**: reading score
    8. **writing_score**: writing score
    9. **average_score**: average score
"""
)

st.dataframe(sp, width = 1000)

st.header("...")
st.text("...")
st.markdown("---")
tab1, tab2, tab3 = st.tabs(["1", "2", "3"])
with tab1:
 col1, col2 = st.columns([1, 3])
with col1:
        space(lines=10)
        
        by_what_1 = st.radio(
            "Choose a category:",
            ('lunch', 'gender', 'test_preparation_course','parental_level_of_education'),
            key = "r1")
        with col2:
        
         sp['average_score'] = sp.apply(lambda row:(row.math_score + row.reading_score + row.writing_score) / 3, axis = 1)
         fig1 = px.pie(sp, values = "average_score", names = by_what_1, hole = 0.7) 
         fig1.update_traces(text = sp[by_what_1], textposition = "outside")
st.plotly_chart(fig1, theme = "streamlit", use_container_width=True)
with tab2:
 col1, col2 = st.columns([1, 3])
with col1:
         by_what_2 = st.radio(
            "Choose a subject score:",
            ('math_score', 'reading_score', 'writing_score'),
            key = "r2")
with col2:
 gender = ['male', 'female' ]
st.subheader("")
selected_gender = st.selectbox("Seletct gender", gender)
st.caption(f"You selected: {selected_gender}")
if selected_gender:
 filterd_data = sp[sp['gender'] == selected_gender]
chart= px.box(filterd_data,x= filterd_data['race_ethnicity'],
                  y= filterd_data[by_what_2], notched=True, points ='all', 
                  labels={"average_score": "average_score"},)
chart.update_layout(title=f"Students score in each subject of different ethnicity group in {selected_gender}",
                        xaxis_title="Race/Ethnicity", yaxis_title="Score",xaxis_tickangle=0)
chart.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                  marker_line_width=0, opacity=0.6)
st.plotly_chart(chart)
with tab3:
  average_scores = sp.groupby('race_ethnicity')[['math_score', 'reading_score', 'writing_score']].mean().reset_index()
average_scores['average_score'] = average_scores[['math_score', 'reading_score', 'writing_score']].mean(axis=1)
st.title('Top Race/Ethnicity Groups by Average Score')
top_n = st.slider('Select number of groups', 1, len(average_scores), 1)
top_groups = average_scores.nlargest(top_n, 'average_score')
fig = px.bar(top_groups, x='race_ethnicity', y='average_score', title=f"Top {top_n} Ethnicity Groups That Have Highest Average Score")
st.plotly_chart(fig)