import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
import re


def get_pdf_text(pdf_docs):
    # TODO: add a handwriting recognising API here for handwritten documents
    text_array = []
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in range(len(pdf_reader.pages)):
            page_obj = pdf_reader.pages[page]
            text_array.append(page_obj.extract_text())
    return text_array

# def get_text_chunks(text, ques_no):
#     text_array = [text]
#     text_array2 = []
#     for i in range(ques_no):
#         y = text_array[i].split(str(i+1), ques_no)


def home():
    st.set_page_config(page_title="Eduboost", page_icon=":books:")
    st.header("Pdf reader :book:")

    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader("Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
    if st.button("Process"):
        with st.spinner("Processing..."):
            raw_text = get_pdf_text(pdf_docs)
            print(raw_text)
            for i in raw_text:
                print(i)
                text_chunks = re.split('\d+'+"."+"\n", i)
                text_chunks.pop(0)
                text_chunks = [i.replace("\n", " ") for i in text_chunks]
                print(text_chunks)
                for j in text_chunks:
                    st.write(j)
                st.markdown("""---""")


if __name__ == "__main__":
    home()
