from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage
from dotenv import load_dotenv

load_dotenv()
message = [SystemMessage(content='You are an helpful assistant'),HumanMessage(content='What is the capital of India')    ]
llm = ChatOpenAI(model="openai/gpt-3.5-turbo-instruct", base_url="https://openrouter.ai/api/v1")

re = llm.invoke(message)
message.append(AIMessage(content=re.content))

print(message)