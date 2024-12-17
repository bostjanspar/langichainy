import logging
import config
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import HumanMessage
from langchain_core.pydantic_v1 import BaseModel

# Get logger for this module
logger = logging.getLogger(__name__)



class AnswerWithJustification(BaseModel):
    '''An answer to the user question along with justification for the answer.'''
    answer: str
    '''The answer to the user's question'''
    justification: str
    '''Justification for the answer'''

class MistralChaty:
    def __init__(self):        
        logger.info(f"Initializing Mistral LLM  model {config.MISTRAL_MODEL}")
        self.llm = ChatMistralAI(
            model=config.MISTRAL_MODEL,
            temperature=0
        )
    
    def chat(self):
        logger.info("Starting chat")
        # messages = [
        #     (
        #         "system",
        #         "You are a helpful assistant that translates English to French. Translate the user sentence.",
        #     ),
        #     ("human", "I love programming."),
        # ]
        # ai_msg = self.llm.invoke(messages)
        # print(ai_msg.content)
        prompt = [HumanMessage('What is the capital of France?')]
        completion = self.llm.invoke(prompt)
        print(completion.content)

    def chatStruct(self):
        logger.info("Starting chat")

        structured_llm =  self.llm.with_structured_output(AnswerWithJustification)      
        completion =  structured_llm.invoke("What weighs more, a pound of bricks or a pound of feathers")
        print(completion)
    