from pydantic import BaseModel, Field

class Shell(BaseModel):
    shell:str = Field(...,description="Choose the shell according to the OS.",examples=['powershell','bash','cmd'])
    command: str = Field(..., description="The command to be executed according to the shell.",examples=['pip install flask','python app.py','cd ..','ls -l','Get-ComputerInfo','Get-PSDrive','Get-Process'])
    # elevated_privileges: bool=Field(description="Indicates whether the command requires elevated privileges.",examples=[True,False],default=False)

class Python(BaseModel):
    script: str = Field(..., description="The python script to be executed.",examples=['''print("Hello World")'''])