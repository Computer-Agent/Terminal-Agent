import subprocess
import tempfile
import os

# Create a temporary file using tempfile
with tempfile.NamedTemporaryFile(delete=False, mode='w', newline='', suffix='.txt') as temp_file:
    output_file = temp_file.name
    print(f"Temporary file created at: {output_file}")

    # PowerShell command to run Get-VM and save output to the temporary file
    command = (
        rf'powershell.exe -Command "& {{Start-Process powershell -ArgumentList '
        rf'\'-NoProfile -Command ""Get-VM | Format-Table -AutoSize | Out-File -FilePath \"{output_file}\"""\' -Verb RunAs}}"'
    )

    try:
        # Execute the command
        subprocess.run(command, shell=True, check=True)
        print(f"Command executed. Output should be saved to {output_file}.")

        # Check if output file exists, then read it
        if os.path.exists(output_file):
            with open(output_file, 'r') as file:
                output = file.read()
                print("Command output:")
                print(output)
        else:
            print("No output file was created. Ensure the command ran successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
    finally:
        # Optionally remove the temporary file after use
        os.remove(output_file)
        print(f"Temporary file {output_file} deleted.")
