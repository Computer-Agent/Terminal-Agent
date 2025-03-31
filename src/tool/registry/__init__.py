from src.tool.registry.views import Function,ToolResult
from src.tool import Tool

class Registry:
    def __init__(self,tools:list[Tool]):
        self.tools=tools
        self.registry=self.tool_registry()
    
    def tools_prompt(self):
        actions_prompt=[tool.get_prompt() for tool in self.tools]
        return '\n\n'.join(actions_prompt)
    
    def tool_registry(self)->dict[str,Function]:
        return {tool.name : Function(name=tool.name,description=tool.description,params=tool.params,function=tool.func) for tool in self.tools}
    
    async def async_execute(self,name:str,input:dict,**kwargs)->ToolResult:
        tool=self.registry.get(name)
        try:
            if tool is None:
                raise ValueError('Tool not found')
            tool_params=tool.params.model_validate(input)
            params=tool_params.model_dump()|kwargs
            content=await tool.function(**params)
            return ToolResult(name=name,content=content)
        except Exception as e:
            return ToolResult(name=name,content=str(e))

    def execute(self,name:str,input:dict,**kwargs)->ToolResult:
        tool=self.registry.get(name)
        try:
            if tool is None:
                raise ValueError('Tool not found')
            tool_params=tool.params.model_validate(input)
            params=tool_params.model_dump()|kwargs
            content=tool.function(**params)
            return ToolResult(name=name,content=content)
        except Exception as e:
            return ToolResult(name=name,content=str(e))
    
