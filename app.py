import streamlit as st
import hmac
import pandas as pd
import random
import os
import time
import base64
import logging
import io
import config
from openai import OpenAI

def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False

    # Return True if the password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show input for password.
    st.text_input(
        "Password", type="password", on_change=password_entered, key="password"
    )
    if "password_correct" in st.session_state:
        st.error("😕 Password incorrect")
    return False

if not check_password():
    st.stop()  # Do not continue if check_password is not True.

# Set up logging
logging.basicConfig(level=logging.DEBUG, filename='app_log.log', filemode='w',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Creating a download link for a file
# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806/2
def create_download_link(file_path, file_name):
    try:
        with open(file_path, "rb") as file:
            file_content = file.read()
        encoded_content = base64.b64encode(file_content).decode("utf-8")
        download_link = f'<a href="data:file/csv;base64,{encoded_content}" download="{file_name}">Download {file_name}</a>'
        return download_link
    except FileNotFoundError:
        error_message = f"The file {file_name} was not found."
        st.error(error_message)
        logging.exception(error_message)
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        st.error(error_message)
        logging.exception(error_message)

# Load terms from a CSV file
# https://discuss.streamlit.io/t/how-to-upload-a-csv-file/7052/2
def load_terms(file_input):
    try:
        if isinstance(file_input, str):
            data = pd.read_csv(file_input)
        else:
            data = pd.read_csv(io.StringIO(file_input.read().decode('utf-8')))
        return data
    except Exception as e:
        st.error(f"An error occurred while loading the file: {str(e)}")
        logging.exception(f"Error loading file: {e}")

# Set the page to wide mode
st.set_page_config(layout="wide")

# Set custom styles
def set_custom_styles():
    st.markdown("""
    <style>
    /* Custom font size for specific markdown lines */
    .markdown-font-large {
        font-size: 14pt;  /* Adjust the size as needed */
    }

    /* [Other styles] */
    </style>
    """, unsafe_allow_html=True)

set_custom_styles()

# Streamlit app layout
# col1, col2 = st.columns([1,5])
st.title(config.app_title)
st.write(config.app_author)
st.markdown(config.intro_para)
st.markdown('<br>', unsafe_allow_html=True)
st.sidebar.title(config.sidebar_title)

# Set a seed for random number generation
random_seed = 25
random.seed(random_seed)

# Download link for the template file
template_file_path = "terms_template.csv"
st.sidebar.markdown("If you want to use your own terms, download this template file. Be sure to save the file as a CSV and not edit the first row.")
st.sidebar.markdown(create_download_link(template_file_path, "terms_template.csv"), unsafe_allow_html=True)

# File Uploader
uploaded_file = st.sidebar.file_uploader("Choose a text file with terms")
if uploaded_file is not None:
    logging.info(f"File uploaded: {uploaded_file.name}")
    st.session_state.uploaded_file = uploaded_file

# Load terms from the file
if 'uploaded_file' in st.session_state and st.session_state.uploaded_file is not None:
    terms = load_terms(st.session_state.uploaded_file)
else:
    terms = load_terms(template_file_path)

# Function to select a random term and its schema
def select_random_term_and_schema(terms_df, counter):
    if not terms_df.empty and 'TERM' in terms_df.columns and 'SCHEMA' in terms_df.columns:
        random.seed(counter)
        selected_row = terms_df.sample()
        selected_term = selected_row['TERM'].values[0]
        selected_schema = selected_row['SCHEMA'].values[0]
        return selected_term, selected_schema
    else:
        return None, None
    

# Display the instructions
st.markdown('<div class="markdown-font-large">Click the button below to randomly pick a term</div>', unsafe_allow_html=True)

# Line Break
st.markdown('<br>', unsafe_allow_html=True)

# Define a basic initial context at the beginning of your script
initial_context = {
    "role": "system",
    "content": config.initial_prompt
}

# Initialize the session state variables for selected term, schema, and display messages
if 'selected_term' not in st.session_state:
    st.session_state.selected_term = None
if 'selected_schema' not in st.session_state:
    st.session_state.selected_schema = None
if 'display_messages' not in st.session_state:
    st.session_state.display_messages = [initial_context]

# Initialize session states for the selected term, counter, and display flag
if 'selected_term' not in st.session_state:
    st.session_state.selected_term = None
if 'term_click_counter' not in st.session_state:
    st.session_state.term_click_counter = 0
if 'display_term' not in st.session_state:
   st.session_state.display_term = False

# Toggle term display and select a new term if needed
if st.button('Click to pick a term'):
    st.session_state.term_click_counter += 1
    selected_term, selected_schema = select_random_term_and_schema(terms, st.session_state.term_click_counter)
    st.session_state.selected_term = selected_term
    st.session_state.selected_schema = selected_schema
    st.session_state.display_term = True

    # Update the initial context with dynamic content
    updated_prompt = config.term_prompt(st.session_state.selected_term, st.session_state.selected_schema)
    initial_context = {
        "role": "system", 
        "content": updated_prompt}

    # Reset the conversation with the new initial context
    st.session_state.display_messages = [initial_context]

# Display the term if the condition is met
if st.session_state.display_term and st.session_state.selected_term:
    st.header(st.session_state.selected_term)
    # Pass the displayed term to the assistant as part of the message
    user_message = f"Define '{st.session_state.selected_term}':"
elif not st.session_state.selected_term:
    st.write("Please click the button to begin")

st.markdown('<hr>', unsafe_allow_html=True)

#print("DataFrame:", terms)
#print("Selected Term:", st.session_state.selected_term)

#####OPENAI CHAT####

# Initialize the OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Initialize the session state variables if they don't exist
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = config.ai_model

if "display_messages" not in st.session_state:
    st.session_state.display_messages = [initial_context]

# Display the messages
st.markdown(config.instructions)

# Input for new messages
if prompt := st.chat_input("Type your message here..."):
    # Insert initial_context here
    if not st.session_state.display_messages:
        st.session_state.display_messages.append(initial_context)

    st.session_state.display_messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            for response in client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.display_messages
                ],
                stream=True,
                temperature=config.temperature,
                max_tokens=config.max_tokens,
            ):
                full_response += (response.choices[0].delta.content or "")
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
    st.session_state.display_messages.append({"role": "assistant", "content": full_response})

# Line Break
st.markdown('<br>', unsafe_allow_html=True)

# Display the messages
st.markdown('<div class="markdown-font-large"><em>ChatGPT can make errors and does not replace verified and reputable online and classroom resources.</em></div>', unsafe_allow_html=True)

st.sidebar.markdown("Online Resources")
for resource in config.resources:
    with st.sidebar:
        st.markdown(f"### [{resource['title']}]({resource['url']})")
        st.write(resource['description'])

# Footer
with st.sidebar:
    st.markdown("---")

    st.markdown("""
        The template for this app was created by Keefe Reuther and the members of the Reuther Lab - [https://reutherlab.biosci.ucsd.edu/](https://reutherlab.biosci.ucsd.edu/)
    """)
    st.markdown("""
        It can be found at [https://github.com/The-Reuther-Lab/SABER_2024](https://github.com/The-Reuther-Lab/SABER_2024) 
        and is distributed under the GNU GPL-3 License.
    """)

