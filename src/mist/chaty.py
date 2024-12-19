import logging
import config

from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import PromptTemplate

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

        template = PromptTemplate.from_template("""Answer the question based on the context below. 
                                                If the question cannot be answered using the information provided answer with "I don't know".
        Context: {context}
        Question: {question}
        Answer: """)
        
        prompt = template.invoke({
            "context": "The most recent advancements in NLP are being driven by Large Language Models (LLMs). These models outperform their smaller counterparts and have become invaluable for developers who are creating applications with NLP capabilities. Developers can tap into these models through Hugging Face's `transformers` library, or by utilizing OpenAI and Cohere's offerings through the `openai` and `cohere` libraries respectively.",
            "question": "Which model providers offer LLMs?"
        })
        completion = self.llm.invoke(prompt)
        print(completion.content)
