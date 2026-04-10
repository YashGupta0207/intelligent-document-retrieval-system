from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="openai/gpt-3.5-turbo-instruct", base_url="https://openrouter.ai/api/v1")

re = llm.invoke("What is the capital of India")

print(re.content)