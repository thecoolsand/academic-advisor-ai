import streamlit as st
from PyPDF2 import PdfReader
import re
import json
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
import time


def test_eval(key):
    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader("Upload your PDFs here and click on 'Process'", accept_multiple_files=True, key=key)
        print(pdf_docs)
    subject = st.radio(label="Choose your subject", options=["Physics", "Chemistry", "Biology", "Artificial "
                                                                                                "Intelligence (Code "
                                                                                                "417)", "Information "
                                                                                                        "Technology ("
                                                                                                        "Code 402)"])
    if st.button("Process"):
        print("processing")
        try:
            with st.spinner("Processing..."):
                raw_text = [i.replace("\n", " ") for i in get_pdf_text(pdf_docs)]
                questions_student = []
                answers_student = []
                for i in raw_text:
                    text_chunks = re.split('\d+' + "." + " ", i)
                    # string_name.replace('\d+' + "." + " ", " ")
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
            percentage_dict = json.loads(json.dumps(llm_chain.run(f'''Give me a very accurate percentage along with an elaborate reason for each percentage based on the grade of these answers to their respective questions one by one (according to the Indian CBSE class 9 {subject} syllabus) and make the data into a valid JSON object and make sure the same formatting is followed in every subsequent request in this conversation chain. Make the "percentage" and the "explanation" two different properties: {q_a_dict_student}''')))

            # percentage_dict = {"What are the fundamental differences between scalar and vector quantities?": { "percentage": 75, "reason": "The answer accurately explains the fundamental differences between scalar and vector quantities with a suitable example." }, "Explain the three laws of motion formulated by Sir Isaac Newton.": { "percentage": 0, "reason": "The answer is incomplete." }, "Define and differentiate between gravitational force and electrostatic force.": { "percentage": 75, "reason": "The answer accurately defines and differentiates between gravitational force and electrostatic force." }, "Describe the concept of work and its relation to energy.": { "percentage": 75, "reason": "The answer accurately describes the concept of work and its relation to energy." }, "Explain the term 'refraction of light' and provide examples from daily life.": { "percentage": 75, "reason": "The answer accurately explains the term 'refraction of light' and provides examples from daily life." }, "Elaborate on the difference between series and parallel circuits.": { "percentage": 75, "reason": "The answer accurately elaborates on the difference between series and parallel circuits." }, "Define sound waves and their propagation through different mediums.": { "percentage": 75, "reason": "The answer accurately defines sound waves and their propagation through different mediums." }, "What is the role of a concave lens in optical devices?": { "percentage": 75, "reason": "The answer accurately explains the role of a concave lens in optical devices." }, "Discuss the effects of force on an object's motion with suitable examples.": { "percentage": 75, "reason": "The answer accurately discusses the effects of force on an object's motion with a suitable example." }, "Explain the laws of reflection of light using a mirror as an example.": { "percentage": 75, "reason": "The answer accurately explains the laws of reflection of light using a mirror as an example." } }
            st.write(percentage_dict)
            percentage_list = []
            explanation_list = []

            for i in questions_student:
                for j in json.loads(percentage_dict):
                    if i.strip() == j:
                        try:
                            percentage_list.append(json.loads(percentage_dict)[j]["percentage"])
                            explanation_list.append(json.loads(percentage_dict)[j]["explanation"])
                        except KeyError:
                            percentage_list.append(json.loads(percentage_dict)[j]["Percentage"])
                            explanation_list.append(json.loads(percentage_dict)[j]["Explanation"])
            st.write(percentage_list, explanation_list)
            st.session_state.topic_prompt = ""

        except TypeError:
            response = "<span style='color:red'>Please input 2 pdf files as question and answer pdfs, separately (Question 1st, Answer 2nd)</span>"
            st.markdown(response, unsafe_allow_html=True)


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


def read_counter(file_name):
    with open(file_name, "r") as f:
        return int(f.readline())


def write_counter(file_name):
    with open(file_name, "w") as f:
        f.write("1")
    f.close()

# ---CONSTANTS----
OPEN_AI_API_KEY = st.secrets["open_ai_api"]
# ---CONSTANTS----

q_a_dict_student = {}

template = """Question: {question}

Answer: Simply return the asked data and maintain specifications and skip any intermediary steps required."""

prompt = PromptTemplate(template=template, input_variables=["question"])
llm = OpenAI(api_key=OPEN_AI_API_KEY, max_tokens=1500)

llm_chain = LLMChain(prompt=prompt, llm=llm)


def time_determine():
    t = int(time.strftime("%H", time.localtime()))
    if 0 <= t <= 2 or 17 <= t <= 23:
        return "Good Evening"
    elif 2 <= t <= 12:
        return "Good morning"
    elif 12 <= t <= 17:
        return "Good afternoon"


def home():
    global greet_counter
    st.set_page_config(page_title="Eduboost", page_icon=":books:")
    st.header("Test Evaluation :book:")

    print(st.session_state)


    # Initialise topic
    if "topic_prompt" not in st.session_state:
        st.session_state.topic_prompt = ""
    elif st.session_state.topic_prompt == "evaluate test":
        st.chat_input("What is up?", disabled=True, key="disabled_chat_widget")
        with st.chat_message("assistant"):
            test_eval(key="0")

        #     message_placeholder = st.empty()
        #     full_response = ""
        # for chunk in assistant_response.split():
        #         full_response += chunk + " "
        #         time.sleep(0.05)
        #         # Add a blinking cursor to simulate typing
        #         message_placeholder.markdown(full_response + "▌")
        #     message_placeholder.markdown(full_response)
        #     # Add assistant response to chat history
        #     st.session_state.messages.append({"role": "assistant", "content": full_response})
    if "use_app" not in st.session_state:
        st.session_state.use_app = False
    # Initialise greeting count
    if "greeting_count" not in st.session_state:
        st.session_state.greeting_count = 0
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if st.session_state.greeting_count == 0:
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            assistant_response = f"Hey there! {time_determine()}! What would you like to do today?"
            full_response = ""
            for chunk in assistant_response.split():
                    full_response += chunk + " "
                    time.sleep(0.05)
                    # Add a blinking cursor to simulate typing
                    message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            st.session_state.greeting_count += 1
    else:
        pass



    # React to user input
    if prompt := st.chat_input("What is up?", key="real_chat_widget"):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            if not st.session_state.use_app:
                print("if0")
                if prompt.lower() == "use app":
                    st.session_state.use_app = True
                    assistant_response = "Which option would you like to choose? (Evaluate Test, Generate Test, Generate Course Plan)"
                    if prompt.lower() == "evaluate test":
                        st.session_state.topic_prompt = "evaluate test"
                        if st.session_state.topic_prompt == "evaluate test":
                            st.experimental_rerun()
                else:
                    assistant_response = "Sorry I don't understand"
            else:
                print("else0")
                if st.session_state.topic_prompt == "":
                    print("if1")
                    assistant_response = "Which option would you like to choose? (Evaluate Test, Generate Test, Generate Course Plan)"
                    if prompt.lower() == "evaluate test":
                        st.session_state.topic_prompt = prompt.lower()
                        if st.session_state.topic_prompt == "evaluate test":
                            st.experimental_rerun()

                elif st.session_state.topic_prompt == "evaluate test":
                    print("elif1")
                    st.experimental_rerun()

            # Simulate stream of response with milliseconds delay
            for chunk in assistant_response.split():
                full_response += chunk + " "
                time.sleep(0.05)
                # Add a blinking cursor to simulate typing
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": full_response})


if __name__ == "__main__":
    home()
