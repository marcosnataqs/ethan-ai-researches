import streamlit as st
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.agents import ZeroShotAgent, AgentExecutor
from langchain.agents.tools import Tool

from ethan.simple_chat_agent_tool import EthanSimpleChatAgentTool
from ethan.sql_agent_tool import EthanSqlAgentTool
from ethan.pdf_tool import EthanPdfTool
from ethan.csv_tool import EthanCsvTool

class EthanAgent:
    def __init__(self) -> None:
        self._openai_api_key = st.secrets["OPENAI_API_KEY"]
        self._agent = self.init_agent()

    def _setup_tools(self) -> list[Tool]:
        tools = [EthanSimpleChatAgentTool(), EthanSqlAgentTool(), EthanPdfTool(), EthanCsvTool()]
        return tools

    def init_agent(self):
        prefix = """Answer the following questions as best you can, You have access to the following tools:"""
        suffix = """Begin! If users want to generate and/or export their data, use the following format as parameter for the respective requested tool:

        Remember when you are preparing the parameter for the tool, use only the data returned by the previous tool. Don't use your reasoning or any other data.

        Format:
        {format_example}

        Previous conversation history:
        {history}

        The Final Answer should be the exact tool output.

        Question: {input}
        {agent_scratchpad}"""

        tools = self._setup_tools()

        prompt = ZeroShotAgent.create_prompt(
            tools, prefix=prefix, suffix=suffix, input_variables=["input", "format_example", "history", "agent_scratchpad"]
        )

        llm = OpenAI(temperature=0, openai_api_key=self._openai_api_key)

        # model_name="gpt-3.5-turbo-16k-0613"
        llm_chain = LLMChain(llm=llm, prompt=prompt)

        tool_names = [tool.name for tool in tools]
        agent = ZeroShotAgent(llm_chain=llm_chain, allowed_tools=tool_names)

        agent_executor = AgentExecutor.from_agent_and_tools(
            agent=agent, tools=tools, verbose=True
        )

        return agent_executor
    
    def _get_history(self, messages: list[dict[str, str]]) -> str:
        history = ""
        for message in messages:
            role = 'Human' if message['role'] == 'user' else 'AI'
            history += f"{role}: {message['content']}\n"
        return history

    # Example prompts:
    # Could you give me the total number of albums and export it into pdf?
    # Could you export it as CSV but now add the number of tracks as well?
    # Could you list the first 10 artists and export it into CSV? Please add all table columns available.
    def run(self, prompt: str, messages: list[dict[str, str]]):
        history = self._get_history(messages)
        format_example = """[{"key1": value1, "key2": value2, ...}, {"key1": value1, "key2": value2, ...}, ...]"""
        response = self._agent.run(input=prompt, format_example=format_example, history=history)
        return response