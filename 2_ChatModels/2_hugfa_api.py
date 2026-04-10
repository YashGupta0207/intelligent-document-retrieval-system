from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="HuggingFaceH4/zephyr-7b-beta",
    task="conversational",   
)

model = ChatHuggingFace(llm=llm)

res = model.invoke("What is the capital of Uttar Pradesh?")
print(res.content)
