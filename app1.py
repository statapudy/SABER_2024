import streamlit as st
import pandas as pd
import random
import openai
import os

# Load TERMS from CSV file
@st.cache_data
def load_terms(file_name):
    data = pd.read_csv(file_name)
    return data['TERM'].tolist()

terms = load_terms('bio_terms.csv')

# Streamlit app layout
st.title("Schema Study: An AI-enhanced study app")
st.write("Click the button below to randomly pick a relevant term from an introductory undergraduate course in ecology, evolution, and biodiversity")

# Display a random term
if st.button('Pick a term'):
    displayed_term = random.choice(terms)
    st.session_state['current_term'] = displayed_term
    st.write(displayed_term)

# Input for user's definition
definition = st.text_area("Write a simple definition of the term and anything else that you might include in a concept map of this term (500 characters max).", max_chars=500)

# Function to interact with OpenAI's API
def check_answer(term, definition):
    prompt = (
        f"You asked me to write a simple definition of \"{term}\" and anything else that you think might be important to remember if this term was on an exam. "
        f"This would include common misconceptions, case studies, examples from class, other associated terms, and any other relevant information that comes to mind when you think of this concept. "
        f"My response is \"{term}\" can be described as \"{definition}\". "
        "Provide formative feedback in a clear, succinct way. Mention any factual errors in the response. List information that was not in my response, but you would likely have placed in the answer key for this question. "
        "Do NOT use extraneous language, such as 'your answer lacks a detailed explanation'. Do not expect my response to include the term we are asked to define. Keep in mind that my response is limited to 500 characters so there is no expectation that the correct answer is more than a short paragraph. "
        "Try and keep your response within 500 characters. Do not provide advice, such as: 'Remember, the more specific and detailed your response, the better your understanding of the concept will be.' "
        "If they write anything unrelated to topics possibly covered in an undergraduate ecology, evolution, and biodiversity course, please respond with: I appreciate your question, but if you would like to take a break, might I suggest a tall glass of water and mindful relaxation."
    )

    response = openai.Completion.create(
        model="gpt-4-1106-preview",
        prompt=prompt,
        temperature=0.05,
        max_tokens=500,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    return response.choices[0].text.strip()

# Set your OpenAI API key
openai.api_key = 'OPENAI_API_KEY'

# Button to check the answer
if st.button('Click here to check answer'):
    feedback = check_answer(st.session_state.get('current_term', ''), definition)
    st.write(feedback)

# Contact information and other UI elements
st.write("Questions? Thoughts? Email Keefe Reuther at kdreuther@ucsd.edu")
st.markdown("[Lab Website](https://reutherlab.biosci.ucsd.edu)")

# Note: Add your OpenAI API key and other specific configurations as required.
