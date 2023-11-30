# Academic Advisor AI

---
### _Download and set up_
1. Clone the repository or download the zip file
2. Install dependencies with:  
```pip install -r requirements.txt```
3. run ```streamlit run main.py```
4. server is hosted at ```localhost:8501```
---

## Objective
This repository is made for students, who want to self learn with the help of AI. This repository makes use of AI chat bots to generate and 
evaluate tests and course plans according to student's needs. This can also be used by teachers in creating tests for classes.

## Generate Tests
After login, this is one of the three options avalible to the user. 
When clicked will ask for the desired subject and on which topics of that subject. 
Also it will ask for the number of questions to be asked. 
Then it will generate a test in a word file.

## Evaluate Tests
The user must enter the question paper as well as the answer sheet in seperate pdfs. 
The API will return a word file with points that were missed by the user.

## Generate Course Plan
Based on multiple tests, the API has an understanding of the student's weaknesses and strong points. 
The API will return a file containing
- The weaknesses in each topic of each subject
- Recommended books that could help the student

## Special Features
After each test, the AI will adjust the number of questions to be alloted to each topic. 
Weak topics will be given more importance hence more questions from there and less from the strong topics.


