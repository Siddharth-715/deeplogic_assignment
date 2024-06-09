"""**************CHAT BOT UI*****************"""

import os
import streamlit as st
from part_one import (get_context, get_pdf_text , get_text_chunks , get_vector_store)
from part_two import llm_response
from dotenv import load_dotenv



def main():

    # Logo Url
    load_dotenv()
    logo_url = os.environ['logo_url']

    # Title and header
    st.set_page_config(page_title="Chat PDF")
    st.image(logo_url, width=300)
    st.header("DeepLogic AI Assignment")

    # Project link
    url = "https://github.com/Siddharth-715/deeplogic_assignment"

    
    user_question = st.text_input("Ask a Question from the PDF Files. ")
    if user_question:
            docsearch = st.session_state["docsearch"]
            context = get_context(docsearch, user_question)
            st.write(llm_response(user_question, context))

    with st.sidebar:
        st.title("Menu")
        pdf_docs = st.file_uploader("Upload your PDF Files and Click on the Submit & Process Button", accept_multiple_files=True)
        if pdf_docs:
            if st.button("Submit & Process"):
                with st.spinner("Processing..."):
                    raw_text = get_pdf_text(pdf_docs)
                    text_chunks = get_text_chunks(raw_text)
                    docsearch = get_vector_store(text_chunks)
                    st.session_state["docsearch"] = docsearch
                    st.success("Processing Done")
                
    st.write("Check this out on [Github](%s)" % url)
    

if __name__ == "__main__":
    main()
