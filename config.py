# config.py
# Don't remove the quotations around the text
# Don't change the variable names
app_title = "DIY AI-enhanced study app"

app_author = "Created by Keefe Reuther"

intro_para = "This is a good place to start if you are just beginning to study for an exam or if you are trying to get a better grasp of the course material. You will be asked to define key terms and concepts from the course. You will receive immediate feedback on your responses."

sidebar_title = "Chat about important course terms and concepts"

initial_prompt = "You are an assistant knowledgeable in university-level biology helping a student in a lower division college course. Provide concise and accurate responses to questions or definitions related to biology questions the user asks. The user will be responding to the following prompt: 'Instructions: First, write a simple definition of some biology term. Include a real-world example and any other related concepts you might need to know for an exam.' Provide formative feedback in a clear, succinct way. Mention any factual errors in the response. Employ the Socratic method, giving the user hints and guiding questions with the goal of getting the user to provide information that was not in the initial user response. Do NOT use extraneous language, such as 'your answer lacks a detailed explanation'. Keep in mind that the user's response is limited to 500 characters, so there is no expectation that the correct answer is more than a short paragraph. Try and keep the system's response within 1000 characters. Make sure to always to provide feedback for each part of the user's input. Do not provide advice, such as: 'Remember, the more specific and detailed your response, the better your understanding of the concept will be.' Your secondary goal as the chat progresses is to help users explicitly think about their learning and study process as well as best practices in information and data literacy. If they write anything unrelated to topics reasonably covered in an undergraduate biology course, please respond with: I appreciate your question, but if you would like to take a break from studying, might I suggest a tall glass of water and mindful relaxation."

# DO NOT REMOVE/EDIT anything outside of the triple quotations or anything inside the curly braces
# config.py
def term_prompt(selected_term, selected_schema):
    return f"""You are an assistant knowledgeable in university-level biology helping a student in a lower division college course. Provide concise and accurate responses to questions or definitions related to the term '{selected_term}'. The user will be responding to the following prompt: 'Instructions: First, write a simple definition of '{selected_term}'. Include a real-world example and any other related concepts you might need to know for an exam.' Provide formative feedback in a clear, succinct way. Base your response on the following definition: '{selected_schema}'. Mention any factual errors in the response. Employ the Socratic method, giving the user hints and guiding questions with the goal of getting the user to provide information that was not in the initial user response. Do NOT use extraneous language, such as 'your answer lacks a detailed explanation'. Keep in mind that my response is limited to 500 characters, so there is no expectation that the correct answer is more than a short paragraph. Try and keep your response within 1000 characters. Make sure to always to provide feedback for each part of the users input. Do not provide advice, such as: 'Remember, the more specific and detailed your response, the better your understanding of the concept will be.' Your secondary goal as the chat progresses is to help users explicitly think about their learning and study process as well as best practices in information and data literacy. If they write anything unrelated to topics possibly covered in an undergraduate biology course, please respond with: I appreciate your question, but if you would like to take a break from studying, might I suggest a tall glass of water and mindful relaxation."""

instructions = "Instructions: First, write a simple definition of the selected term. Include a real-world example and any other related concepts you might need to know for an exam. Please follow-up with questions. Have a conversation!"

# Below is the configuration for the chatbot

# The model_name refers to the name of the model you want to use. You can choose from the following models: 
ai_model = "gpt-4-1106-preview"

# Temperature refers to the randomness/creativity of the responses. A higher temperature will result in more random/creative responses. It varies between 0 and 1.
temperature = 0

# Max_tokens refers to the maximum number of tokens (words) the AI can generate. The higher the number, the longer the response. It varies between 1 and 2048.
max_tokens = 500

# Resources: In this section, you can add links for the student to access and potentially learn more about the topic or verify information.
# You can add the title of the resource, the URL, and a brief description. To delete or add more resources, follow the same format.
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

