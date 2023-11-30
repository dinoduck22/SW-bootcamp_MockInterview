# 6_qa_vectordb.py
import dotenv
import os

import streamlit as st

# from langchain.vectorstores import Pinecone
import pinecone

from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.embeddings.openai import OpenAIEmbeddings

dotenv.load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX="job"
PINECONE_ENVIRONMENT = "gcp-starter"

embeddings = OpenAIEmbeddings()

pinecone.init(api_key=PINECONE_API_KEY , environment=PINECONE_ENVIRONMENT)
docsearch = Pinecone.from_existing_index(PINECONE_INDEX,embeddings)

# query = "What did the president say about Ketanji Brown Jackson"
# docs = docsearch.similarity_search(query)

# print(docs)

# Create OPENAI LLM instance
llm = OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)
chain = load_qa_chain(llm, chain_type="stuff")

# Create a Streamlit app.
st.title("Interview Practice App")

# Prompt user to type their question
query = st.text_input("Question: Type your question here. when you done, type quit:")

if query != "quit":
    docs = docsearch.similarity_search(query)
    answer = chain.run(input_documents=docs, question=query)
    st.write(answer)
else:
    st.write("You are done.  Thank you for using the app.")

