from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(model_name="mixtral-8x7b-32768", groq_api_key=os.getenv("GROQ_API_KEY"))

with open("prompts/summarize_prompt.txt") as f:
    summarize_template = f.read()

summarize_prompt = PromptTemplate.from_template(summarize_template)
summarize_chain = LLMChain(prompt=summarize_prompt, llm=llm)