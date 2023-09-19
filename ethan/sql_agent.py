import os
import streamlit as st
from langchain.llms import OpenAI
from langchain.sql_database import SQLDatabase
from langchain.agents import create_sql_agent, AgentExecutor
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents.agent_types import AgentType

class EthanSqlAgent:
    def __init__(self) -> None:
        self._openai_api_key = st.secrets["OPENAI_API_KEY"]
        # model_name="gpt-3.5-turbo-16k-0613"
        self._llm = OpenAI(temperature=0, openai_api_key=self._openai_api_key, verbose=True)
        self._agent = self._setup_agent()
    
    def _get_db(self) -> SQLDatabase:
        file_path = os.path.join(os.path.dirname(__file__), "data/chinook.db")
        db = SQLDatabase.from_uri(database_uri=f"sqlite:///{file_path}")
        return db
    
    def _setup_toolkit(self) -> SQLDatabaseToolkit:
        db = self._get_db()
        toolkit = SQLDatabaseToolkit(db=db, llm=self._llm)
        return toolkit
    
    def _setup_agent(self) -> AgentExecutor:
        toolkit = self._setup_toolkit()
        agent = create_sql_agent(llm=self._llm, toolkit=toolkit, agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
        return agent

    def run(self, prompt: str):
        response = self._agent.run(prompt)
        return response
