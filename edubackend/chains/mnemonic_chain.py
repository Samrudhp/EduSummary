
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(model_name="mixtral-8x7b-32768", groq_api_key=os.getenv("GROQ_API_KEY"))

with open("prompts/mnemonic_prompt.txt") as f:
    mnemonic_template = f.read()

mnemonic_prompt = PromptTemplate.from_template(mnemonic_template)

def generate_mnemonics(text: str, mode: str) -> str:
    num_mnemonics = 1 if mode == "topic" else 3
    chain = LLMChain(prompt=mnemonic_prompt, llm=llm)
    return chain.run(text=text, num_mnemonics=num_mnemonics)