from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate

load_dotenv()

model = ChatOpenAI(model="openai/gpt-3.5-turbo-instruct", base_url="https://openrouter.ai/api/v1")

t1 = PromptTemplate(
    template='Write a detailed report on{topic}',
    input_variables=['topic']
)

t2 = PromptTemplate(
    template='write 2 line summary on the following text----{text}',
    input_variables=['text']
)

p1 = t1.invoke({'topic':'White Color'})

r1 = model.invoke(p1)
p2=t2.invoke({'text':r1.content})

r2 = model.invoke(p2)

print(r2.content)