from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="openai/gpt-4o-mini", base_url="https://openrouter.ai/api/v1")

parser = StrOutputParser()

prompt1 = PromptTemplate(
    template='Create a joke on the {topic}',
    input_variables=['topic']
)
prompt2 = PromptTemplate(
    template='explain the joke {text}',
    input_variables=['text']
)
chain = RunnableSequence(prompt1 , llm , parser,prompt2,llm,parser)

print(chain.invoke({'topic':'Ai'}))