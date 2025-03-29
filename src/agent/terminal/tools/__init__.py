from src.agent.terminal.tools.views import Shell,Python
from src.tool import Tool
from subprocess import run
from platform import system
import sys
import io

os=system()

@Tool('Shell Tool',params=Shell)
def shell_tool(shell: str=None,command: str='') -> str:
    '''Executes a shell command on the system and returns the output.'''
    elevated_privileges:bool=False
    try:
        if os=='Windows':
            if shell is None:
                admin_prefix = ["runas","/noprofile","/user:Administrator"] if elevated_privileges else []
                response=run(admin_prefix+command.split(),capture_output=True,text=True)
            elif shell.lower()=='powershell':
                admin_prefix = [] if elevated_privileges else []
                response=run(admin_prefix+[shell,'-Command']+command.split(),capture_output=True,text=True)
            else:
                return 'Shell not supported for Windows'
        elif os=='Linux' or os=='Darwin':
            sudo_prefix = ["sudo"] if elevated_privileges else []
            response=run(sudo_prefix+command.split(),capture_output=True,text=True)
        else:
            raise Exception('OS not supported')
        if response.returncode==0:
            return response.stdout.strip()
        else:
            return f'Error: {response.stderr.strip()}'
    except Exception as e:
        return f'Error: {e}'
    
@Tool('Python Tool',params=Python)
def python_tool(script: str) -> str:
    '''Executes a python script and returns the output.'''
    stdout=sys.stdout
    sys.stdout=io.StringIO()
    try:
        exec(script)
        output=sys.stdout.getvalue()
    except Exception as e:
        output=f'Error: {e}'
    finally:
        sys.stdout=stdout
    return output.strip()