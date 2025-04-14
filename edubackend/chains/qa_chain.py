from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(model_name="mixtral-8x7b-32768", groq_api_key=os.getenv("GROQ_API_KEY"))

with open("prompts/qa_prompt.txt") as f:
    qa_template = f.read()

qa_prompt = PromptTemplate.from_template(qa_template)

def generate_qa(text: str, mode: str) -> list:
    num_questions = 5 if mode == "topic" else 12
    chain = LLMChain(prompt=qa_prompt, llm=llm)
    return chain.run(text=text, num_questions=num_questions)