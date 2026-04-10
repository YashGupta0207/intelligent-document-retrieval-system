from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StructuredOutputParser, ResponseSchema

###### StrucucredOutputparser is removed from the langchain
load_dotenv()

llm = ChatOpenAI(model="openai/gpt-3.5-turbo-instruct", base_url="https://openrouter.ai/api/v1")

schema = [
    ResponseSchema(name='fact_1', description='Fact 1 about the topic' ),
     ResponseSchema(name='fact_2', description='Fact 2 about the topic' ),
      ResponseSchema(name='fact_3', description='Fact 3 about the topic' )
]

parser = StructuredOutputParser

tem = PromptTemplate(

    template='Give 3 facts about the topic \n {format_instruction}',
    input_variables=['topic'],
    partial_variables={'format_instruction':parser.get_format_instructions()}
)
p = tem.format({'topic':'Red Color'})
re = llm.invoke(p)
fi = parser.parse(re.content)
print(fi)