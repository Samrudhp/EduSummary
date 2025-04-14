from fastapi import FastAPI
from pydantic import BaseModel
from chains.summarize_chain import generate_summary
from chains.qa_chain import generate_qa
from chains.concept_chain import generate_concept_map
from chains.mnemonic_chain import generate_mnemonics
from utils.text_cleaner import clean_text

app = FastAPI()

class InputText(BaseModel):
    text: str
    type: str  # 'topic' or 'chapter'

@app.post("/generate-notes")
async def generate_notes(input_text: InputText):
    text = clean_text(input_text.text)

    summary = generate_summary(text, input_text.type)
    qa = generate_qa(text, input_text.type)
    concept_map = generate_concept_map(text, input_text.type)
    mnemonics = generate_mnemonics(text, input_text.type)

    return {
        "summary": summary,
        "qa": qa,
        "concept_map": concept_map,
        "mnemonics": mnemonics
    }