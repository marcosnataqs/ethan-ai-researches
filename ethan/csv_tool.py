import json
from langchain.agents.tools import BaseTool
from typing import Type, List, Dict
from pydantic import BaseModel, Field

def generate_csv(json_string: str) -> str:
    print(f"\n\n[generate_csv] => Received parameter data: {json_string}")
    dict_list: List[Dict[str, str]] = json.loads(json_string)
    print(f"[generate_csv] => After converting into dictionary list: {dict_list}")
    return json_string

class EthanCsvInput(BaseModel):
    """Inputs for the generate_csv"""

    data: str = Field(description="Data to be used to generate the csv. The data should be in a json format.")

class EthanCsvTool(BaseTool):
    name = "generate_csv"
    description = """
        Useful when you want to generate a csv file.
        """
    args_schema: Type[BaseModel] = EthanCsvInput

    def __hash__(self) -> int:
        return hash((type(self)))

    def _run(self, data: str):
        anwser = generate_csv(data)
        return anwser

    def _arun(self, data: str):
        raise NotImplementedError("generate_csv does not support async")