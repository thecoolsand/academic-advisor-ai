import streamlit as st
from PyPDF2 import PdfReader
import re
import json
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

# ---CONSTANTS----
# Replace "your_openai_api_key" with your actual OpenAI API key
OPEN_AI_API_KEY = "your_openai_api_key"
# ---CONSTANTS----

q_a_dict_student = {}

template = """Question: {question}

Answer: Simply return the asked data and maintain specifications and skip any intermediary steps required."""

prompt = PromptTemplate(template=template, input_variables=["question"])
llm = OpenAI(api_key=OPEN_AI_API_KEY, max_tokens=1500)

llm_chain = LLMChain(prompt=prompt, llm=llm)


def get_pdf_text(pdf_docs):
    # TODO: add a handwriting-recognizing API here for handwritten documents
    text_array = []
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in range(len(pdf_reader.pages)):
            page_obj = pdf_reader.pages[page]
            text_array.append(page_obj.extract_text())
    if text_array != []:
        return text_array
    else:
        return None


def analyze_student_performance(questions, answers, subject):
    # Implement the analysis logic here
    # Return weaknesses and strengths
    weaknesses = {}
    strengths = {}
    return weaknesses, strengths


def recommend_books(weaknesses):
    # Implement book recommendation logic here
    # Return recommended books
    recommended_books = {}
    return recommended_books


def main():
    st.set_page_config(page_title="Generate Course Plan", page_icon=":books:")
    st.title("Generate Course Plan :book:")

    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader("Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
    subject = st.radio(label="Choose your subject", options=["Physics", "Chemistry", "Biology"])

    if st.button("Process"):
        try:
            with st.spinner("Processing..."):
                raw_text = [i.replace("\n", " ") for i in get_pdf_text(pdf_docs)]
                questions_student = []
                answers_student = []
                for i in raw_text:
                    text_chunks = re.split('\d+' + "." + " ", i)
                    text_chunks.pop(0)
                    if raw_text.index(i) == 0:
                        answers_student.extend(text_chunks)
                    else:
                        questions_student.extend(text_chunks)

                for i in questions_student:
                    q_a_dict_student[i] = answers_student[questions_student.index(i)]

                weaknesses, strengths = analyze_student_performance(questions_student, answers_student, subject)
                recommended_books = recommend_books(weaknesses)

            st.write("Weaknesses:")
            for question, explanation in weaknesses.items():
                st.write(f"{question}: {explanation}")

            st.write("Strengths:")
            for question, explanation in strengths.items():
                st.write(f"{question}: {explanation}")

            st.write("Recommended Books:")
            for topic, books in recommended_books.items():
                st.write(f"For {topic}, consider reading: {', '.join(books)}")

        except TypeError:
            response = "<span style='color:red'>Please upload a valid PDF file and select a subject</span>"
            st.markdown(response, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
