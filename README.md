# Practice Exercise – Build a Multi-Model Chatbot

## Task

Build a conversational chatbot in Streamlit where the user can:

1. Select the provider (OpenAI, Gemini, Groq, or Ollama).
2. Choose from the available models under that provider.
3. Chat with the selected model in a simple conversational interface.

## Suggested Steps

1. Set up Streamlit app (app.py)

    - Add a dropdown (select box) for the provider.
    - Based on the provider, show another dropdown with available models (for example:
        - OpenAI → gpt-3.5-turbo, gpt-4.1
        - Gemini → gemini-2.5-pro, gemini-2.5-flash
        - Groq → llama-3.1-8b-instant, llama-3.3-70b-versatile
        - Ollama → gemma3, llama3.1).

2. Create chat input and history

    - Add a text input box for the user’s message.
    - Maintain a chat history in session state so the conversation context is preserved.

3. Send query to selected model

    - Call the correct function depending on provider and model.
    - Append the response to the chat history.

4. Display conversation

    - Show both user and chatbot messages in the UI, in a chat-like format.

## What you will practice

- Creating a chatbot UI in Streamlit
- Allowing users to choose provider and model dynamically
- Maintaining multi-turn conversation history
- Handling different APIs and local models in a single app

👉 Once complete, you can push this chatbot to Streamlit Cloud and test it online.