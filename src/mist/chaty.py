import logging
import config

from langchain_mistralai import ChatMistralAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

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
        system_msg = SystemMessage('You are a helpful assistant that responds to questions with three exclamation marks.')
        human_msg = HumanMessage('What is the capital of France?')
        completion = self.llm.invoke([system_msg, human_msg])
        print(completion.content)
