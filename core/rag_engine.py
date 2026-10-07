from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from core.vector_store import build_vector_store, get_retriever, load_vector_store

def get_llm():
    return ChatMistralAI(model='mistral-small-latest', mistral_api_key = os.getenv('MISTRAL_API_KEY'), temperature=0.2)

def format_docs(docs):
    return "/n/n".join([doc.page_content for doc in docs])

def get_prompt():
    return ChatPromptTemplate.from_messages([
        (
            "system",
            """You are an expert meeting assistant.

Answer the user's question based ONLY on the meeting transcript context.

If the answer is not found in the context, say:
"I could not find this information in the meeting transcript."

Always be concise and precise. If quoting someone, mention it clearly.

Context from meeting transcript:
{context}""",
        ),
        ("human", "{question}"),
    ])

def create_rag_chain(retriever):
    return (
        {
            "context": retriever | RunnableLambda(format_docs),
            "question": RunnablePassthrough(),
        }
        | get_prompt()
        | get_llm()
        | StrOutputParser()
    )

def build_rag_pipeline(transcript: str):
    vector_store = build_vector_store(transcript)
    retriever = get_retriever(vector_store)
    rag_chain =  create_rag_chain(retriever)
    
    return rag_chain

def load_rag_pipeline():
    vector_store = load_vector_store()
    retriever = get_retriever(vector_store)    
    rag_chain =  create_rag_chain(retriever)
    
    return rag_chain

def ask_question(question: str, rag_chain):
    print(f"Question : {question}")
    answer = rag_chain.invoke({"question": question})
    print(f"Answer : {answer}")
    return answer
    

        
        