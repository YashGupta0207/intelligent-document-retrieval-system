from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

load_dotenv()

llm = ChatOpenAI(model="openai/gpt-4o-mini", base_url="https://openrouter.ai/api/v1")

class Person(BaseModel):
    name:str=Field(description='Name of the person')
    age:int=Field(gt=18,description='Age of the person')
    city:str=Field(description='Name of the city person belongs to')

parser = PydanticOutputParser(pydantic_object=Person)
tem = PromptTemplate(

    template='Give me the name,age and city of fictional {place} person \n {format_instruction}',
    input_variables=['place'],
    partial_variables={'format_instruction':parser.get_format_instructions()}
)

chain = tem | llm | parser
result = chain.invoke({"place": "Indian"})
print(result)