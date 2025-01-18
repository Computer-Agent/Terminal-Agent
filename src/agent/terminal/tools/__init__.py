from src.agent.terminal.tools.views import Shell
from src.tool import Tool
from subprocess import run
from platform import system

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
            return response.stderr.strip()
    except Exception as e:
        return str(e)