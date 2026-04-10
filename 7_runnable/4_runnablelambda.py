from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence,RunnableParallel,RunnablePassthrough,RunnableLambda
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="openai/gpt-4o-mini", base_url="https://openrouter.ai/api/v1")

parser = StrOutputParser()

prompt = PromptTemplate(
    template='Gernerate a joke on the {topic}',
    input_variables='topic'
)
joke_gen = RunnableSequence(prompt,llm,parser)
def word_count(text):
    return len(text.split())

parall = RunnableParallel(
    {
        'joke': RunnablePassthrough(),
        'Words' : RunnableLambda(word_count)
    }
)

fan = RunnableSequence(joke_gen,parall)
print(fan.invoke({'topic':'AI'}))