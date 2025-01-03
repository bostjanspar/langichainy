from itertools import chain
import logging
import config

from langchain_ollama import ChatOllama
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import HumanMessage

from langgraph.graph import StateGraph, START, END
from langgraph.graph import MessagesState
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition


# Get logger for this module
logger = logging.getLogger(__name__)


def multiply(a: int, b: int) -> int:
    """Multiply a and b.

    Args:
        a: first int
        b: second int
    """
    return a * b


class MistralRouter:
    def __init__(self):        
        logger.info(f"Initializing Mistral LLM  model {config.MISTRAL_MODEL}")
        # self.llm = ChatMistralAI(
        #     model=config.MISTRAL_MODEL,
        #     temperature=0
        # )
        self.llm = ChatOllama(
            model="llama3.2",
            temperature=0
        )
        self.llm_with_tools =  self.llm.bind_tools([multiply])

        # Build graph
        builder = StateGraph(MessagesState)
        builder.add_node("tool_calling_llm", self.tool_calling_llm)
        builder.add_node("tools", ToolNode([multiply]))
        builder.add_edge(START, "tool_calling_llm")
        builder.add_conditional_edges(
            "tool_calling_llm",
            # If the latest message (resultool_calling_llmt) from assistant is a tool call -> tools_condition routes to tools
            # If the latest message (result) from assistant is a not a tool call -> tools_condition routes to END
            tools_condition,
        )
        builder.add_edge("tools", END)
        self.graph = builder.compile()


    def tool_calling_llm(self, state: MessagesState):
        return {"messages": [self.llm_with_tools.invoke(state["messages"])]}

    
    def doStuff(self):
        logger.info("do Stuff")
        messages = [HumanMessage(content="multi 2 and 5")]
        messages = self.graph.invoke({"messages": messages})
        for m in messages['messages']:
            m.pretty_print()
                
