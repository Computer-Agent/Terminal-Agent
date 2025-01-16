from pydantic import BaseModel, Field

class Shell(BaseModel):
    shell:str = Field(description="The shell to be used. By default Command Prompt for Windows and Bash for Linux and MacOS",examples=['bash','powershell',None],default=None)
    command: str = Field(..., description="The command to be executed according to the shell.",examples=['pip install flask','python app.py','cd ..','ls -l','Get-ComputerInfo','Get-PSDrive','Get-Process'])