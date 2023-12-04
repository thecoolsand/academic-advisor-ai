import streamlit as st
from PyPDF2 import PdfReader
import re
import json
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
import time
import random

# FUNCTIONS USED
def last_word(word: str) -> list[str]:
    for i in range(len(word)):
        if word[-i] == " " and word[-i + 1] != " ":
            return [word[0:len(word) - i], word.strip(" ")[-1]]


def check(questions: str):
    dummy = []
    for i in range(len(questions)):
        if questions[i] == " ":
            if questions[i - 3] == "\n" or questions[i - 4] == "\n":
                dummy.append(i)
    return dummy


def change_percent(percent: list, subject: str, order: list, p: dict) -> None:
    s = SUBJECTS.get(subject)
    dummy = [[s[i], 0, 0] for i in range(len(s))]  # first zero is question numbers and second zero is number wrong
    # count
    for i in range(len(percent)):
        dummy[s.index(order[i])][1] = dummy[s.index(order[i])][1] + 1

    # check
    for i in range(len(dummy)):
        if percent[i] <= 80:
            dummy[dummy.index([order[i], 0, 0])][2] = dummy[dummy.index([order[i], 0, 0])][2] + 1

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

# Variables needed
LIS = []
SUBJECTS = {'Physics': ['Motion', 'Force', 'Gravitation', 'Sound', 'Work']}
prev = {'Motion': 0.00, 'Force': 0.00, 'Gravitation': 0.00, 'Sound': 0.00, 'Work': 0.00}
prev_topics = []
order = []

#main func

def test_gen(key):
    ques_tot = st.radio(label="Number of questions", options=[10, 20, 30, 40])
    if st.button("Generate test"):
        with st.spinner("Processing..."):
            questions_student = []
            topics = SUBJECTS.get(subject)
            topics = sort_with_prev(topics, p=prev)
            ques = ques_tot // len(topics)
            for i in topics:
                if i != topics[len(topics) - 1]:
                    ques += math.floor(ques * prev.get(i))  # NOQA
                    ques_tot -= ques
                    LIS.append(ques)
                else:
                    LIS.append(ques_tot)

        if LIS[-1] > LIS[-2]:
            LIS[-1], LIS[-2] = LIS[-2], LIS[-1]
        for i in range(len(topics)):
            for j in range(LIS[i]):
                prev_topics.append(topics[i])

        ques, a = [], ''
        questions_student.append(llm_chain.run(gen_prompt(topics=topics)))
        st.write(questions_student)
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
                
        for k in range(len(ques)):
            d = random.choice(ques)
            st.write(f"{k + 1}. {d[0]} ({d[1]})")
            del ques[ques.index(d)]
            
