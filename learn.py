import streamlit as st
import numpy as np
import pandas as pd
import time
from streamlit import text_input, cache_data

st.sidebar.title('Schema Study: An AI-enhanced study app')

if "counter" not in st.session_state:
    st.session_state.counter = 0

st.session_state.counter += 1

st.header(f"This page has run {st.session_state.counter} times.")
st.button("Run it again")

x = st.slider('x')  # 👈 this is a widget
st.write(x, 'squared is', x * x)

# Check if 'name' is not in session_state, then initialize it
if 'name' not in st.session_state:
    st.session_state.name = 'Keefe'  # Replace 'default_value' with a suitable initial value

# Create a text input box with 'Keefe' as the default value
# The value is updated in session_state when the user inputs a new name
st.session_state.name = st.text_input('Enter your name:', st.session_state.name)

# Display a greeting message using the name
st.write(f"Hello, {st.session_state.name}!")

st.write("There are a few common scenarios where Session State is helpful. As demonstrated above, Session State is used when you have a progressive process that you want to build upon from one rerun to the next. Session State can also be used to prevent recalculation, similar to caching. For example, if you have a long-running computation that you want to run only once, you can use Session State to keep track of whether the computation has already been run. Finally, Session State can be used to keep track of widget state. For example, if you have a widget that you want to update based on another widget, you can use Session State to keep track of the state of the first widget.")

st.write("Every widget with a key is automatically added to Session State. For more information about Session State, its association with widget state, and its limitations, see Session State API Reference Guide.")

option = st.sidebar.selectbox(
    'Schema Study Level',
    ['1 - Understanding Course Concepts', 
     '2 - Connecting Course Concepts', 
     '3 - Creating a Concept Map'])

#Part 1: Understanding Course Concepts

if option == '1 - Understanding Course Concepts':
    st.write('1 - Understanding Course Concepts')
    st.write('This is a good place to start if you are just beginning to study for an exam or if you are trying to get a better grasp of the course material. You will be asked to define key terms and concepts from the course. You will receive immediate feedback on your responses and will be able to see how your responses compare to the responses of other students.')

#Part 2: Connecting Course Concepts
    
elif option == '2 - Connecting Course Concepts':
    st.write('2 - Connecting Course Concepts')
    st.write('This is a good place to start if you are just beginning to study for an exam or if you are trying to get a better grasp of the course material. You will be asked to define key terms and concepts from the course. You will receive immediate feedback on your responses and will be able to see how your responses compare to the responses of other students.')    

#Part 3: Creating a Concept Map
    
else:    
    st.write('3 - Creating a Concept Map')
    st.write('This is a good place to start if you are just beginning to study for an exam or if you are trying to get a better grasp of the course material. You will be asked to define key terms and concepts from the course. You will receive immediate feedback on your responses and will be able to see how your responses compare to the responses of other students.')

left_column, right_column = st.columns(2)

with right_column:
    chosen = st.radio(
        'Sorting hat',
        ("Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"))
    st.write(f"You are in {chosen} house!")

with left_column:
    if "dataframe" not in st.session_state:
        st.session_state.dataframe = pd.DataFrame(
            np.random.randn(10, 20),
            columns=('col %d' % i for i in range(20)))
        
    st.dataframe(st.session_state.dataframe)

if st.checkbox('Show Map'):
    map_data = pd.DataFrame(np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])
    
    st.map(map_data)

