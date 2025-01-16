from pydantic import BaseModel, Field

class Shell(BaseModel):
    command: str = Field(..., description="The shell command to be executed.",examples=['pip install flask','python app.py','cd ..','ls -l','Get-ComputerInfo','Get-PSDrive','Get-Process'])
    shell:str = Field(..., description="The shell to be used.",examples=['bash','powershell'])