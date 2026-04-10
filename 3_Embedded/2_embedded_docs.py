from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

embeding = OpenAIEmbeddings(model="openai/text-embedding-3-large",
        base_url="https://openrouter.ai/api/v1",dimensions=24)


docs = ["Delhi is the capital of India","Kolkata is the capital of West Bengal","Paris is the capital of France"]

re = embeding.embed_documents(docs)
print(re)