from typing import Union
from fastapi import FastAPI
from typing import List, Union

from pydantic import BaseModel
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings

import os

app = FastAPI()

persist_directory = 'db'


class TextChunks(BaseModel):
    text: List[str] = []

class QueryText(BaseModel):
    text: str

@app.get("/")
def read_root():
    key = os.environ["OPENAI_API_KEY"]
    print(f"Len Open AI key: {len(key)}")
    return {"Hello": "World"}


@app.put("/store_text")
def store_text(text_request: TextChunks):
    chunks = text_request.text
    print(f"Receiving chunks [{len(chunks)}] size")
    if len(chunks) == 0:
        return "EMPTY CHUNKS"

    embeddings = OpenAIEmbeddings()
    vectordb = Chroma.from_texts(chunks, embeddings,persist_directory=persist_directory)
    vectordb.persist()

    return "OK"

@app.get("/get_text")
def get_text():
    embeddings = OpenAIEmbeddings()
    vectordb = Chroma.from_texts([""], embeddings,persist_directory=persist_directory)
    result = vectordb.get()

    return result

@app.post("/get_text")
def get_text(query_request: QueryText):
    query = query_request.text
    print(f"Query: {query}")

    embeddings = OpenAIEmbeddings()
    vectordb = Chroma.from_texts([""], embeddings,persist_directory=persist_directory)
    docs = vectordb.similarity_search(query)
    print(f"Num of docs found: {len(docs)}")
    context = ""
    for doc in docs:
        context += doc.page_content
    print(f"Result: {context}")

    return context