from src.inference.gemini import ChatGemini
from src.inference.groq import ChatGroq
from src.agent.terminal import TerminalAgent
from dotenv import load_dotenv
import os

load_dotenv()

# api_key=os.getenv('GROQ_API_KEY')
# llm=ChatGroq(model='llama-3.3-70b-versatile',api_key=api_key,temperature=0)

api_key=os.getenv('GOOGLE_API_KEY')
llm=ChatGemini(model='gemini-2.0-flash-exp',api_key=api_key,temperature=0)

agent=TerminalAgent(llm=llm,verbose=True)
user_query=input('Enter your query: ')
agent_response=agent.invoke(user_query)
print(agent_response)