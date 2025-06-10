import os
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_text_splitters import CharacterTextSplitter

def file_to_chroma(
    file_path: str = "startup-finance-copilot/data/startupInfo.txt",
    db_location: str = "./chroma_pitchdeck",
    collection_name: str = "pitchdeck_collection",
    model_name: str = "mxbai-embed-large"
) -> Chroma:
    """
    Μετατρέπει ένα αρχείο κειμένου σε Chroma vector store χρησιμοποιώντας Ollama Embeddings.

    Επιστρέφει τον Chroma retriever (για RAG).
    """

    if os.path.exists(db_location):
        # print("Φορτώνω υπάρχον vectorstore από cache.")
        return Chroma(
            collection_name=collection_name,
            persist_directory=db_location,
            embedding_function=OllamaEmbeddings(model=model_name)
        )
    # else:
    #     print("Δεν υπάρχει cache, δημιουργώ νέο vectorstore...")
    # Διαβάζουμε το αρχείο
    with open(file_path, "r", encoding="utf-8") as f:
        raw_text = f.read()

    # Τεμαχισμός σε chunks
    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.create_documents([raw_text])  # επιστρέφει λίστα από Documents

    # Προσθήκη metadata και IDs
    documents = []
    ids = []
    for i, doc in enumerate(chunks):
        doc.metadata = {"source": file_path, "chunk": i}
        doc.id = str(i)
        documents.append(doc)
        ids.append(str(i))

    # Ενσωματώσεις
    embeddings = OllamaEmbeddings(model=model_name)

    # Δημιουργία Chroma και αποθήκευση
    vector_store = Chroma(
        collection_name=collection_name,
        persist_directory=db_location,
        embedding_function=embeddings
    )
    vector_store.add_documents(documents=documents, ids=ids)
    print(f"Διαβάζω αρχείο: {file_path}")
    print(f"Πλήθος εγγράφων μετά το φορμάρισμα: {len(documents)}")
    return vector_store
