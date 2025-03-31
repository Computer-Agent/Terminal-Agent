from src.message import AIMessage,SystemMessage
from abc import ABC,abstractmethod
from pydantic import BaseModel
from src.tool import Tool

class Token(BaseModel):
    input: int
    output: int
    total: int

structured_output_prompt='''
### JSON Response Format:
Integrate the JSON output as part of the structured response, ensuring it strictly follows the provided schema.
```json
{json_schema}
```
If there is code block inside the JSON adheres to the following formatting guidelines:
1. Escape Newlines: `\n` should be `\n`.
2. Escape Quotes: `'` should be `\'` and `"` should be `\"`.
3. Escape Backslashes: `\` should be `\\`.
Validate all fields, use `null` or empty values for missing data, and format the JSON in a clear, indented code block.
'''

class BaseInference(ABC):
    def __init__(self,model:str,api_key:str='',base_url:str='',tools:list[Tool]=[],temperature:float=0.5):
        self.model=model
        self.api_key=api_key
        self.base_url=base_url
        self.tools=tools
        self.temperature=temperature
        self.headers={'Content-Type': 'application/json'}
        self.structured_output_prompt=structured_output_prompt
        self.tokens:Token=Token(input=0,output=0,total=0)

    @abstractmethod
    def invoke(self,messages:list[dict],json:bool=False,model:BaseModel=None)->AIMessage|BaseModel:
        pass

    @abstractmethod
    async def async_invoke(self,messages:list[dict],json:bool=False,model:BaseModel=None)->AIMessage|BaseModel:
        pass

    @abstractmethod
    def stream(self,messages:list[dict],json:bool=False)->AIMessage:
        pass

    def structured(self,message:SystemMessage,model:BaseModel):
        return f'{message.content}\n{structured_output_prompt.format(json_schema=model.model_json_schema())}'