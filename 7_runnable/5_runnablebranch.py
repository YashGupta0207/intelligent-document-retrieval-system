from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence,RunnableParallel,RunnablePassthrough,RunnableBranch,RunnableLambda
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="openai/gpt-4o-mini", base_url="https://openrouter.ai/api/v1")

parser = StrOutputParser()

prompt = PromptTemplate(
    template='Gernerate a report on the {topic}',
    input_variables=['topic']
)
prompt2 = PromptTemplate(
    template='summarize the text {text}',
    input_variables=['text']
)
report = RunnableSequence(prompt,llm,parser)


branch = RunnableBranch(
    (lambda x:len(x.split())>100,RunnableLambda(lambda x: {"text": x}) | prompt2 | llm | parser),
    RunnablePassthrough()
)
final =RunnableSequence(report,branch)
print(final.invoke({'topic':'AI'}))
