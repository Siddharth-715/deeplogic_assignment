# deeplogic_assignment
This repository contains a pipeline for processing documents, especially invoice/receipt PDFs with text and image content. It uses OCR and LLMs to extract key information (like key-value pairs) and enables user interaction through a chatbot interface. Supports document classification and translation.

## Description

The project is divided into three main parts: Part One (Document Conversion, OCR, and Preprocessing); Part Two (LLM-Powered Understanding and Actions); and Part Three (User Interaction via a Chatbot Interface).

### Part 1: Document Conversion, OCR, and Preprocessing

**Document Conversion**: Converts PDF documents into a standardized format (e.g., .TXT) suitable for LLM processing. Uses Fitz(By PyMuPDF) for simple text extraction. It is simple and efficient and highly accurate.

**OCR Integration**: Identifies and extracts text from images within documents using OCR engine provided by *pytesseract*. This engine first takes _byte_stream_ of pdf, extracts images from it and then performs OCR to extract text append it to previous text.

**Preprocessing**: Prepares the extracted text for optimal LLM performance by cleaning text, removing whitespaces  and turning tokens inot _embeddings_. Uses *Ollama Embeddings* for creating embedding vectors from processed text and *Chroma DB* to store the embedding vectors. Both are chosen for their speed and accuracy. 
  
  The nomic-embed-text embedding model used here, is known for surrpassing OpenAI embedding for short contexts especially.
  
  The ChromaDB is popular for fast vector similarity searches and ease of use. 
  
  Later when user gives an input question, the question itself is embedded into vector embeddings and a simillarity search is performed to get the most relvant document pieces, which is provided to LLM into next part as context.

### Part 2: LLM-Powered Understanding and Actions

**LLM Integration**: Integrates a Large Language Model into the pipeline. Groq was preferred because it currently holds the title of _Fastest infrencing LLM_ utilizing LPUs (Language Processing Unit) which perfoms better than its contempary counterparts. In this project we can use either from _llama3-8b-8192_ or _mixtral-8x7b-32768_, both provide good answers but Llama3 proves to be more generalized and better suited to general use-caeses.

**Information Extraction**: Extracts essential information such as entities (names, dates, locations, organizations), relationships between entities, and key information summaries. Implemented as Mode 1, to use just mention it chat prompt.

**Document Classification**: Classifies documents into predefined categories based on content. Implemented as Mode 2, to use just mention it chat prompt.

**Internal Translation**: Translates text within documents into different languages using the LLM. 

### Part 3: User Interaction via a Chatbot Interface

**Chatbot UI**: Creates a user-friendly chatbot interface using Streamlit for user interaction with the LLM and processed documents. Users can upload multiple PDFs with a simple _drag & drop_, ask questions, request specific information, review extracted data, and provide feedback. 
![UI screenshot](https://drive.google.com/file/d/1AXxHdCl7AGyRqPg8_Mv2jYcIqYAdCJXY/view?usp=drive_link)
**Pipeline Integration**: We used _LangChain_ for pipeline, to integrate LLMs, Chat prompts, Vector Store and Memory Buffer. 

## Getting Started

### Dependencies

Start by installing the following dependecis:

```python
fitz==0.0.1.dev2
groq==0.8.0
langchain==0.2.3
langchain_community==0.2.4
langchain_core==0.2.5
langchain_groq==0.1.5
llama_index==0.10.43
pdf2image==1.17.0
Pillow==9.0.1
pytesseract==0.3.10
python-dotenv==1.0.1
streamlit==1.24.0
```

or by simply executing:
```bash
$ pip install -r requirements.txt
```

### Executing program

Clone the repsository into your pc:
```bash
git clone https://github.com/your-username/document-processing-pipeline.git
cd document-processing-pipeline
```

Then install the required dependencies via:
```bash
pip install -r requirements.txt
```
Now create a **.env** file in the same directory and intialize secret keys as follows:
```python
GROQ_API_KEY = "<YOUR_GROQ_API_KEY>"
logo_url = "<YOUR_LOGO_IMAGE_URL>"
```

After installing dependencies, run the _part_three.py_, 
```python
python3 ./part_three.py
```

Now lauch the streamlit app by command:
```python
streamlit run "/path/to/python/file/part_three.py"
```


## Authors

Contributors names and contact info
Siddharth Singh Patel 
patelsiddharth715@gmail.com


## License

This project is licensed under the  License - see the LICENSE.md file for details

