from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

load_dotenv()

llm = ChatOpenAI(model="openai/gpt-3.5-turbo-instruct", base_url="https://openrouter.ai/api/v1")

parser = JsonOutputParser()

tem = PromptTemplate(

    template='Give me the name,age and city of fictional person \n {format_instruction}',
    input_variables=[],
    partial_variables={'format_instruction':parser.get_format_instructions()}
)
p = tem.format()
re = llm.invoke(p)
fi = parser.parse(re.content)
print(fi)