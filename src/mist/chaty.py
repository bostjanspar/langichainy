import logging
import config

from langchain_mistralai import ChatMistralAI
from langchain_core.messages import HumanMessage

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
        prompt = [HumanMessage('What is the capital of France?')]
        completion = self.llm.invoke(prompt)
        print(completion.content)
