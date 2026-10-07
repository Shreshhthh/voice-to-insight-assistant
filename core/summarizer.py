from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.runnables import RunnableLambda, RunnablePassthrough

import os

def get_llm():
    return ChatMistralAI(model='mistral-small-latest', mistral_api_key = os.getenv('MISTRAL_API_KEY'), temperature=0.4)

def split_transcript(transcript: str) -> list:
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 3000,
        chunk_overlap = 200
        
    )
    
    return splitter.split_text(transcript)

def summarize_transcript(transcript: str)-> list:
    llm=get_llm()
    
    chunk_prompt = ChatPromptTemplate(
        [
            ("system", "Summarize this portion of a meeting transcript concisely."),
            ("human", "{text}")
        ]
    )
    summarize_chain = chunk_prompt | llm | StrOutputParser()
    
    chunks = split_transcript(transcript)
    
    chunk_summaries = [summarize_chain.invoke({'text':chunk}) for chunk in chunks]
    
    summary = "/n/n".join(chunk_summaries)
    
    summarize_prompt = ChatPromptTemplate.from_messages(
        [
            ('system','You are an expert meeting summarizer, combine these partial summaries into one final professional meeting summary in bullet points'),
            ('human', '{text}')
        ]
    )
    
    final_chain = (
        RunnablePassthrough() | RunnableLambda(lambda x:{'text'}) | summarize_prompt | llm | StrOutputParser()
    )
    
    return final_chain.invoke(summary)


def generate_title(transcript: str)->str:
    llm=get_llm()
    
    title_chain=(
        RunnablePassthrough()| RunnableLambda(lambda x:{'text'}) |
        ChatPromptTemplate([
            ('system', 'Based on the meeting transcript, generate a short professional meeting title, use max 8 words and only return the title, nothing else'),
            ('human', '{text}')
        ]) | llm | StrOutputParser()
    ) 
    return title_chain.invoke(transcript[:100])