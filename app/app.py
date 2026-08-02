import subprocess

from dotenv import load_dotenv
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama


def pull_model(model_name: str) -> tuple[bool, str]:
    """
    Download a model from Ollama.

    Returns:
        Tuple of (success: bool, message: str)
    """
    try:
        process = subprocess.run(
            ["ollama", "pull", model_name],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )

        if process.returncode == 0:
            return True, f"Successfully installed {model_name}"
        else:
            return False, f"Error pulling {model_name}: {process.stderr}"

    except Exception as e:
        return False, f"Error downloading {model_name}: {str(e)}"


# ollama models
if "ollama_models" not in st.session_state:
    st.session_state.ollama_models = ["llama3.2:1b", "gemma3:270m"]

    for mdl in st.session_state.ollama_models:
        pull_model(mdl)


# load the env variables
load_dotenv()

# streamlit page setup
st.set_page_config(
    page_title="Foodbot",
    page_icon="🍕",
    layout="centered",
)

st.title("🍕 Chef-Bot 🍕")
st.text("""\
I can help you plan your weekly meals. \
If you have any ingredients that you want to use, please let me know and we can plan accordingly!"
""")
# give option to choose from Ollama or OpenAI models
option = st.selectbox(
    "Choose your LLM provider",
    ("Ollama", "OpenAI"),
)

# choose a model from the chosen provider
if option == "OpenAI": 
    model = st.selectbox(
        "Choose the model from OpenAI",
        ["gpt-5.4-mini"]
    )
else:
    model = st.selectbox(
        "Choose the model from Ollama",
       st.session_state.ollama_models
    )

# initiate chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# show chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# llm initiate
if option == "OpenAI":
    llm = ChatOpenAI(
        model=model,
        temperature=0.7,  # add 70% creativity
    )

else:
    llm = ChatOllama(
            model=model,
            temperature=0.7,  # add 70% creativity
    )

# input box
user_prompt = st.chat_input("Ask Chef-Bot...")

if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    response = llm.invoke(
        input = [
            {
                "role": "system", 
                "content": """\
                You are a professional chef helping to give dinner ideas based on
                the input provided. If the user shares some available ingredients, 
                these should be used only once throughout the whole week.
                
                The output should be a link to a recipe that can be followed.

                Give 1 to 3 options per day of the week.

                If the question is not related to meal planning, simply reply 
                'I am a meal planner, please ask me about that instead.'.
                """
            }, 
            *st.session_state.chat_history
        ]
    )
    assistant_response = response.content
    st.session_state.chat_history.append(
        {"role": "assistant", "content": assistant_response}
    )

    with st.chat_message("assistant"):
        st.markdown(assistant_response)
