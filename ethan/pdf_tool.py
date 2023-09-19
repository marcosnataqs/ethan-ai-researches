import json
from langchain.agents.tools import BaseTool
from typing import Type, List, Dict
from pydantic import BaseModel, Field

def generate_pdf(json_string: str) -> str:
    print(f"\n\n[generate_pdf] => Received parameter data: {json_string}")
    dict_list: List[Dict[str, str]] = json.loads(json_string)
    print(f"[generate_pdf] => After converting into dictionary list: {dict_list}")
    return json_string

class EthanPdfInput(BaseModel):
    """Inputs for the generate_pdf"""

    data: str = Field(description="Data to be used to generate the pdf. The data should be in a json format.")

class EthanPdfTool(BaseTool):
    name = "generate_pdf"
    description = """
        Useful when you want to generate a pdf file.
        """
    args_schema: Type[BaseModel] = EthanPdfInput

    def __hash__(self) -> int:
        return hash((type(self)))

    def _run(self, data: str):
        anwser = generate_pdf(data)
        return anwser

    def _arun(self, data: str):
        raise NotImplementedError("generate_pdf does not support async")