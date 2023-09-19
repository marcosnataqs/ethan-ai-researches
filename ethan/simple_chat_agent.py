import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain import OpenAI, PromptTemplate, OpenAI, LLMChain

class EthanSimpleChatAgent:
    def __init__(self) -> None:
        self._openai_api_key = st.secrets["OPENAI_API_KEY"]
        self._llm = OpenAI(openai_api_key=self._openai_api_key, temperature=0)
        self._template = """
            You are a helpful and very polite assistant who helps people query their music database.
            You only answer questions regarding querying the music database.
            
            History:
            {chat_history}

            Question: {prompt}
        """
        self._prompt = PromptTemplate.from_template(self._template)
        self._memory = ConversationBufferMemory(memory_key="chat_history")
        self._llm_chain = LLMChain(
            llm=self._llm, prompt=self._prompt, memory=self._memory, verbose=True)

    
    def run(self, prompt: str):
        response = self._llm_chain.run(prompt=prompt)
        return response