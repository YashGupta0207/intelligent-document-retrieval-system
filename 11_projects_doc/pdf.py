from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
import streamlit as st
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from docx import Document
from langchain_core.output_parsers import StrOutputParser
load_dotenv()

llm = ChatOpenAI(model="openai/gpt-4o-mini", base_url="https://openrouter.ai/api/v1")
parser = StrOutputParser()
def get_pdf_text(files):
    text = ""

    for file in files:
        if file.name.endswith(".pdf"):
            reader = PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() or ""

        elif file.name.endswith(".docx"):
            doc = Document(file)
            for para in doc.paragraphs:
                text += para.text + "\n"

        else:
            st.warning(f"Unsupported file type: {file.name}")

    return text

def get_text_chunks(text):
    text_split = RecursiveCharacterTextSplitter(chunk_size = 10000,chunk_overlap = 2000)
    chunks = text_split.split_text(text)
    return chunks

def get_vector_store(text_chunks):
    embed = OpenAIEmbeddings(model="text-embedding-3-small",base_url="https://openrouter.ai/api/v1")
    vector_store = FAISS.from_texts(text_chunks,embedding=embed)
    vector_store.save_local("faiss_index")


def get_conver_chain():
    prompt_temp = """Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in the provided  context just say,"answer is not available in the context" don't provide the wrong answer.
    
    Context: \n{context}\n
    Question: \n{question}\n

    Answer:
    """
    prompt = PromptTemplate(template=prompt_temp,input_variables=['context','question'])
    chain = prompt | llm | parser

    return chain

def user_input(user_question):
    embedd = OpenAIEmbeddings(
        model="text-embedding-3-small",
        base_url="https://openrouter.ai/api/v1"
    )

    new_db = FAISS.load_local(
    "faiss_index",
    embedd,
    allow_dangerous_deserialization=True
)


    docs = new_db.similarity_search(user_question)

    context = "\n\n".join(doc.page_content for doc in docs)

    chain = get_conver_chain()

    response = chain.invoke({
        "context": context,
        "question": user_question
    })

    st.write("Reply:", response)


def main():
    st.set_page_config("Chat With Multiple PDF")
    st.header("Chat with Multiple PDF using OpenAI🧑‍💻")

    user_question = st.text_input("Ask a Question from the PDF Files")

    if user_question:
        user_input(user_question)

    with st.sidebar:
        st.title("Menu:")
        pdf_docs = st.file_uploader(
            "Upload your PDF Files and Click on the Submit & Process Button",
            accept_multiple_files=True
        )
        if st.button("Submit & Process"):
            with st.spinner("Processing..."):
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunks(raw_text)
                get_vector_store(text_chunks)
                st.success("Done")
 

if __name__ == '__main__':
    main()