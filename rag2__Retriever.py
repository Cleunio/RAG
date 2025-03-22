# -*- coding: utf-8 -*-
"""Rag2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1VJg9HnmYCo09SSKsTBEuyFeAkUeVjmqD
"""

import bs4
from langchain_community.document_loaders import WebBaseLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

loader = WebBaseLoader(web_paths = ("https://www.bbc.com/portuguese/articles/cd19vexw0y1o",),)

docs = loader.load()

len(docs[0].page_content)

docs

print(docs[0].page_content[:100])

from langchain_text_splitters import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, add_start_index=True)
splits = text_splitter.split_documents(docs)

len(splits)

splits

hf_embeddings = HuggingFaceEmbeddings(model_name = "sentence-transformers/all-mpnet-base-v2")

vectorstore = Chroma.from_documents(documents=splits, hf_embeddings=hf_embeddings)

retriever = vectorstore.as_retriever(search_type = "similarity", search_kwargs={"k"=6})

prompt_rag = PromptTemplate(
    input_variables = ["context", "question"],
    template = template_rag,
)
prompt_rag

def format_docs(docs)
 return "\n\n".join(doc.page_content for doc in docs)

chain_rag = ({"context": retriever | format_docs}, "question": RunnablePassthrough() | prompt_rag | llm | StrOutputParser())

#without RAG
chain.invoke("Which movie won the Oscar?")

#without RAG
chain_rag.invoke("Which movie won the Oscar?")

vectorstore.delete_collection()