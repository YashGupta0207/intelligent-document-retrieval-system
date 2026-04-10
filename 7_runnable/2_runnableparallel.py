from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence,RunnableParallel
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="openai/gpt-4o-mini", base_url="https://openrouter.ai/api/v1")

prompt1 = PromptTemplate(
    template='Generate a tweet about{topic}',
    input_variables=['topic']
)

prompt2 = PromptTemplate(
    template='Generate a linkdin post for the {topic}',
    input_variables=['topic']
)

parser = StrOutputParser()

parallel_chain = RunnableParallel(
    {
        'tweet':RunnableSequence(prompt1,llm,parser),
        'linkdin':RunnableSequence(prompt2,llm,parser)
    })

print(parallel_chain.invoke({'topic':'AI'}))