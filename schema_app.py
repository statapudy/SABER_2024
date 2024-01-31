import streamlit as st
import pandas as pd
import random
import os
import time
import base64
import logging
import io
from openai import OpenAI

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
col1, col2 = st.columns([1,5])
col2.title('Schema Study: An AI-enhanced study app')
col1.image("static/logolight.png", width=80)
st.write("Created by Keefe Reuther")
st.markdown('<div class="markdown-font-large">This is a good place to start if you are just beginning to study for an exam or if you are trying to get a better grasp of the course material. You will be asked to define key terms and concepts from the course. You will receive immediate feedback on your responses.</div>', unsafe_allow_html=True)
st.markdown('<br>', unsafe_allow_html=True)
st.sidebar.title('Chat about important course terms and concepts')

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
    "content": "You are an assistant knowledgeable in university-level biology helping a student in a lower division college course. Provide concise and accurate responses to questions or definitions related to biology questions the user asks. The user will be responding to the following prompt: 'Instructions: First, write a simple definition of some biology term. Include a real-world example and any other related concepts you might need to know for an exam.' Provide formative feedback in a clear, succinct way. Mention any factual errors in the response. Employ the Socratic method, giving the user hints and guiding questions with the goal of getting the user to provide information that was not in the initial user response. Do NOT use extraneous language, such as 'your answer lacks a detailed explanation'. Keep in mind that my response is limited to 500 characters, so there is no expectation that the correct answer is more than a short paragraph. Try and keep your response within 1000 characters. Make sure to always to provide feedback for each part of the users input. Do not provide advice, such as: 'Remember, the more specific and detailed your response, the better your understanding of the concept will be.' Your secondary goal as the chat progresses is to help users explicitly think about their learning and study process as well as best practices in information and data literacy. If they write anything unrelated to topics possibly covered in an undergraduate biology course, please respond with: I appreciate your question, but if you would like to take a break from studying, might I suggest a tall glass of water and mindful relaxation."
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

    # Update the initial context with the new selected term
    initial_context = {
        "role": "system",
        "content": f"You are an assistant knowledgeable in university-level biology helping a student in a lower division college course. Provide concise and accurate responses to questions or definitions related to the term '{st.session_state.selected_term}'. The user will be responding to the following prompt: 'Instructions: First, write a simple definition of '{st.session_state.selected_term}'. Include a real-world example and any other related concepts you might need to know for an exam.' Provide formative feedback in a clear, succinct way. Base your response on the definitions provided: '{st.session_state.selected_schema}'. Mention any factual errors in the response. Employ the Socratic method, giving the user hints and guiding questions with the goal of getting the user to provide information that was not in the initial user response. Do NOT use extraneous language, such as 'your answer lacks a detailed explanation'. Keep in mind that my response is limited to 500 characters, so there is no expectation that the correct answer is more than a short paragraph. Try and keep your response within 1000 characters. Make sure to always to provide feedback for each part of the users input. Do not provide advice, such as: 'Remember, the more specific and detailed your response, the better your understanding of the concept will be.' Your secondary goal as the chat progresses is to help users explicitly think about their learning and study process as well as best practices in information and data literacy. If they write anything unrelated to topics possibly covered in an undergraduate biology course, please respond with: I appreciate your question, but if you would like to take a break from studying, might I suggest a tall glass of water and mindful relaxation."
    }

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
    st.session_state["openai_model"] = "gpt-4-1106-preview"

if "display_messages" not in st.session_state:
    st.session_state.display_messages = [initial_context]

# Display the messages
st.markdown('<div class="markdown-font-large">Instructions: First, write a simple definition of the selected term. Include a real-world example and any other related concepts you might need to know for an exam. Please follow-up with questions. Have a conversation!</div>', unsafe_allow_html=True)

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
                temperature=0,
                max_tokens=500
            ):
                full_response += (response.choices[0].delta.content or "")
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
    st.session_state.display_messages.append({"role": "assistant", "content": full_response})

# Line Break
st.markdown('<br>', unsafe_allow_html=True)

# Display the messages
st.markdown('<div class="markdown-font-large"><em>ChatGPT can make errors and does not replace verified and reputable online and classroom resources.</em></div>', unsafe_allow_html=True)


# Links and descriptions
resources = [
    {
        "title": "Evolution 101 - UC Berkeley",
        "url": "https://evolution.berkeley.edu/evolution-101/",
        "description": "A comprehensive guide to the basics of evolution, covering key concepts, history of life, and evolutionary mechanisms."
    },
    {
        "title": "Understanding Evolution - UC Berkeley",
        "url": "https://evolution.berkeley.edu/",
        "description": "A one-stop resource for in-depth information on evolution, designed to enhance understanding of what evolution is and how it works."
    },
    {
        "title": "Khan Academy - Biology",
        "url": "https://www.khanacademy.org/science/biology",
        "description": "Offers a wide range of biology topics with easy-to-understand video tutorials and practice exercises for undergraduate students."
    },
    {
        "title": "NCBI Bookshelf - Biology",
        "url": "https://www.ncbi.nlm.nih.gov/books/",
        "description": "A collection of biology books and literature available online for free, suitable for in-depth study in various biology areas."
    },
    {
        "title": "OpenStax - Biology",
        "url": "https://openstax.org/details/books/biology",
        "description": "Provides free, peer-reviewed, openly licensed textbooks for introductory college and AP-level biology courses."
    },
    {
        "title": "Learn Genetics - Utah",
        "url": "https://learn.genetics.utah.edu/",
        "description": "An interactive resource offering educational materials on genetics, bioscience, and health topics. Perfect for students and educators looking for comprehensive genetics and bioscience information."
    },
    {
        "title": "Scitable by Nature Education",
        "url": "https://www.nature.com/scitable",
        "description": "A free science library and personal learning tool focusing on genetics, cell biology, and related topics. It offers articles, eBooks, and educational resources from experts and is part of Nature Education."
    }
]

st.sidebar.markdown("Online Resources")
for resource in resources:
    with st.sidebar:
        st.markdown(f"### [{resource['title']}]({resource['url']})")
        st.write(resource['description'])

# Footer
with st.sidebar:
    st.markdown("---")

    st.markdown("""
        This app is managed by Keefe Reuther - [https://reutherlab.biosci.ucsd.edu/](https://reutherlab.biosci.ucsd.edu/)
    """)
    st.markdown("""
        It can be found at [https://github.com/keefereuther/bioapp_streamlit](https://github.com/keefereuther/bioapp_streamlit) 
        and is distributed under the GNU GPL-3 License.
    """)

