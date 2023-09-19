from langchain.agents.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field

from ethan.sql_agent import EthanSqlAgent

def run_data_question(data_question: str):
    ethanSqlAgent = EthanSqlAgent()
    response = ethanSqlAgent.run(data_question)
    return response


class EthanSqlAgentInput(BaseModel):
    """Inputs for the run method of EthanSqlAgent"""

    data_question: str = Field(description="Question to be asked to the database. For example, 'What is the album with the most tracks?'")

class EthanSqlAgentTool(BaseTool):
    name = "run_data_question"
    description = """
        Useful when you want to ask a question to the music database.
        You should enter the question knowing that later you will need to generate a SQL query based on the question.
        """
    args_schema: Type[BaseModel] = EthanSqlAgentInput

    def __hash__(self) -> int:
        return hash((type(self)))

    def _run(self, data_question: str):
        anwser = run_data_question(data_question)
        return anwser

    def _arun(self, data_question: str):
        raise NotImplementedError("run_data_question does not support async")