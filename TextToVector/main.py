from typing import Union
from fastapi import FastAPI

from langchain.text_splitter import NLTKTextSplitter
import nltk
from pydantic import BaseModel

import requests
import os

app = FastAPI()
nltk.download('punkt')

class Text(BaseModel):
    text: str


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/add_text")
def read_item(text_request: Text):
    text = text_request.text
    print(f"Receiving text of [{len(text)}] size")
    text_splitter = NLTKTextSplitter(chunk_size=1000)
    splitted_text = text_splitter.split_text(text)
    print("")
    print("Chunks: ", len(splitted_text))
    print(f"First chunk: [{splitted_text[0]}]")
    print("")
    dbvec_host = os.environ["DBVECTOR_SERVICE_NAME"]
    dbvec_port = os.environ["DBVECTOR_SERVICE_PORT"]
    db_vector_url = f"http://{dbvec_host}:{dbvec_port}/store_text"
    print(f"Send to VectorDB: {db_vector_url} ")

    r = requests.put(db_vector_url, json={"text": splitted_text})
    print("Result:")
    print(r)
    print(r.content)

    return "OK"

