from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
load_dotenv()

llm = ChatOpenAI(model="openai/gpt-4o-mini", base_url="https://openrouter.ai/api/v1")

pr = PromptTemplate(
    template='Give 5 interesting facts about {topic}',
    input_variables=['topic']
)

parser = StrOutputParser()

chain = pr | llm | parser

re = chain.invoke({'topic':'Cricket'})
print(re)

chain.get_graph().print_ascii()