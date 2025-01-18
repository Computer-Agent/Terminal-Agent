import subprocess

# Command that you want to run as administrator
command_to_run = 'Get-VM'

# Relaunch PowerShell with admin privileges to execute the command
def run_as_admin(command):
    # Run PowerShell as an administrator and capture output
    response = subprocess.run(
        ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", command],
        capture_output=True, text=True, shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE
    )
    
    # Check for successful execution
    if response.returncode == 0:
        print(response.stdout)  # Output of the command
    else:
        print(f"Error occurred: {response.stderr}")

# Main logic: Run the command as administrator
run_as_admin(command_to_run)
