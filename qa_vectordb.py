# 6_qa_vectordb.py by mentor Jeong
import dotenv
import os
# streamlit
import streamlit as st
# Pincone
import pinecone
# langchain
from langchain.vectorstores import Pinecone
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import TextLoader
import chardet
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Pinecone


dotenv.load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX="job"
PINECONE_ENVIRONMENT = "gcp-starter"
DOC_PATH = "./overflow.txt"

# open ai 임베딩
embeddings = OpenAIEmbeddings()

# text loading
loader = TextLoader(DOC_PATH, autodetect_encoding=True)
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
doc = text_splitter.split_documents(documents)

# pinecone 설정
pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)
# First, check if our index already exists. If it doesn't, we create it
if PINECONE_INDEX not in pinecone.list_indexes():
    # we create a new index
    pinecone.create_index(name=PINECONE_INDEX, metric="cosine", dimension=1536)
# The OpenAI embedding model `text-embedding-ada-002 uses 1536 dimensions`
docsearch = Pinecone.from_documents(doc, embeddings, index_name=PINECONE_INDEX)

# Create OPENAI LLM instance
llm = OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)
chain = load_qa_chain(llm, chain_type="stuff")

# query = how is overflow founded

def main():
    # Create a Streamlit app.
    st.title("Interview Practice App")

    # Prompt user to type their question
    query = st.text_input("Question: Type your question here. when you done, type quit:")

    st.markdown(reply(query))


def reply(query):
    if query:
        docs = docsearch.similarity_search(query)
        answer = chain.run(input_documents=docs, question=query)
        return answer


if __name__ == '__main__':
    main()