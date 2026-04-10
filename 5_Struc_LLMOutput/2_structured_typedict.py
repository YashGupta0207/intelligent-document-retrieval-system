from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from typing import TypedDict,Annotated

load_dotenv()

llm = ChatOpenAI(model="openai/gpt-4o-mini", base_url="https://openrouter.ai/api/v1")

class Review(TypedDict):
    summary:str
    sentiment:str
    name: Annotated[list[str],"write the name of the reviewer"]

struct = llm.with_structured_output(Review)

res = struct.invoke("The hardware is great but software got bloated. There are two many apps that i cannot remove. Also the UI looks outdated compared to other brands. Hoping for a software update to fix reviewd by yash")

print(res)
