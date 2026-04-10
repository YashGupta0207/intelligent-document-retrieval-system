from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

embed = OpenAIEmbeddings(model="openai/text-embedding-3-large",
        base_url="https://openrouter.ai/api/v1",dimensions=24)

re = embed.embed_query("Delhi is the capital of India")
print(re)