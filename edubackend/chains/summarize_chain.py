from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os
from dotenv import load_dotenv

load_dotenv()

# Update to a currently supported model
llm = ChatGroq(model_name="llama3-70b-8192", groq_api_key=os.getenv("GROQ_API_KEY"))

with open("prompts/summarize_prompt.txt") as f:
    summarize_template = f.read()

summarize_prompt = PromptTemplate.from_template(summarize_template)
summarize_chain = LLMChain(prompt=summarize_prompt, llm=llm)

def generate_summary(text: str, type: str) -> str:
    # Fix parameter naming inconsistency (mode vs type)
    return summarize_chain.run(text=text, type=type)