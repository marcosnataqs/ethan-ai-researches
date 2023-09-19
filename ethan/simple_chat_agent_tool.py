from langchain.agents.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field

from ethan.simple_chat_agent import EthanSimpleChatAgent

def ethan_simple_chat_agent(question: str):
    ethanSimpleChatAgent = EthanSimpleChatAgent()
    response = ethanSimpleChatAgent.run(question)
    return response


class EthanSimpleChatAgentInput(BaseModel):
    """Inputs for the ethan_simple_chat_agent tool"""

    question: str = Field(description="The question to ask Ethan")

class EthanSimpleChatAgentTool(BaseTool):
    name = "ethan_simple_chat_agent"
    description = """
        Useful when you want to ask any other question non-related to the database. For example, "Hey, what is your name?".
        """
    args_schema: Type[BaseModel] = EthanSimpleChatAgentInput

    def __hash__(self) -> int:
        return hash((type(self)))

    def _run(self, question: str):
        anwser = ethan_simple_chat_agent(question)
        return anwser

    def _arun(self, question: str):
        raise NotImplementedError("ethan_simple_chat_agent does not support async")