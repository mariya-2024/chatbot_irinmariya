#This is code for loading pdf
from langchain_community.document_loaders import PyPDFLoader


from langchain_community.document_loaders import PyPDFLoader

pdf_files = [
    "pdf_files/KMC 2004 Phase Trans.pdf"
]

documents = []

for pdf in pdf_files:
    loader = PyPDFLoader(pdf)
    documents.extend(loader.load())

#codee for splitting the pdf into chunks 
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

chunks = splitter.split_documents(documents)


#code for printing chunks
'''for chunk in chunks[:3]: #printing only 3 chunks  
    print(chunk.page_content)
    print("-" * 50) #seperator line

print(type(chunks))
print(len(chunks))'''


#embedding model code
from langchain_huggingface import HuggingFaceEmbeddings
embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)


#storing chunks and embeddings in chroma db 
from langchain_community.vectorstores import Chroma
db = Chroma.from_documents(
    chunks,
    embeddings,
    persist_directory="chroma_db"
)



#asking question from user and retrieving relevant chunks step and printing 
from groq import Groq
client = Groq(
        api_key="ur_api key"
    )



messages = []

while True:

    question = input("Ask a question: ")

    if question.lower() == "exit":
        break

    docs = db.similarity_search(question, k=10)

    print("\nRetrieved Chunks:\n")

    for i, doc in enumerate(docs):
        print(f"Chunk {i+1}:\n")
        print(doc.page_content)
        print("\n" + "-"*80 + "\n")

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

    # append user message
    messages.append({
        "role": "user",
        "content": prompt
    })

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages
    )

    ai_response = response.choices[0].message.content

    # append assistant response
    messages.append({
        "role": "assistant",
        "content": ai_response
    })

    print("\nFinal Answer:\n")
    print(ai_response)