from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
load_dotenv()

llm = ChatOpenAI(model="openai/gpt-4o-mini", base_url="https://openrouter.ai/api/v1")

p1 = PromptTemplate(
    template='Generate a detailed report on {topic}',
    input_variables=['topic']
)

parser =StrOutputParser()

p2 = PromptTemplate(
    template='Give 2 important line of the {description}',
    input_variables=['description']
)

chain = p1 | llm | parser | p2 | llm | parser

re = chain.invoke({'topic':'Cricket'})
#print(re)
chain.get_graph().print_ascii()