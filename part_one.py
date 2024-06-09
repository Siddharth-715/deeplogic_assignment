"""*************TEXT PREPROCESSING**************"""

import io
import re
import fitz  
import pytesseract
from PIL import Image
from pdf2image import convert_from_bytes
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Text cleaning
def clean_text(text):
        # Replace multiple newlines with a single newline
        text = re.sub(r'\n+', '\n', text)
        # Replace newlines with a single space
        text = re.sub(r'\n', ' ', text)
        # Replace multiple spaces with a single space
        text = re.sub(r'\s+', ' ', text)
        # Strip leading and trailing whitespace
        text = text.strip()
        return text


# Function to extract text from PDFs
def get_pdf_text(files):
    text = ""
    for file in files:
        #reading the uploaded files in byte form
        pdf_bytes = file.read()
        pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
    
        for page_num in range(len(pdf_document)):
            
            #extracting text
            page = pdf_document[page_num]
            text += page.get_text()

            #extracting images
            image_list = convert_from_bytes(pdf_bytes, first_page=page_num + 1, last_page=page_num + 1)
        
            for image in image_list:
            
                img_byte_arr = io.BytesIO()
                image.save(img_byte_arr, format='PNG')
                img_byte_arr = img_byte_arr.getvalue()
            
                #OCR img-to-text
                text += pytesseract.image_to_string(Image.open(io.BytesIO(img_byte_arr)))
    
    return text

# Function to chunk the extracted text
def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_text(text)
    return texts

# Function to create a Chroma vector store along with embeddings
def get_vector_store(texts):
    metadatas = [{"source": f"{i}-pl"} for i in range(len(texts))]
    # Tokenization happens here
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    docsearch = Chroma.from_texts(texts, embeddings, metadatas=metadatas)
    return docsearch

# Function to get relevant data from documents 
def get_context(doc,query):

        text_list = doc.as_retriever().invoke(query)
        context = ""
        for text in text_list:
            raw_t = text.page_content
            text = clean_text(raw_t)
            context += text
        
        context = "{context window start} " + context + "{context window end} "
        return context
