from pydantic import BaseModel, Field
from typing import Literal

class Done(BaseModel):
    content:str = Field(...,description="deliver the content for the user's query in proper markdown format",examples=["The task is completed successfully."])

class Shell(BaseModel):
    shell:str = Field(...,description="Choose the shell according to the OS.",examples=['powershell','bash','cmd'])
    cmd: str = Field(..., description="The command to be executed according to the shell.",examples=['python app.py','cd ..','ls -l','Get-ComputerInfo','Get-PSDrive','Get-Process'])
    # elevated_privileges: bool=Field(description="Indicates whether the command requires elevated privileges.",examples=[True,False],default=False)

class Python(BaseModel):
    mode:Literal['script','package']=Field(description="The mode of operation.",examples=['script','package'],default='script')
    script: str = Field(description="The python script to be executed.",examples=['''print("Hello World")'''],default='')
    packages: list[str] = Field(description="The python package to be installed.",examples=['flask<=2.2','requests'],default=[])
