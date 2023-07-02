from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import paraphrasingModule
import os

# # Disable proxy temporarily
# if "HTTP_PROXY" in os.environ:
#     del os.environ["HTTP_PROXY"]
# if "HTTPS_PROXY" in os.environ:
#     del os.environ["HTTPS_PROXY"]
# Load the paraphrasing, keyword extraction and synonym finding modules
paraphraser = paraphrasingModule.PegasusParaphraser()
kw_syn = paraphrasingModule.KeywordSynonyms()

# User's input text is sent as a request body. The structure of this body can be defined by extending Pydantic's BaseModel
class Paragraph(BaseModel):
    paragraph: str
# The model above declares a JSON object (or Python dict) like:
# {
#     "paragraph": "user's input text"
# }

# Initialize the FastAPI application
app = FastAPI()

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

# API root
@app.get("/")
def get_root():
    return "API is running successfully"

# POST endpoint with path '/paraphrase'
@app.post("/paraphrase")
async def paraphrase_text(text: Paragraph):
    paraphrased_text = paraphraser.paraphrase_text(text.paragraph)

    return {
        "original": text.paragraph,
        "paraphrased": paraphrased_text,
        "keywords_synonyms": kw_syn.getSynonymsForKeywords(paraphrased_text)
    }