from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

# Update to a currently supported model
llm = ChatGroq(model_name="llama3-70b-8192", groq_api_key=os.getenv("GROQ_API_KEY"))

with open("prompts/concept_prompt.txt") as f:
    concept_template = f.read()

concept_prompt = PromptTemplate.from_template(concept_template)

def generate_concept_map(text: str, mode: str) -> str:
    chain = LLMChain(prompt=concept_prompt, llm=llm)
    # To address the deprecation warning, you could also update this to:
    # result = chain.invoke({"text": text})
    # return result["text"]
    return chain.run(text=text)