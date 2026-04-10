import streamlit as st
import os
from dotenv import load_dotenv

# 🔐 Load environment variables
load_dotenv()

# 🔐 Load API keys (works for both local + deployment)
OPENAI_API_KEY = None
HUGGINGFACE_API_KEY = None

try:
    OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
    HUGGINGFACE_API_KEY = st.secrets["HUGGINGFACEHUB_API_TOKEN"]
except:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACEHUB_API_TOKEN")

# ❌ Stop app if key missing
if not OPENAI_API_KEY:
    st.error("❌ OpenAI API key not found. Add it in .env or secrets.toml")
    st.stop()

# Set env variables
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
os.environ["HUGGINGFACEHUB_API_TOKEN"] = HUGGINGFACE_API_KEY or ""

# 📦 Imports after keys
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from pypdf import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from docx import Document


# 🤖 LLM Setup (OpenRouter)
llm = ChatOpenAI(
    model="openai/gpt-4o-mini",
    base_url="https://openrouter.ai/api/v1"
)

parser = StrOutputParser()


# 📄 Extract text
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


# ✂️ Split text (optimized)
def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=200
    )
    return text_splitter.split_text(text)


# 🧠 Create FAISS store
def get_vector_store(text_chunks):
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        base_url="https://openrouter.ai/api/v1"
    )

    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")


# 🔗 Conversation chain
def get_conversation_chain():
    prompt_template = """
    Answer the question as detailed as possible from the provided context.
    If the answer is not in the context, say:
    "Answer is not available in the context."

    Context:
    {context}

    Question:
    {question}

    Answer:
    """

    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"]
    )

    chain = prompt | llm | parser
    return chain


# 💬 Handle query
def user_input(user_question):
    if not os.path.exists("faiss_index"):
        st.warning("⚠️ Please upload and process documents first.")
        return

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        base_url="https://openrouter.ai/api/v1"
    )

    db = FAISS.load_local(
        "faiss_index",
        embeddings,
        allow_dangerous_deserialization=True
    )

    docs = db.similarity_search(user_question, k=4)
    context = "\n\n".join(doc.page_content for doc in docs)

    chain = get_conversation_chain()

    response = chain.invoke({
        "context": context,
        "question": user_question
    })

    st.write("### 🤖 Reply:")
    st.write(response)


# 🖥️ UI
def main():
    st.set_page_config(page_title="Chat with Documents", layout="wide")

    st.header("📄 Chat with Multiple PDFs & DOCX 🧠")

    user_question = st.text_input("💬 Ask a question from your documents")

    if user_question:
        user_input(user_question)

    with st.sidebar:
        st.title("📁 Upload Documents")

        files = st.file_uploader(
            "Upload PDF or DOCX files",
            accept_multiple_files=True
        )

        if st.button("🚀 Submit & Process"):
            if not files:
                st.warning("Please upload at least one file.")
                return

            with st.spinner("Processing documents..."):
                raw_text = get_pdf_text(files)

                if not raw_text.strip():
                    st.error("No readable text found in files.")
                    return

                chunks = get_text_chunks(raw_text)
                get_vector_store(chunks)

                st.success("✅ Documents processed successfully!")


# 🚀 Run
if __name__ == "__main__":
    main()