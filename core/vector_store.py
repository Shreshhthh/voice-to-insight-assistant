from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

CHROMA_DIR = "vector_db"
COLLECTION_NAME = "meeting_transcript"
EMBEDDING_MODEL  = "all-MiniLM-L6-v2"

def get_embedding():
    return HuggingFaceEmbeddings(model_name = EMBEDDING_MODEL, model_kwargs={'device': 'cuda'})

def build_vector_store(transcript: str):
    
    splitter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap = 50)
    
    chunks = splitter.split_text(transcript)
    
    docs = [
        Document(page_content=chunk, metadata = {'chunk_index' : i})
        for i,chunk in enumerate(chunks)
    ]
    
    embedding = get_embedding()
    
    vector_store = Chroma.from_documents(
        documents = docs,
        embedding = embedding,
        persist_directory = CHROMA_DIR,
        collection_name = COLLECTION_NAME
    )
    
    return vector_store

def load_vector_store()->Chroma:
    embedding = get_embedding()
    vector_store = Chroma(persist_directory = CHROMA_DIR, embedding_function = embedding, collection_name = COLLECTION_NAME)
    return vector_store

def get_retriever(vector_store: Chroma, k: int =4)->str:
    
    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": k})
    return retriever
    
    
    
    