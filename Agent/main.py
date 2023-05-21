from typing import Union
from fastapi import FastAPI
from typing import List, Union

from pydantic import BaseModel
import requests

import os
from langchain.llms import OpenAI
from langchain.prompts import load_prompt
from langchain.chains import LLMChain

app = FastAPI()


class QueryText(BaseModel):
    text: str

@app.get("/")
def read_root():
    key = os.environ["OPENAI_API_KEY"]
    print(f"Len Open AI key: {len(key)}")
    return {"Hello": "World"}


@app.post("/query")
def get_text(query_request: QueryText):
    query = query_request.text
    print(f"Query: {query}")
    dbvec_host = os.environ["DBVECTOR_SERVICE_NAME"]
    dbvec_port = os.environ["DBVECTOR_SERVICE_PORT"]
    db_vector_url = f"http://{dbvec_host}:{dbvec_port}/get_text"
    print(f"Send to VectorDB: {db_vector_url} ")

    r = requests.post(db_vector_url, json={"text": query})
    print("Result:")
    print(r)
    context = str(r.content.decode())
    print(context)

    llm = OpenAI(temperature=0.0)
    prompt = load_prompt("lc://prompts/vector_db_qa/prompt.json")
    chain = LLMChain(llm=llm, prompt=prompt)
    response = chain.run(question=query, context=context)

    return response