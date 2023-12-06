import streamlit as st
from PyPDF2 import PdfReader
import re
import json
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
import time
from test_gen_func import sort_with_prev, gen_prompt, check, last_word, change_percent
import math
import random
from pprint import pprint
# import aspose


gen_questions_list = []
#LIS
prev = {'Motion': 0.00, 'Force': 0.00, 'Gravitation': 0.00, 'Sound': 0.00, 'Work': 0.00}
prev_topics = []
order = []

#---Main functions---


def test_eval(key):

    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader("Upload your PDFs here and click on 'Process'", accept_multiple_files=True, key=key)
    subject = st.radio(label="Choose your subject", options=["Physics", "Chemistry", "Biology", "Artificial "
                                                                                                "Intelligence (Code "
                                                                                                "417)", "Information "
                                                                                                        "Technology ("
                                                                                                        "Code 402)"])
    if st.button("Process"):
        # try:
        with st.spinner("Processing..."):
            raw_text = [i.replace("\n", " ") for i in get_pdf_text(pdf_docs)]
            st.write("raw text", raw_text)
            questions_student = []
            answers_student = []
            for i in raw_text:
                text_chunks = [j.strip() for j in re.split('\d+' + "." + " ", i)]
                text_chunks.pop(0)
                st.write("text_chunks", text_chunks)
                if raw_text.index(i) == 0:
                    for j in text_chunks:

                        j = last_word(j.strip())
                        # print(j)
                        questions_student.append(j[1])
                        order.append(last_word(j[0][1:-1]))
                else:
                    for j in text_chunks:
                        answers_student.append(j)

            questions_student = [i.strip() for i in questions_student]
            st.write("questions_student", questions_student)
            st.write("answers_student", answers_student)
            for i in questions_student:
                q_a_dict_student[i] = answers_student[questions_student.index(i)]
        try:
            percentage_dict = json.loads(json.dumps(llm_chain.run(f'''Give me a percentage based on the gradation of the answers on how accurate they are along with an elaborate reason for each percentage based on the grade of these answers to their respective questions one by one (according to the Indian CBSE class 9 {subject} syllabus) and format the data into a valid JSON object and make sure the same formatting is followed in every subsequent request in this conversation chain. Use double quotes instead of single quotes. Make the "percentage" and the "explanation" two different properties: {q_a_dict_student}'''))).split("\n\n")[1]
        except IndexError:
            percentage_dict = json.loads(json.dumps(llm_chain.run(f'''Give me a percentage based on the gradation of the answers on how accurate they are along with an elaborate reason for each percentage based on the grade of these answers to their respective questions one by one (according to the Indian CBSE class 9 {subject} syllabus) and format the data into a valid JSON object and make sure the same formatting is followed in every subsequent request in this conversation chain. Use double quotes instead of single quotes. Make the "percentage" and the "explanation" two different properties: {q_a_dict_student}''')))
        # percentage_dict = {"Explain what is meant by the term frequency in relation to sound.": { "percentage": 75, "reason": "The answer accurately explains the fundamental differences between scalar and vector quantities with a suitable example." }, "Describe the process of sound propagation in different media.": { "percentage": 0, "reason": "The answer is incomplete." }, "Explain how work is done by an object when it is moved through a distance.": { "percentage": 75, "reason": "The answer accurately defines and differentiates between gravitational force and electrostatic force." }, "Describe the importance of gravity for the formation and stability of the solar system.": { "percentage": 75, "reason": "The answer accurately describes the concept of work and its relation to energy." }, "Describe the different types of forces and how they can interact with each other.": { "percentage": 75, "reason": "The answer accurately explains the term 'refraction of light' and provides examples from daily life." }, "Explain the concept of a force and how it can cause objects to accelerate.": { "percentage": 75, "reason": "The answer accurately elaborates on the difference between series and parallel circuits." } }
        st.write(percentage_dict)
        print("percentage dict", repr(percentage_dict))
        percentage_list = []
        explanation_list = []
        try:
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
            change_percent(percent=percentage_list, subject=subjects_dict.get(subject), order=order, p=prev)
            st.session_state.messages.append(st.session_state.messages.append({"role": "assistant", "content": percentage_dict}))
            st.session_state.topic_prompt = ""
        except ValueError as e:
            print(e)
            percentage_dict = percentage_dict.strip("Formatted JSON Object: ")[1]
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
            change_percent(percent=percentage_list, subject=subjects_dict.get(subject), order=order, p=prev)
            st.session_state.messages.append(percentage_dict)
            st.session_state.topic_prompt = ""
    # except TypeError as e:
    #     print(e)
    #     response = "<span style='color:red'>Please input 2 pdf files as question and answer pdfs, separately (Question 1st, Answer 2nd)</span>"
    #     st.markdown(response, unsafe_allow_html=True)


