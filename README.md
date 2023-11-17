# Academic Advisor Ai

## Objective
This repository is made for students, who want to self learn with the help of AI. This repository makes use of AI chat bots to generate and 
evaluate tests and course plans according to student's needs. This can also be used by teachers in creaing tests for classes.

## Login
**Needs to be updated**

Three options will be provided after completion of login
- Generate Tests
- Evaluate Tests
- Generate Course Plan

## Generate Tests
After login, this is one of the three options avalible to the user. 
When clicked will ask for the disered subject and on which topics of that subject. 
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
Weak topics will be given more importence hence more questions from there and less from the strong topics.


