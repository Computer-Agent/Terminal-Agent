from src.agent.terminal.tools.views import Shell,Python,Done
from typing import Literal
from src.tool import Tool
from subprocess import run,check_call
from platform import system
from importlib.util import find_spec
import sys
import io

os=system()

@Tool('Done Tool',params=Done)
def done_tool(content:str):
    '''To indicate that the task is completed'''
    return content

@Tool('Shell Tool',params=Shell)
def shell_tool(shell: str=None,cmd: str='') -> str:
    '''Executes a shell command on the system and returns the output.'''
    elevated_privileges:bool=False
    try:
        if os=='Windows':
            if shell is None:
                admin_prefix = ["runas","/noprofile","/user:Administrator"] if elevated_privileges else []
                response=run(admin_prefix+cmd.split(),capture_output=True,text=True)
            elif shell.lower()=='powershell':
                admin_prefix = [] if elevated_privileges else []
                response=run(admin_prefix+[shell,'-Command']+cmd.split(),capture_output=True,text=True)
            else:
                return 'Shell not supported for Windows'
        elif os=='Linux' or os=='Darwin':
            sudo_prefix = ["sudo"] if elevated_privileges else []
            response=run(sudo_prefix+cmd.split(),capture_output=True,text=True)
        else:
            raise Exception('OS not supported')
        if response.returncode==0:
            return response.stdout.strip()
        else:
            return f'Error: {response.stderr.strip()}'
    except Exception as e:
        return f'Error: {e}'
    
@Tool('Python Tool',params=Python)
def python_tool(mode:Literal['script','package']='script',script: str='',packages: list[str]=[]) -> str:
    '''Executes a python script and returns the output.'''
    if mode=='script':
        stdout=sys.stdout
        sys.stdout=io.StringIO()
        try:
            exec(script,globals={'__builtins__':__builtins__})
            output=sys.stdout.getvalue()
        except Exception as e:
            output=f'Error: {e}'
        finally:
            sys.stdout=stdout
        return output.strip()
    elif mode=='package':
        packages=list(filter(lambda package: find_spec(package) is None,packages))
        if not packages:
            return 'All packages are already installed'
        packages_string=' '.join(packages)
        try:
            check_call([sys.executable, "-m", "pip", "install", packages_string])
        except Exception as e:
            return f'Error: {e}'
        return f'{packages_string} installed successfully'
    else:
        raise Exception('Mode not supported')