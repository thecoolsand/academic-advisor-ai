import streamlit as st
from PyPDF2 import PdfReader
import re
import requests
import json
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate


#GUIDE
#q_a_dict_student: Contains all questions and answers in a simple JSON format from PDF
#questions_student: Contains list of all questions
#answers_student: Contains list of all answers

# ---CONSTANTS----
OPEN_AI_API_KEY = st.secrets["open_ai_key"]
# ---CONSTANTS----

q_a_dict_student = {}

template = """Question: {question}

Answer: Simply return the asked data and maintain specifications and skip any intermediary steps required."""

prompt = PromptTemplate(template=template, input_variables=["question"])
llm = OpenAI(api_key=OPEN_AI_API_KEY, max_tokens=1500)

llm_chain = LLMChain(prompt=prompt, llm=llm)


def get_pdf_text(pdf_docs):
    # TODO: add a handwriting recognising API here for handwritten documents
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


def home():
    st.set_page_config(page_title="Eduboost", page_icon=":books:")
    st.header("Test Evaluation :book:")

    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader("Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
    subject = st.radio(label="Choose your subject", options=["Physics", "Chemistry", "Biology", "Artificial "
                                                                                                "Intelligence (Code "
                                                                                                "417)", "Information "
                                                                                                        "Technology ("
                                                                                                        "Code 402)"])
    if st.button("Process"):
        try:
            with st.spinner("Processing..."):
                raw_text = [i.replace("\n", " ") for i in get_pdf_text(pdf_docs)]
                questions_student = []
                answers_student = []
                for i in raw_text:
                    text_chunks = re.split('\d+' + "." + " ", i)
                    text_chunks.pop(0)
                    # print(text_chunks)
                    if raw_text.index(i) == 0:
                        for j in text_chunks:
                            answers_student.append(j)
                    else:
                        for j in text_chunks:
                            questions_student.append(j)
                for i in questions_student:
                    q_a_dict_student[i] = answers_student[questions_student.index(i)]
            percentage_dict = json.loads(llm_chain.run(f"Give me an accurate percentage along with an elaborate reason for each percentage based on the grade of these answers to their respective questions one by one (according to the CBSE class 9 {subject} syllabus) and make the data into a JSON object and make sure the same formatting is followed in every subsequent request in this conversation chain. Make the 'percentage' and the 'explanation' two different properties: {q_a_dict_student}"))
            print(percentage_dict)
            print(type(percentage_dict))
            # percentage_dict = {"What are the fundamental differences between scalar and vector quantities?": { "percentage": 75, "reason": "The answer accurately explains the fundamental differences between scalar and vector quantities with a suitable example." }, "Explain the three laws of motion formulated by Sir Isaac Newton.": { "percentage": 0, "reason": "The answer is incomplete." }, "Define and differentiate between gravitational force and electrostatic force.": { "percentage": 75, "reason": "The answer accurately defines and differentiates between gravitational force and electrostatic force." }, "Describe the concept of work and its relation to energy.": { "percentage": 75, "reason": "The answer accurately describes the concept of work and its relation to energy." }, "Explain the term 'refraction of light' and provide examples from daily life.": { "percentage": 75, "reason": "The answer accurately explains the term 'refraction of light' and provides examples from daily life." }, "Elaborate on the difference between series and parallel circuits.": { "percentage": 75, "reason": "The answer accurately elaborates on the difference between series and parallel circuits." }, "Define sound waves and their propagation through different mediums.": { "percentage": 75, "reason": "The answer accurately defines sound waves and their propagation through different mediums." }, "What is the role of a concave lens in optical devices?": { "percentage": 75, "reason": "The answer accurately explains the role of a concave lens in optical devices." }, "Discuss the effects of force on an object's motion with suitable examples.": { "percentage": 75, "reason": "The answer accurately discusses the effects of force on an object's motion with a suitable example." }, "Explain the laws of reflection of light using a mirror as an example.": { "percentage": 75, "reason": "The answer accurately explains the laws of reflection of light using a mirror as an example." } }
            st.write(percentage_dict)
            percentage_list = []
            explanation_list = []

            for i in questions_student:
                for j in percentage_dict:
                    if i.strip() == j:
                        try:
                            percentage_list.append(percentage_dict[j]["percentage"])
                            explanation_list.append(percentage_dict[j]["explanation"])
                        except KeyError:
                            percentage_list.append(percentage_dict[j]["Percentage"])
                            explanation_list.append(percentage_dict[j]["Explanation"])
            st.write(percentage_list, explanation_list)
            print(percentage_list, explanation_list)
        except TypeError:
            response = "<span style='color:red'>Please input 2 pdf files as question and answer pdfs, separately (Question 1st, Answer 2nd)</span>"
            st.markdown(response, unsafe_allow_html=True)


if __name__ == "__main__":
    home()
