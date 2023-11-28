import streamlit as st
from PyPDF2 import PdfReader
import re
import os
from dotenv import load_dotenv
from getpass import getpass

from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate


# load_dotenv()

# ---CONSTANTS----
OPEN_AI_API_KEY = "YOUR_API_KEY_HERE"

# ---CONSTANTS----

q_a_dict_ai = {}
q_a_dict_student = {}

template = """Question: {question}

Answer: Let's think step by step."""

prompt = PromptTemplate(template=template, input_variables=["question"])
llm = OpenAI(api_key=OPEN_AI_API_KEY)

llm_chain = LLMChain(prompt=prompt, llm=llm)
question = ""



def get_pdf_text(pdf_docs):
    # TODO: add a handwriting recognising API here for handwritten documents
    text_array = []
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in range(len(pdf_reader.pages)):
            page_obj = pdf_reader.pages[page]
            text_array.append(page_obj.extract_text())
    return text_array


def home():
    st.set_page_config(page_title="Eduboost", page_icon=":books:")
    st.header("Pdf reader :book:")

    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader("Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
    if st.button("Process"):
        with st.spinner("Processing..."):
            raw_text = get_pdf_text(pdf_docs)
            questions_student = []
            answers_student = []
            for i in raw_text:
                text_chunks = re.split('\d+' + "." + "\n", i)
                text_chunks.pop(0)
                text_chunks = [i.replace("\n", " ") for i in text_chunks]
                if raw_text.index(i) == 0:
                    for j in text_chunks:
                        answers_student.append(j)
                else:
                    for j in text_chunks:
                        questions_student.append(j)
            for i in questions_student:
                q_a_dict_student[i] = answers_student[questions_student.index(i)]
        st.write(q_a_dict_student)


if __name__ == "__main__":
    home()
