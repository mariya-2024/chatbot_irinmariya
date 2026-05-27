
import streamlit as st

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from groq import Groq



uploaded_files = st.file_uploader(
    "Upload PDFs",
    type="pdf",
    accept_multiple_files=True
)


documents = []

if uploaded_files:

    for uploaded_file in uploaded_files:

        with open(uploaded_file.name, "wb") as f:
            f.write(uploaded_file.getbuffer())

        loader = PyPDFLoader(uploaded_file.name)

        documents.extend(loader.load())



    splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=30
    )

    chunks = splitter.split_documents(documents)

    @st.cache_resource
    def load_embedding_model():

        embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2"
    )
        return embeddings
    
    embeddings = load_embedding_model()

    @st.cache_resource
    def create_vector_db(chunks, embeddings):

        db = Chroma.from_documents(
            chunks,
            embeddings,
            persist_directory="chroma_db"
    )

        return db
    
    db = create_vector_db(
    chunks,
    embeddings
)

client = Groq(
    api_key="ur_api"
)

st.title("📘 RAG Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])

question = st.chat_input("Ask a question")

if question:
    st.session_state.messages.append({
    "role": "user",
    "content": question
})

    docs = db.max_marginal_relevance_search(
    question,
    k=5
)

    context = "\n\n".join([doc.page_content for doc in docs])

    prompt = f"""
Answer the question only using the provided context.
If you could not find the answer, say:
"I am sorry, I could not find the answer in the document."

Context:
{context}

Question:
{question}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=st.session_state.messages+[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    ai_response = response.choices[0].message.content


    st.session_state.messages.append({
    "role": "assistant",
    "content": ai_response
})
    st.chat_message("user").write(question)
    st.chat_message("assistant").write(ai_response)


    with st.expander("Retrieved Chunks"):

        for doc in docs:
            st.write(doc.page_content)
            st.write("------")



