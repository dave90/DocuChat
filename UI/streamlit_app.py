import streamlit as st
from streamlit_chat import message
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space
import os
import requests

st.set_page_config(page_title="DocuChat - An LLM-powered Streamlit app")
agent_host = os.environ["AGENT_SERVICE_NAME"]
agent_port = os.environ["AGENT_SERVICE_PORT"]


# Response output
## Function for taking user prompt as input followed by producing AI generated responses
def generate_response(prompt):
    #agent_vector_url = f"http://{agent_host}:{agent_port}/agent/query"
    agent_vector_url = f"http://{agent_host}:{agent_port}/query"
    print(f"Send to Agent: {agent_vector_url} ")
    print("Prompt: ",prompt)
    response = requests.post(agent_vector_url, json={"text": prompt})
    res_json = response.json()

    return (res_json["response"],res_json["context"] )

def submit():
    st.session_state.input_text = st.session_state.input
    print("HELLO")
    print(st.session_state.input_text)
    st.session_state.input = ''

# User input
## Function for taking user provided prompt as input
def get_text():
    input_text = st.text_input("You: ", value="", key="input",on_change=submit)
    return input_text


with st.sidebar:
    st.title('🤗💬 Docuchat App')
    st.markdown('''
    ## About
    This app is an LLM-powered chatbot built using:
    - [Streamlit](<https://streamlit.io/>)
    - [LangChain](<https://python.langchain.com/en/latest/index.html>)

    ''')
    add_vertical_space(5)
    st.write('Made with ❤️')


if 'generated' not in st.session_state:
    st.session_state['generated'] = ["I'm HugChat, How may I help you?"]

if 'context' not in st.session_state:
    st.session_state['context'] = {}


if 'past' not in st.session_state:
    st.session_state['past'] = []

if "input_text" not in st.session_state:
    st.session_state['input_text'] = ''


input_container = st.container()
colored_header(label='', description='', color_name='blue-30')
response_container = st.container()

## Applying the user input box
with input_container:
    user_input = get_text()



## Conditional display of AI generated responses as a function of user provided prompts
with response_container:
    input_text = st.session_state.input_text

    if input_text:
        print("GETTING")
        print(input_text)
        response, context = generate_response(input_text)
        st.session_state.past.append(input_text)
        generate_id = len(st.session_state.generated)
        st.session_state.generated.append(response)
        st.session_state.context[generate_id] = context

    if st.session_state['generated']:
        gen_size = len(st.session_state['generated'])
        past_size = len(st.session_state['past'])
        for i in range(gen_size):
            message(st.session_state['generated'][gen_size-i-1], key=str(i))
            if gen_size-i-1 in st.session_state['context']:
                print("Context: ",st.session_state['context'][gen_size-i-1])
                with st.expander("See explanation"):
                    st.write("Context of the generated response:")
                    st.code(f"""
                    {st.session_state['context'][gen_size-i-1]}
                    """)
            if i < past_size:
                message(st.session_state['past'][past_size-i-1], is_user=True, key=str(i) + '_user')
