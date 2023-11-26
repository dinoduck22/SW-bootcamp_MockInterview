# 6_save_vectordb.py

import pinecone
import dotenv
import openai
import os

import pandas as pd
import numpy as np
import streamlit as st

from langchain.vectorstores import Chroma, Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
import pinecone

from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain

dotenv.load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX="job"
PINECONE_ENVIRONMENT = "gcp-starter"
DOC_PATH = "../data/openai_engineer.csv"

embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

pinecone.init(api_key=PINECONE_API_KEY , environment=PINECONE_ENVIRONMENT)

# load the documents to use for questions and aswnersingst
df = pd.read_csv(DOC_PATH)

# create lists for the vectors and the ids
texts = df['text'].tolist()


# Create or upsert the data to the Pinecone index
index = Pinecone.from_texts(texts, embeddings, index_name=PINECONE_INDEX)


