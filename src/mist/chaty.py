from itertools import chain
import logging
import config

from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate

# Get logger for this module
logger = logging.getLogger(__name__)

class MistralChaty:
    def __init__(self):        
        logger.info(f"Initializing Mistral LLM  model {config.MISTRAL_MODEL}")
        self.llm = ChatMistralAI(
            model=config.MISTRAL_MODEL,
            temperature=0
        )
    
    def chat(self):
        logger.info("Starting chat")

        template = ChatPromptTemplate.from_messages([
            ('system', 'You are a helpful assistant.'),
            ('human', '{question}'),
        ])

        chatbot = template | self.llm 

        result = chatbot.invoke({
                "question": "Which model providers offer LLMs?"
            })
        print(result.content)
                
