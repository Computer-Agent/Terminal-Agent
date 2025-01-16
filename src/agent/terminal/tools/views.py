from pydantic import BaseModel, Field

class Shell(BaseModel):
    shell:str = Field(..., description="The shell to be used.",examples=['bash','powershell'])
    command: str = Field(..., description="The command to be executed according to the shell.",examples=['pip install flask','python app.py','cd ..','ls -l','Get-ComputerInfo','Get-PSDrive','Get-Process'])