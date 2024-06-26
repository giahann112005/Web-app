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
    st.markdown("**HỨA NGUYỄN GIA HÂN**")
    st.write("Date: ", datetime.date(2024, 5, 30))
    st.text("Description: This project understands how the student's performance (test scores) is affected by other variables such as Gender, Ethnicity, Parental level of education, Lunch and Test preparation course.")

with st.container():
    st.subheader("")
    st.title("x")
    st.write("x" ) 

st.title("Score")
st.markdown("I analyze the :blue[relationship between score and other variables] in :red[student study performance] data set available on the internet")

st.divider()

sp = pd.read_csv('C:/Users/vyvil/Documents/study_performance.csv')

st.header("Original data set")

st.text("This is a data frame with 1,000 observations on 9 variables.")

st.markdown(
"""
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

st.header("Average score of three subjects in each variables")
st.text("")

tab1, tab2, tab3, tab4 = st.tabs(["Pie Chart", "Box Chart", "Bar Chart", "Scatter Chart"])
with tab1:
 by_what_1 = st.radio(
            "Choose a category:",
            ('lunch', 'gender', 'test_preparation_course','parental_level_of_education'), horizontal=True,
            key = "r1")
 sp['average_score'] = sp.apply(lambda row:(row.math_score + row.reading_score + row.writing_score) / 3, axis = 1)
fig1 = px.pie(sp, values = "average_score", names = by_what_1, hole = 0.7) 
fig1.update_traces(text = sp[by_what_1], textposition = "outside")
st.plotly_chart(fig1, theme = "streamlit", use_container_width=True)
with tab2:
 by_what_2 = st.radio(
            "Choose a subject score:",
            ('math_score', 'reading_score', 'writing_score'), 
            horizontal = True,
            key = "r2")
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
  average_scores = sp.groupby('parental_level_of_education')[['math_score', 'reading_score', 'writing_score']].mean().reset_index()
average_scores['average_score'] = average_scores[['math_score', 'reading_score', 'writing_score']].mean(axis=1)
st.title('Top Groups by Average Score')
top_n = st.slider('Select number of groups', 1, len(average_scores), 1)
top_groups = average_scores.nlargest(top_n, 'average_score')
fig = px.bar(top_groups, x='parental_level_of_education', y='average_score', title=f"Top {top_n} Groups That Have Highest Average Score")
st.plotly_chart(fig)
with tab4:
  st.sidebar.header('Filter Options')
gender = st.sidebar.multiselect('Gender', options=sp['gender'].unique(), default=sp['gender'].unique())
race_ethnicity = st.sidebar.multiselect('Race/Ethnicity', options=sp['race_ethnicity'].unique(), default=sp['race_ethnicity'].unique())
parental_level_of_education = st.sidebar.multiselect('Parental Level of Education', options=sp['parental_level_of_education'].unique(), default=sp['parental_level_of_education'].unique())
lunch = st.sidebar.multiselect('Lunch', options=sp['lunch'].unique(), default=sp['lunch'].unique())
test_preparation_course = st.sidebar.multiselect('Test Preparation Course', options=sp['test_preparation_course'].unique(), default=sp['test_preparation_course'].unique())

# Filter the data based on user input
filtered_data = sp[
    (sp['gender'].isin(gender)) &
    (sp['race_ethnicity'].isin(race_ethnicity)) &
    (sp['parental_level_of_education'].isin(parental_level_of_education)) &
    (sp['lunch'].isin(lunch)) &
    (sp['test_preparation_course'].isin(test_preparation_course))
]

# Create an Altair chart
chart = alt.Chart(filtered_data).mark_circle(size=60).encode(
    x='math_score',
    y='reading_score',
    color='writing_score',
    tooltip=['gender', 'race_ethnicity', 'parental_level_of_education', 'lunch', 'test_preparation_course', 'math_score', 'reading_score', 'writing_score']
).interactive()

# Display the chart in the Streamlit app
st.altair_chart(chart, use_container_width=True)
