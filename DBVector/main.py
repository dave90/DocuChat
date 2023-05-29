from typing import Union
from fastapi import FastAPI
from typing import List, Union

from pydantic import BaseModel
import openai
import numpy as np

import os

import redis
from redis.commands.search.field import TagField, VectorField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.query import Query

redis_host = os.environ["REDIS_HOST"]
redis_port = os.environ["REDIS_PORT"]

r = redis.Redis(host=redis_host, port=redis_port)
INDEX_NAME = "index"                              # Vector Index Name
DOC_PREFIX = "doc:"                               # RediSearch Key Prefix for the Index
VECTOR_DIMENSIONS = 1536

app = FastAPI()


def create_index(vector_dimensions: int):
    try:
        # check to see if index exists
        r.ft(INDEX_NAME).info()
        print("Index already exists!")
    except:
        # schema
        schema = (
            TagField("tag"),                       # Tag Field Name
            VectorField("vector",                  # Vector Field Name
                "FLAT", {                          # Vector Index Type: FLAT or HNSW
                    "TYPE": "FLOAT32",             # FLOAT32 or FLOAT64
                    "DIM": vector_dimensions,      # Number of Vector Dimensions
                    "DISTANCE_METRIC": "COSINE",   # Vector Search Distance Metric
                }
            ),
        )

        # index Definition
        definition = IndexDefinition(prefix=[DOC_PREFIX], index_type=IndexType.HASH)

        # create Index
        r.ft(INDEX_NAME).create_index(fields=schema, definition=definition)


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
    '''
    Given a chunk of text store into the DB Vector
    '''
    chunks = text_request.text
    print(f"Receiving chunks [{len(chunks)}] size")
    if len(chunks) == 0:
        return "EMPTY CHUNKS"

    create_index(vector_dimensions=VECTOR_DIMENSIONS)

    response = openai.Embedding.create(input=chunks, engine="text-embedding-ada-002")
    embeddings = np.array([r["embedding"] for r in response["data"]], dtype=np.float32)

    # Write to Redis
    pipe = r.pipeline()
    for i, embedding in enumerate(embeddings):
        pipe.hset(f"doc:{i}", mapping={
            "vector": embedding.tobytes(),
            "content": chunks[i],
            "tag": "openai"
        })
    res = pipe.execute()
    print(res)

    r.save()

    return "OK"

@app.get("/get_text")
def get_text():
    '''
    Get random chunks. Used for debug.
    '''

    create_index(vector_dimensions=VECTOR_DIMENSIONS)

    text = "Hello"
    # create query embedding
    response = openai.Embedding.create(input=[text], engine="text-embedding-ada-002")
    query_embedding = np.array([r["embedding"] for r in response["data"]], dtype=np.float32)[0]
    print(f"Embedding size {len(query_embedding)}")

    # query for similar documents that have the openai tag
    query = (
        Query("(@tag:{ openai })=>[KNN 2 @vector $vec as score]")
        .sort_by("score")
        .return_fields("content", "tag", "score")
        .paging(0, 2)
        .dialect(2)
    )

    query_params = {"vec": query_embedding.tobytes()}
    docs = r.ft(INDEX_NAME).search(query, query_params).docs

    result = str(docs)

    return result

@app.post("/get_text")
def get_text(query_request: QueryText):
    '''
    Given a text (query) return similar texts inside DB Vector (context)
    '''
    query = query_request.text
    print(f"Query: {query}")

    # create query embedding
    response = openai.Embedding.create(input=[query], engine="text-embedding-ada-002")
    query_embedding = np.array([r["embedding"] for r in response["data"]], dtype=np.float32)[0]
    print(f"Embedding size {len(query_embedding)}")

    # query 5 similar documents that have the openai tag
    query = (
        Query("(@tag:{ openai })=>[KNN 5 @vector $vec as score]")
        .sort_by("score")
        .return_fields("content", "tag", "score")
        .paging(0, 5)
        .dialect(2)
    )

    query_params = {"vec": query_embedding.tobytes()}
    docs = r.ft(INDEX_NAME).search(query, query_params).docs


    print(f"Num of docs found: {len(docs)}")
    context = ""
    for doc in docs:
        context += doc.content+"\n\n"
    print(f"Result: {context}")

    return {"context":context}