def test_gen():
    global subject, prev, prev_topics, gen_questions_list
    subject = st.radio(label="Choose your subject", options=["Physics", "Chemistry", "Biology", "Artificial "
                                                                                                "Intelligence (Code "
                                                                                                "417)", "Information "
                                                                                                        "Technology ("
                                                                                                        "Code 402)"])
    ques_tot = st.radio(label="Number of questions", options=[10, 20, 30, 40])

    if st.button("Generate test"):
        with st.spinner("Processing..."):
            questions_student = []
            topics = subjects_dict.get(subject)
            topics = sort_with_prev(topics, p=prev)
            ques = ques_tot // len(topics)
            for i in topics:
                if i != topics[len(topics) - 1]:
                    ques += math.floor(ques * prev.get(i))
                    ques_tot -= ques
                    gen_questions_list.append(ques)
                else:
                    gen_questions_list.append(ques_tot)

        if gen_questions_list[-1] > gen_questions_list[-2]:
            gen_questions_list[-1], gen_questions_list[-2] = gen_questions_list[-2], gen_questions_list[-1]
        for i in range(len(topics)):
            for j in range(gen_questions_list[i]):
                prev_topics.append(topics[i])

        ques, a = [], ''
        questions_student.append(llm_chain.run(gen_prompt(topics=topics, gen_questions_list=gen_questions_list)))
        place = check(questions_student[0])
        for i in place:
            for j in range(1, 100000):
                try:
                    if questions_student[0][i + j] != '\n':
                        a = a + questions_student[0][i + j]
                    elif questions_student[0][i + j] == '\n':
                        ques.append([a.strip(), prev_topics[place.index(i)]])
                        a = ''
                        break
                except IndexError:
                    ques.append([a.strip(), prev_topics[place.index(i)]])
                    a = ''
                    break

        # st.write(ques)
        full_response = ""
        for k in range(len(ques)):
            d = random.choice(ques)
            full_response += f"{k+1}. {d[0]} ({d[1]})\n"
            # st.write(f"{k+1}. {d[0]} ({d[1]})")
            del ques[ques.index(d)]
        st.session_state.topic_prompt = ""
        st.session_state.messages.append({"role": "assistant", "content": full_response})

#---Main functions---


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


# ---CONSTANTS----
OPEN_AI_API_KEY = st.secrets["open_ai_api"]
# ---CONSTANTS----

# AI configuration
q_a_dict_student = {}

subjects_dict = {'Physics': ['Motion', 'Force', 'Gravitation', 'Sound', 'Work']}

template = """Question: {question}

Answer: Simply return the asked data and maintain specifications and skip any intermediary steps required. Make sure to give all requirements the same priority and make sure all of them are fulfilled. Make sure the formatting is valid JSON"""

prompt = PromptTemplate(template=template, input_variables=["question"])
llm = OpenAI(api_key=OPEN_AI_API_KEY, max_tokens=1500)

llm_chain = LLMChain(prompt=prompt, llm=llm)


def time_determine():
    """Determines greeting"""
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
        st.chat_input("Type 'how to' for help", disabled=True, key="disabled_chat_widget")
        with st.chat_message("assistant"):
            test_eval(key="0")
    elif st.session_state.topic_prompt == "generate test":
        st.chat_input("Type 'how to' for help", disabled=True, key="disabled_chat_widget")
        with st.chat_message("assistant"):
            test_gen()

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
        try:
            with st.chat_message(message['role']):
                st.markdown(message['content'])
        except TypeError:
            pass

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
    if st.session_state.topic_prompt == "":
        if prompt := st.chat_input("Type 'how to' for help", key="real_chat_widget"):
            # Display user message in chat message container
            st.chat_message("user").markdown(prompt)
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})

            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                if not st.session_state.use_app:
                    if prompt.lower() == "use app":
                        st.session_state.use_app = True
                        assistant_response = "Which option would you like to choose? (Evaluate Test, Generate Test)"
                        if prompt.lower() == "evaluate test" or prompt.lower() == "eval test":
                            st.session_state.topic_prompt = "evaluate test"
                            st.experimental_rerun()
                        elif prompt.lower() == "generate test" or prompt.lower() == "gen test":
                            st.session_state.topic_prompt = "generate test"
                            st.experimental_rerun()
                    elif prompt.lower() == "how to":
                        assistant_response = ""

                    else:
                        assistant_response = "Sorry I don't understand"
                else:
                    if st.session_state.topic_prompt == "":
                        assistant_response = "Which option would you like to choose? (Evaluate Test, Generate Test)"
                        if prompt.lower() == "evaluate test" or prompt.lower() == "eval test":
                            st.session_state.topic_prompt = "evaluate test"
                            st.experimental_rerun()
                        elif prompt.lower() == "generate test" or prompt.lower() == "gen test":
                            st.session_state.topic_prompt = "generate test"
                            st.experimental_rerun()

                    else:
                        st.experimental_rerun()

                # Simulate stream of response with milliseconds delay
                if assistant_response != "":
                    for chunk in assistant_response.split():
                        full_response += chunk + " "
                        time.sleep(0.05)
                        # Add a blinking cursor to simulate typing
                        message_placeholder.markdown(full_response + "▌")
                    message_placeholder.markdown(full_response)
                    # Add assistant response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                else:
                    response = """
                    How to use **Eduboost**
                    1. Type ```use app``` to view options (type ```use app``` after this to reset interaction)
                    2. *Choose option*: Type ```Evaluate Test``` (or ```eval test```) and upload files (Q and A pdfs separately for processing) ```Generate Test```  (or ```gen test```) and choose no of questions along with subject.
                    3. Follow the instructions
                    4. Type ```use app``` again to reset interaction.
                    ---
                    We hope you found our guide helpful!
                  """
                    message_placeholder.markdown(response)
                    # Add assistant response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    home()


