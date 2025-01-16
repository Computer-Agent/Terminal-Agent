from src.agent.terminal.tools.views import Shell
from src.tool import Tool
from subprocess import run

@Tool('Shell Tool',params=Shell)
def shell_tool(command: str,shell: str) -> str:
    '''Executes a shell command on the system and returns the output.'''
    try:
        if shell.lower()=='powershell': #For Windows
            response=run([shell,'-Command']+command.split(),capture_output=True,text=True)
        else: #For Linux,MacOS
            response=run([shell,'-c']+command.split(),capture_output=True,text=True)
        if response.returncode==0:
            return response.stdout.strip()
        else:
            return response.stderr.strip()
    except Exception as e:
        return str(e)