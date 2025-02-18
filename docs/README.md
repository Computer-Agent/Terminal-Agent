# Terminal Agent: Automating Command-Line Tasks with AI

## Overview

**Terminal Agent** is a standalone agent designed to handle and execute shell commands based on user queries. It directly interacts with the terminal environment, performs the necessary shell operations, and returns the results to the user.

### Workflow

1. The **Terminal Agent** receives a user query.
2. It parses the query and translates it into the appropriate shell command.
3. The **Terminal Agent** executes the command in the terminal environment using the correct shell for the operating system.
4. The results from the command execution are returned to the user.

## Key Features

- **Shell Command Execution**: Handles a wide range of shell-based tasks like file manipulation, network operations, package management, and more.
- **Cross-Platform Shell Support**: Automatically selects the appropriate shell based on the operating system:
  - **Linux/macOS**: Uses **Bash** (or the default shell).
  - **Windows**: Uses **PowerShell** (or **Command Prompt**, depending on user preference or system configuration).
- **Error Handling**: Provides clear feedback when a command fails or encounters issues during execution.
- **Simple Interface**: Users interact directly with the terminal, making it straightforward and easy to use.
- **Standalone**: No dependencies on other systems; this project functions on its own as an independent tool.

## Installation

To set up the project, make sure you have Python 3.x installed. Then, run the following command to install the necessary dependencies:

```bash
pip install -r requirements.txt
```

### Running the Application

To start using **Terminal Agent**, execute the following command:

```bash
python app.py
Enter your query: <your task goes here>
```

## Usage

To begin using **Terminal Agent**, follow these steps:

1. Run the application by executing `python app.py`.
2. Enter your query, and **Terminal Agent** will make the command and execute it in the appropriate shell for your operating system.
3. The output of the shell command will be returned to you.

---

**Note:**  
*Please be aware that this agent executes commands directly on your machine's terminal. Make sure you trust the commands you are running and ensure that they do not pose any security risks. Use caution when executing shell commands, especially those that can modify system files, configurations, or data.*

---

### Usage Example

## **Task: Change the system from light to dark mode**
```plaintext
Enter your query: Can you change the system currently in light mode can change it to dark mode           
Thought: I need to use a command to change the system theme to dark mode. I will use the powershell command to achieve this.
Action Name: Shell Tool
Action Input: {'shell': 'powershell', 'command': 'Set-ItemProperty -Path HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize -Name AppsUseLightTheme -Value 0'}
Observation: 
Thought: The command to change the theme to dark mode has been executed. Now I need to execute another command to change the system theme to dark mode as well.
Action Name: Shell Tool
Action Input: {'shell': 'powershell', 'command': 'Set-ItemProperty -Path HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize -Name SystemUsesLightTheme -Value 0'}
Observation: 
Thought: I have executed the necessary commands to change the system theme to dark mode. I am confident that the task is complete.
Final Answer: The system theme has been changed to dark mode.
```

## **Task: Asking about GPU present in the Machine**
```plaintext
Enter your query: Can you tell me which all graphics card I have in this machine?
Thought: To find out which graphics cards are installed in the machine, we can use the command-line interface to query the system for this information. Since the operating system is Windows, we can utilize the Windows Management Instrumentation Command (WMIC) or use PowerShell commands to achieve this. Here, we'll opt for using PowerShell as it provides a more straightforward and user-friendly output for such queries.
Action Name: Shell Tool
Action Input: {'command': 'Get-WMIObject -Class Win32_VideoController | Select-Object Name', 'shell': 'powershell'}
Observation: Name                              
----                              
Intel(R) Iris(R) Xe Graphics      
NVIDIA GeForce RTX 4060
Thought: Based on the observation, the system has two graphics cards installed: Intel(R) Iris(R) Xe Graphics and NVIDIA GeForce RTX 4060 . This information is obtained from the PowerShell command that queried the Win32_VideoController class, which represents the graphics cards installed on the system. Since we have successfully retrieved the list of graphics cards, we can now provide the final answer.
Final Answer: The system has two graphics cards: Intel(R) Iris(R) Xe Graphics and NVIDIA GeForce RTX 4060 .
```

### **Task: Asking the Time**
```plaintext
Enter your query: Can you tell me the time right now
Thought: The user wants to know the current time. I can use the `date` command in the shell to get the current time.
Action Name: Shell Tool
Action Input: {'shell': 'powershell', 'command': 'Get-Date'}
Observation: 16 January 2025 09:19:04
Thought: I have successfully retrieved the current date and time using the `Get-Date` command. Now I can provide the final answer to the user.
Final Answer: The current date and time is 2025-01-16 09:19:04.
```

## License

This project is licensed under the GNU Affero General Public License v3.0 (AGPL-3.0) - see the [LICENSE](LICENSE) file for details.

For more information about the AGPL-3.0 license, please visit: https://www.gnu.org/licenses/agpl-3.0.en.html

---

## Contributions

Feel free to fork the repository and contribute! If you encounter any issues or have suggestions for improvements, submit an issue or a pull request. Contributions are always welcome!

## **Contact**

For queries or support, please reach out via GitHub Issues.

E-mail: jeogeoalukka@gmail.com