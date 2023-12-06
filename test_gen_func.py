import streamlit as st
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

OPEN_AI_API_KEY = st.secrets["open_ai_key"]

template = """Question: {question}

Answer: Simply return the asked data and maintain specifications and skip any intermediary steps required. Make sure to give all requirements the same priority and make sure all of them are fulfilled. Make sure the formatting is valid JSON"""


prompt = PromptTemplate(template=template, input_variables=["question"])
llm = OpenAI(api_key=OPEN_AI_API_KEY, max_tokens=1500)
llm_chain = LLMChain(prompt=prompt, llm=llm)
# FUNCTIONS USED
def remove_space(thing: list) -> list:
    for i in range(len(thing[0])):
        if i != " ":
            return thing[i:]


def last_word(word: str) -> list[str]:
    sentence_list = [i+" " for i in word.split(" ")]
    last_word = sentence_list[len(sentence_list)-1].strip()
    sentence_list.pop(len(sentence_list)-1)
    rest_sentence = "".join(sentence_list)
    return [last_word, rest_sentence]


def check(questions: str):
    dummy = []
    for i in range(len(questions)):
        if questions[i] == " ":
            if questions[i - 3] == "\n" or questions[i - 4] == "\n":
                dummy.append(i)
    return dummy


def change_percent(percent: list, subject: list, order: list, p: dict) -> None:
    s = subject
    dummy = [[s[i], 0, 0] for i in range(len(s))]  # first zero is question numbers and second zero is number wrong
    # check
    try:
        for i in range(len(dummy)):
            if percent[i] <= 80:
                dummy[s.index(order[i][0])][2] = dummy[s.index(order[i][0])][2] + 1
    except TypeError:
        for i in range(len(dummy)):
            if int(percent[i].strip("%")) <= 80:
                dummy[s.index(order[i][0])][2] = dummy[s.index(order[i][0])][2] + 1

    # count
    for i in range(len(percent)):
        dummy[s.index(order[i][0])][1] = dummy[s.index(order[i][0])][1] + 1

    # change
    for i in range(len(dummy)):
        try:
            p[dummy[i][0]] = (p.get(dummy[i][0]) + (dummy[i][2] / dummy[i][1])) / 2
        except ZeroDivisionError:
            pass


def gen_prompt(topics: list, gen_questions_list: list) -> str:
    output = ""
    for i in range(len(topics)):
        if i != len(topics) - 1:
            output = output + f"Generate {gen_questions_list[i]} subjective questions from {topics[i]} for Indian class 9 CBSE exam and"
        else:
            output = output + f"Generate {gen_questions_list[i]} subjective questions from {topics[i]} for Indian class 9 CBSE exam"
    return output


def sort_with_prev(L: list, p: dict) -> list:
    a = [[p.get(L[i]), L[i]] for i in range(len(L))]
    a.sort(reverse=True)
    L = [a[i][1] for i in range(len(a))]
    return L


def recommendation(p: dict, topics: list, subject: str) -> str:
    with st.spinner("Generating..."):
        a = ''

        for i in range(len(topics)):
            if p.get(topics[i]) > 0.50:
                a += f"{topics[i]}, "
        if a != '':
            response = llm_chain.run(f"Recommend non copyright resources for students who are not proficient in Class 9 CBSE {subject} Syllabus in only the following topics: {a}")
        else:
            dummy = [[p.get(topics[i]), topics[i]] for i in range(len(topics))]
            dummy.sort(reverse=True)
            for i in range(3):
                a += dummy[i][1] + ', '

            response = llm_chain.run(
                f"Recommend non copyright resources for students who are not proficient in Class 9 CBSE {subject} Syllabus in only the following topics: {a}")

        return response
# Variables needed
LIS = []
SUBJECTS = {'Physics': ['Motion', 'Force', 'Gravitation', 'Sound', 'Work']}
prev = {'Motion': 0.00, 'Force': 0.00, 'Gravitation': 0.00, 'Sound': 0.00, 'Work': 0.00}
prev_topics = []
order = []
            
