import logging
from langchain_mistralai import  MistralAIEmbeddings


from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_chroma import Chroma

# Get logger for this module
logger = logging.getLogger(__name__)

class MissLoad:
    def __init__(self):
        logger.info("Initializing Mistral Embeddings")
        emb = MistralAIEmbeddings(
            model="mistral-embed",
        )

        self.vector_store = Chroma(
            collection_name="example_collection",
            embedding_function=emb,
            persist_directory="./chroma_langchain_db",  # Where to save data locally, remove if not necessary
        )
        
    
    def load(self):
        logger.info("Starting load")
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=100,
            chunk_overlap=20,
            length_function=len,
            is_separator_regex=False
        )
        doc = text_splitter.split_documents(TextLoader(file_path="HUNGER.txt").load())
        self.vector_store.add_documents(doc)

    def query(self, txt:str):
        logger.info("Starting query")
        return self.vector_store.as_retriever().invoke(txt)