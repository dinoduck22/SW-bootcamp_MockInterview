import getpass
import os

from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Pinecone

os.environ["PINCECONE_API_KEY"] = getpass.getpass("Pincecone aPI Key:")
os.environ["PINECONE_ENV"] = getpass.getpass("Pinecone Environment:")
os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API Key:")