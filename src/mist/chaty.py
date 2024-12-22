from itertools import chain
import logging
import config

from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate

from mist.emb import MissLoad

# Get logger for this module
logger = logging.getLogger(__name__)

class MistralChaty:
    def __init__(self):        
        logger.info(f"Initializing Mistral LLM  model {config.MISTRAL_MODEL}")
        self.llm = ChatMistralAI(
            model=config.MISTRAL_MODEL,
            temperature=0
        )
    
    def chat(self, langfuse_handler):
        question = "Wie lange hat Hungerkünstler gehungert ?"
        docs = MissLoad().query(question)
        logger.info("Starting chat")

        prompt = ChatPromptTemplate.from_template("""Beantworte die Frage nur basierend auf dem folgenden Kontext.
            {context}
            Frage: {question}
            """)

        chatbot = prompt | self.llm 
        result =chatbot.invoke({"context": docs,"question": question}, config={"callbacks": [langfuse_handler]})
    
        print(result.content)
                
