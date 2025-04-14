from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(model_name="mixtral-8x7b-32768", groq_api_key=os.getenv("GROQ_API_KEY"))

with open("prompts/concept_prompt.txt") as f:
    concept_template = f.read()

concept_prompt = PromptTemplate.from_template(concept_template)

def generate_concept_map(text: str, mode: str) -> str:
    chain = LLMChain(prompt=concept_prompt, llm=llm)
    return chain.run(text=text)