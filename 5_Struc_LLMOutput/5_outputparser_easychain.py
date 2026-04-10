from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
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

pars = StrOutputParser()

chain = t1 | model | pars | t2 | model | pars

re = chain.invoke({'topic':'White Color'})

print(re)