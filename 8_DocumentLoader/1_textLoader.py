from langchain_community.document_loaders import TextLoader
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="openai/gpt-4o-mini", base_url="https://openrouter.ai/api/v1")

parser = StrOutputParser()

prompt = PromptTemplate(
    template='Writea summary of the following\n{poem}',
    input_variables=['poem']
)

loader = TextLoader("8_DocumentLoader/cricket_poem.txt", encoding="utf-8")
docs = loader.load()

#print(docs)
#print(docs[0])

chains = prompt | llm | parser

print(chains.invoke({'poem':docs[0].page_content}))


#PyPDFLoader
#DirectoryLoader
# load vs lazy_load