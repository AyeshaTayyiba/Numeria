from dotenv import load_dotenv
import os 
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import TextLoader


# model setup

load_dotenv()
api_key : str  = os.getenv("key")
# print(api_key)
model: str ="deepseek-r1-distill-llama-70b"
deepseek = ChatGroq(api_key=api_key, model_name = model)

# print(deepseek.invoke('Hello There!'))

# Getting only result from the model

parser = StrOutputParser()
deepseek_chain = deepseek|parser
# result: str = deepseek_chain.invoke('what is a bot')
# print(result)


# Loading and Spliting data in chunks
loader = TextLoader('data.txt',encoding = 'utf-8')
data = loader.load()
# print(data)


# Define the function of the chatbot
# template = ("""
# You are a math teacher. You are teaching students in grade {grade} in {location}.   
# Based on the Curriculum provided, can you come up with one question in each category in the curriculum.
# While you read through the curriculum and think about the categories, don't output any of your thoughts.
# The output should only be the math questions. List each of the questions as a numbered list.
# Curriculum: {curriculum}
# """)


template = ("""
"You are a math teacher. You are teaching students in grade {grade} in {location}, specifically following the curriculum provided.
Please read through the curriculum and generate one math question for each category outlined in the curriculum. 
The questions should be clear, simple, and appropriate for the students, and they should directly correspond to the categories in the curriculum.
Do not include any category titles before the questions.
The answers to the math questions must be numerical. If the answer is not numerical, generate a different question until you have a numerical answer, or exculde the category.
Provide the questions in a numbered list, with no other content in your response.
Provide the corresponding answers in a numbered list, with no other content in your response.
Begin by generating only the questions and answers, one per curriculum category."
Curriculum: {curriculum}
""")

stuGrade = 1
stuLocation = "Ontario, Canada"
# stuCurriculum = "pasted"
template = template.format(grade = stuGrade, location = stuLocation, curriculum = data)
# print(template)
answer = deepseek_chain.invoke(template)

# clean the answer - just get the questions
clean_answer = str(answer).split("</think>\n\n")[1]

print(clean_answer)

#list of q = list[print(clean_answer)]
# list of ans = []

# for loop where each question is asked
    # ask user to input an answer
    # chat bot has to check if the answer is correct
        # if ans is CORRECT: move on to the next question
        # if ans if WRONG: 
            # brief explaination
            # ask again with different number
            # if the ans is CORRECT: move on

# once for loop is done, they win the level



