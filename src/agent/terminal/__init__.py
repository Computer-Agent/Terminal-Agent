from src.agent.terminal.utils import extract_llm_response,read_markdown_file
from src.message import AIMessage,HumanMessage,SystemMessage
from langgraph.graph import StateGraph,START,END
from src.agent.terminal.state import AgentState
from src.inference import BaseInference
from src.agent import BaseAgent
from termcolor import colored
from subprocess import run
from platform import platform
from getpass import getuser
from os import getcwd

class TerminalAgent(BaseAgent):
    def __init__(self,llm:BaseInference=None,verbose:bool=False,max_iteration:int=10):
        self.llm=llm
        self.verbose=verbose
        self.max_iteration=max_iteration
        self.iteration=0
        self.system_prompt=read_markdown_file('./src/agent/terminal/prompt.md')
        self.graph=self.create_graph()

    def reason(self,state:AgentState):
        llm_response=self.llm.invoke(state.get('messages'))
        # print(llm_response.content)
        agent_data=extract_llm_response(llm_response.content)
        # print(dumps(agent_data,indent=2))
        if self.verbose:
            thought=agent_data.get('Thought')
            print(colored(f'Thought: {thought}',color='light_magenta',attrs=['bold']))
        return {**state,'agent_data': agent_data}

    def action(self,state:AgentState):
        agent_data=state.get('agent_data')
        thought=agent_data.get('Thought')
        command=agent_data.get('Command')
        route=agent_data.get('Route')
        if self.verbose:
            print(colored(f'Command: {command}',color='blue',attrs=['bold']))
        try:
            result=run(command.split(),capture_output=True,text=True)
            if result.returncode==0:
                observation=result.stdout
            else:
                observation=result.stderr
        except Exception as e:
            observation=str(e)
        if self.verbose:
            print(colored(f'Observation: {observation}',color='green',attrs=['bold']))
        ai_prompt=f'<Thought>{thought}</Thought>\n<Command>{command}</Command>\n\n<Route>{route}</Route>'
        user_prompt=f'<Observation>{observation}</Observation>'
        messages=[AIMessage(ai_prompt),HumanMessage(user_prompt)]
        return {**state,'agent_data':agent_data,'messages':messages}
    
    def final(self,state:AgentState):
        agent_data=state.get('agent_data')
        final_answer=agent_data.get('Final Answer')
        if self.verbose:
            print(colored(f'Final Answer: {final_answer}',color='cyan',attrs=['bold']))
        return {**state,'output':final_answer}

    def main_controller(self,state:AgentState):
        agent_data=state.get('agent_data')
        route=agent_data.get('Route').lower()
        return route
        

    def create_graph(self):
        workflow=StateGraph(AgentState)
        workflow.add_node('reason',self.reason)
        workflow.add_node('action',self.action)
        workflow.add_node('final',self.final)

        workflow.add_edge(START,'reason')
        workflow.add_conditional_edges('reason',self.main_controller)
        workflow.add_edge('action','reason')
        workflow.add_edge('final',END)

        return workflow.compile(debug=False)

    def invoke(self,input:str):
        parameters={
            'os':platform(),
            'cwd':getcwd(),
            'user':getuser()
        }
        system_prompt=self.system_prompt.format(**parameters)
        user_prompt=f'Query: {input}'
        state={
            'input':input,
            'messages':[SystemMessage(system_prompt),HumanMessage(user_prompt)],
            'agent_data':None,
            'output':None
        }
        graph_response=self.graph.invoke(state)
        return graph_response['output']

    def stream(self,input:str):
        pass
        