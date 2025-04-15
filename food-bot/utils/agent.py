import os
from langchain.chains import ConversationalRetrievalChain
from langchain_community.chat_models import ChatGoogleGenerativeAI
from utils.memory import get_memory

def agent():
    retriever = get_memory().as_retriever()

    llm = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.5,
        convert_system_message_to_human=True
    )

    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever
    )

    return qa_chain
