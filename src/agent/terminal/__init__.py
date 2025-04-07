from src.agent.terminal.utils import extract_agent_data,read_markdown_file
from src.agent.terminal.tools import shell_tool,python_tool
from src.message import AIMessage,HumanMessage,SystemMessage
from langgraph.graph import StateGraph,START,END
from src.agent.terminal.state import AgentState
from src.memory.episodic import EpisodicMemory
from src.inference import BaseInference
from src.tool.registry import Registry
from src.agent import BaseAgent
from termcolor import colored
from platform import platform
from datetime import datetime
from getpass import getuser
from src.tool import Tool
from pathlib import Path
import json

tools=[
    shell_tool,python_tool
]

class TerminalAgent(BaseAgent):
    def __init__(self,instructions:list[str]=[],episodic_memory:EpisodicMemory=None,additional_tools:list[Tool]=[],llm:BaseInference=None,verbose:bool=False,max_iteration:int=10,token_usage:bool=False):
        self.llm=llm
        self.verbose=verbose
        self.max_iteration=max_iteration
        self.iteration=0
        self.instructions=self.format_instructions(instructions)
        self.registry=Registry(tools+additional_tools)
        self.system_prompt=read_markdown_file('./src/agent/terminal/prompt/system.md')
        self.observation_prompt=read_markdown_file('./src/agent/terminal/prompt/observation.md')
        self.action_prompt=read_markdown_file('./src/agent/terminal/prompt/action.md')
        self.answer_prompt=read_markdown_file('./src/agent/terminal/prompt/answer.md')
        self.graph=self.create_graph()
        self.episodic_memory=episodic_memory
        self.token_usage=token_usage

    def format_instructions(self,instructions):
        return '\n'.join([f'{i+1}. {instruction}' for (i,instruction) in enumerate(instructions)])

    def reason(self,state:AgentState):
        llm_response=self.llm.invoke(state.get('messages'))
        # print(llm_response.content)
        agent_data=extract_agent_data(llm_response.content)
        thought=agent_data.get('Thought')
        route=agent_data.get('Route')
        if self.verbose:
            print(colored(f'Thought: {thought}',color='light_magenta',attrs=['bold']))
        return {**state,'agent_data': agent_data,'route':route}

    def action(self,state:AgentState):
        agent_data=state.get('agent_data')
        thought=agent_data.get('Thought')
        action_name=agent_data.get('Action Name')
        action_input=agent_data.get('Action Input')
        route=agent_data.get('Route')
        if self.verbose:
            print(colored(f'Action Name: {action_name}',color='blue',attrs=['bold']))
            print(colored(f'Action Input: {action_input}',color='blue',attrs=['bold']))
        tool_result=self.registry.execute(name=action_name,input=action_input)
        observation=tool_result.content
        if self.verbose:
            print(colored(f'Observation: {observation}',color='green',attrs=['bold']))
        if self.verbose and self.token_usage:
            print(f'Input Tokens: {self.llm.tokens.input} Output Tokens: {self.llm.tokens.output} Total Tokens: {self.llm.tokens.total}')
        # Delete the last message
        state.get('messages').pop()
        action_prompt=self.action_prompt.format(thought=thought,action_name=action_name,action_input=json.dumps(action_input,indent=2),route=route)
        observation_prompt=self.observation_prompt.format(observation=observation)
        messages=[AIMessage(action_prompt),HumanMessage(observation_prompt)]
        return {**state,'agent_data':agent_data,'messages':messages}
    
    def answer(self,state:AgentState):
        state['messages'].pop() # Remove the last message for modification
        if self.iteration<self.max_iteration:
            agent_data=state.get('agent_data')
            thought=agent_data.get('Thought')
            final_answer=agent_data.get('Final Answer')
        else:
            thought='Looks like I have reached the maximum iteration limit reached.',
            final_answer='Maximum Iteration reached.'
        answer_prompt=self.answer_prompt.format(thought=thought,final_answer=final_answer)
        messages=[AIMessage(answer_prompt)]
        if self.verbose:
            print(colored(f'Final Answer: {final_answer}',color='cyan',attrs=['bold']))
        return {**state,'output':final_answer,'messages':messages}

    def controller(self,state:AgentState):
        if self.iteration<self.max_iteration:
            self.iteration+=1
            return state.get('route').lower()
        else:
            return 'final' 
        
    def create_graph(self):
        workflow=StateGraph(AgentState)
        workflow.add_node('reason',self.reason)
        workflow.add_node('action',self.action)
        workflow.add_node('answer',self.answer)

        workflow.add_edge(START,'reason')
        workflow.add_conditional_edges('reason',self.controller)
        workflow.add_edge('action','reason')
        workflow.add_edge('answer',END)

        return workflow.compile(debug=False)

    def invoke(self,input:str):
        parameters={
            'instructions':self.instructions,
            'current_datetime':datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'tools_prompt':self.registry.tools_prompt(),
            'os':platform(),
            'home_dir':Path.home().as_posix(),
            'user':getuser(),
        }
        system_prompt=self.system_prompt.format(**parameters)
        # Attach episodic memory to the system prompt 
        if self.episodic_memory and self.episodic_memory.retrieve(input):
            system_prompt=self.episodic_memory.attach_memory(system_prompt)
        human_prompt=f'Task: {input}'
        state={
            'input':input,
            'messages':[SystemMessage(system_prompt),HumanMessage(human_prompt)],
            'agent_data':{},
            'router':'',
            'output':''
        }
        response=self.graph.invoke(state)
        # Extract and store the key takeaways of the task performed by the agent
        if self.episodic_memory:
            self.episodic_memory.store(response.get('messages'))
        return response.get('output')

    def stream(self,input:str):
        pass
        