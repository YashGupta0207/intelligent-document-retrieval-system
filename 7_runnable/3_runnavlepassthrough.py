from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence,RunnableParallel,RunnablePassthrough
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="openai/gpt-4o-mini", base_url="https://openrouter.ai/api/v1")

parser = StrOutputParser()

prompt = PromptTemplate(
    template='Gernerate a joke on the {topic}',
    input_variables='topic'
)

prompt2 = PromptTemplate(
    template='Explain the joke {joke}',
    input_variables='joke'
)
sequ = RunnableSequence(prompt,llm,parser)
parallel_chain = RunnableParallel(
    {
        'joke': RunnablePassthrough(),
        'expla':RunnableSequence(prompt2,llm,parser)
    }
)

final = RunnableSequence(sequ,parallel_chain)

print(final.invoke({'topic':'AI'}))