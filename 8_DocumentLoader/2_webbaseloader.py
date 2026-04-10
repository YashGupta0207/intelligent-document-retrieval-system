from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="openai/gpt-4o-mini", base_url="https://openrouter.ai/api/v1")

parser = StrOutputParser()

prompt = PromptTemplate(
    template='Answer the following question {question}from the {text}',
    input_variables=['question','topic']
)
url ='https://www.flipkart.com/apple-macbook-air-m4-16-gb-256-gb-ssd-macos-sequoia-mc6t4hn-a/p/itm7c1831ce25509'

loader = WebBaseLoader(url)
q = input('Enter the quesion')
docs = loader.load()

chain = prompt | llm | parser

print(chain.invoke({'question':q,'text':docs[0].page_content}))