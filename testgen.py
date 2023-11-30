from openai import OpenAI
import math

LIS = []
prev = {'Motion': 0.67, 'Force': 0.60, 'Gravitation': 0.00, 'Sound': 0.98}


def sort_with_prev(L: list) -> list:
    a = [[prev.get(L[i]), L[i]] for i in range(len(L))]
    a.sort(reverse=True)
    L = [a[i][1] for i in range(len(a))]
    return L


ques_tot = 20
topics = ['Motion', 'Force', 'Gravitation', 'Sound']
topics = sort_with_prev(topics)
for i in topics:
    if i != topics[len(topics) - 1]:
        ques = ques_tot // len(topics)
        ques += math.floor(ques * prev.get(i))
        ques_tot -= ques
        LIS.append(ques)
    else:
        LIS.append(ques_tot)

if LIS[-1] > LIS[-2]:
    LIS[-1], LIS[-2] = LIS[-2], LIS[-1]

client = OpenAI(api_key="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")
for i in range(len(LIS)):
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": f"Generate {LIS[i]} subjective questions from {topics[i]} for class 9 CBSE exam", }],
        model="gpt-3.5-turbo", )
    print(chat_completion.choices[0].message.content)

# print(LIS)