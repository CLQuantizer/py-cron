from langchain_community.document_loaders import TextLoader
from langchain_mistralai.chat_models import ChatMistralAI
from langchain_mistralai.embeddings import MistralAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import CharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from dotenv import load_dotenv
import os

api_key = os.getenv("MISTRAL_KEY")

# Load data
# loader = TextLoader("essay.txt")
loader = TextLoader("fiction.txt")
docs = loader.load()
# Split text into chunks 
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
documents = text_splitter.split_documents(docs)
# Define the embedding model
embeddings = MistralAIEmbeddings(model="mistral-embed", mistral_api_key=api_key)
# Create the vector store 
vector = FAISS.from_documents(documents, embeddings)
print("Vector store created number of documents:", vector.index.ntotal)
results = vector.similarity_search("The author worked on two main things before college.")
print("nunber of documents:", len(results))
print("documents 0:", results[0].page_content)
# Define a retriever interface
retriever = vector.as_retriever()
# Define LLM
model = ChatMistralAI(mistral_api_key=api_key)
# Define prompt template
prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context:

<context>
{context}
</context>

Question: {input}""")

# Create a retrieval chain to answer questions
document_chain = create_stuff_documents_chain(model, prompt)
retrieval_chain = create_retrieval_chain(retriever, document_chain)
response = retrieval_chain.invoke({"input": "What were the two main things the author worked on before college?"})
print(response["answer"])