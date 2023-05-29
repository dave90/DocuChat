from langchain.document_loaders import PyPDFLoader
import requests

TEXT_TO_VEC_HOST=""
TEXT_TO_VEC_PORT="80"


pdf="./Answer_Set_Programming_A_Primer.pdf"
pdf_text = ""

loader = PyPDFLoader(pdf)
documents = loader.load()

for doc in documents:
  text = doc.page_content
  pdf_text += text

print(f"Len {len(pdf_text)}")
#print("Text:")
#print(pdf_text)

text_to_vec_url = f"http://{TEXT_TO_VEC_HOST}:{TEXT_TO_VEC_PORT}/text-to-vec/add_text"
print(f"Send to Agent: {text_to_vec_url} ")
response = requests.post(text_to_vec_url, json={"text": pdf_text})
print(response)
