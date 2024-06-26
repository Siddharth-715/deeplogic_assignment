"""*************LLM INTEGRATION**************"""

import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.messages import SystemMessage
from langchain.chains.conversation.memory import ConversationBufferWindowMemory

# Loading API key for Groq LLM
load_dotenv()
groq_api_key = os.environ['GROQ_API_KEY']

# Getting response from API
def llm_response(user_question, context):
    
    # Language for translation
    language = "English"

    
    model = 'llama3-8b-8192'
    # Initialize Groq Langchain chat object and conversation
    groq_chat = ChatGroq(
            groq_api_key=groq_api_key, 
            model_name=model,
            temperature=0.3,
    )
    
    # System instructions for how to answer the question based on context from documents.
    # The chatbot's answer is generated by sending the full prompt to the Groq API.

    system_prompt = f""" when no mode is specified you simply answer based on context window.
                    It is not necessary to use modes..
                    mode 0: You are a professional assistant who answer on the basis of context window and history precisely. 
                    Change everything (input, context, output, etc) into {language}.
                    You work in many modes, unless not specified clearly, you answer like a normal assitant, user has to clearly specify the mode.
                    
                    Mode 1: Start by extracting and showing entities like names, dates, locations, organizations,
                    and summarize key information from context window"
                    "Entities:\n"
                    "- Names:\n"
                    "- Dates:\n"
                    "- Locations:\n"
                    "- Organizations:\n"
                    "- Summary:\n'

                    Mode 2:Classify the following document into one of these categories: 'Business', 'Education', 'Health', 'Technology', 'Others'.
                    you can choose multiple categories """
    
    conversational_memory_length = 5 # number of previous messages the chatbot will remember during the conversation

    memory = ConversationBufferWindowMemory(k=conversational_memory_length, memory_key="chat_history", return_messages=True)


    # Chat prompt template using various components
    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                content=system_prompt
            ),  # This is the persistent system prompt that is always included at the start of the chat.

            MessagesPlaceholder(
                variable_name="chat_history"
            ),  # This placeholder will be replaced by the actual chat history during the conversation. It helps in maintaining context.

            HumanMessagePromptTemplate.from_template(
                "{human_input}"
            ),  # This template is where the user's current input will be injected into the prompt.
        ]
    )

    # Conversation chain using the LangChain LLM 
    conversation = LLMChain(
        llm=groq_chat,  # The Groq LLLM
        prompt=prompt,  # The constructed prompt template.
        verbose=False,   # TRUE Enables verbose output, which can be useful for debugging.
        memory=memory,  # The conversational memory object that stores and manages the conversation history.
    )

    # Context is appended to user's question before passing it to LLM
    user_question = user_question + " also use this extra context for answering the question "+ context
    
    return conversation.predict(human_input=user_question)


