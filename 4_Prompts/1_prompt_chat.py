from langchain_core.messages import SystemMessage,HumanMessage,AIMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="openai/gpt-4o-mini", base_url="https://openrouter.ai/api/v1")
chat = [SystemMessage(content='You are an helpful assistant')]
while True:
    user_input = input("You:")
    chat.append(HumanMessage(content=user_input))
    if(user_input == 'exit'):
        break
    re = llm.invoke(chat)
    chat.append(AIMessage(content=re.content))
    print("AI:" , re.content)

print(chat)