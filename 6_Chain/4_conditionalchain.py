from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel,RunnableBranch,RunnableLambda
from pydantic import BaseModel,Field
from typing import Literal
from langchain_core.output_parsers import PydanticOutputParser
load_dotenv()

llm1 = ChatOpenAI(model="openai/gpt-4o-mini", base_url="https://openrouter.ai/api/v1")

parser1 = StrOutputParser()

class Feedback(BaseModel):
    sentiment: Literal['positive','negative'] = Field(description='Give the sentiment of the feedback')

parser2 = PydanticOutputParser(pydantic_object=Feedback)    

tem = PromptTemplate(
    template='Classify the sentiment of the following feedback into positive or negative \n {feedback}\n {format_instruction}' ,
    input_variables=['feedback'],
    partial_variables={'format_instruction':parser2.get_format_instructions()}
)

classifier_chain =  tem | llm1 |parser2

p1 = PromptTemplate(
    template='Write an appropriate response to the positive feedback.\n{feedback}',
    input_variables=['feedback']
)

p2 = PromptTemplate(
    template='Write an appropriate response to the negative feedback.\n{feedback}',
    input_variables=['feedback']
)

branch = RunnableBranch(
    (lambda x:x.sentiment=='positive',  p1 | llm1 | parser1 ),
    (lambda x:x.sentiment == 'negative', p2 | llm1 | parser1),
    RunnableLambda(lambda x: 'Could not find sentiment')
)

chain = classifier_chain | branch

print(chain.invoke({'feedback':'This is a terrible phone'}))




