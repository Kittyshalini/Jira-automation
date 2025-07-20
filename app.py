import streamlit as st
import helper

st.title('Jira Automation')

title = st.text_input('Enter the summary of your issue')
story_points = st.number_input('Enter the story points you want to assign')

submit = st.button('Submit')

if(submit):
    a,b,c = helper.get_data(title, story_points)
    st.write(a)
    st.write(b)
    st.write(c)
    st.write(story_points)
