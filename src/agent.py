import logging
import os

from langchain_ollama import ChatOllama


from langgraph.graph import MessagesState
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import START, StateGraph
from langgraph.prebuilt import tools_condition
from langgraph.prebuilt import ToolNode

# Get logger for this module
logger = logging.getLogger(__name__)

# System message


from langfuse import Langfuse

# get keys for your project from https://cloud.langfuse.com
os.environ["LANGFUSE_PUBLIC_KEY"] = "pk-lf-4f776735-0697-401c-85f3-6391370d9720"
os.environ["LANGFUSE_SECRET_KEY"] = "sk-lf-df2d8b0f-80d9-4e29-b2a0-0d793326a5db"
os.environ["LANGFUSE_HOST"] = "http://localhost:3000"


from langfuse import Langfuse
from langfuse.callback import CallbackHandler

# Initialize Langfuse client (prompt management)
langfuse = Langfuse()

# Initialize Langfuse CallbackHandler for Langchain (tracing)
langfuse_callback_handler = CallbackHandler()

# Optional, verify that Langfuse is configured correctly
assert langfuse.auth_check()
assert langfuse_callback_handler.auth_check()

class AgentSimple:

    sys_msg = SystemMessage(content="You are a helpful assistant tasked with performing arithmetic on a set of inputs.")

    def __init__(self):        
        logger.info(f"Initializing simple agent")
        self.tools = [AgentSimple.add, AgentSimple.multiply, AgentSimple.divide]

        self.llm_tools= ChatOllama(
            model="llama3.2",
            temperature=0
        ).bind_tools(self.tools)

    def doStuff(self):
        builder = StateGraph(MessagesState)
        # Define nodes: these do the work
        builder.add_node("assistant", self.assistant)
        builder.add_node("tools", ToolNode(self.tools))

        # Define edges: these determine how the control flow moves
        builder.add_edge(START, "assistant")
        builder.add_conditional_edges(
            "assistant",
            # If the latest message (result) from assistant is a tool call -> tools_condition routes to tools
            # If the latest message (result) from assistant is a not a tool call -> tools_condition routes to END
            tools_condition,
        )
        builder.add_edge("tools", "assistant")
        react_graph = builder.compile()
        messages = [HumanMessage(content="Add 3 and 4. Multiply the output by 2. Divide the output by 5")]
        messages = react_graph.invoke({"messages": messages})
        for m in messages['messages']:
            m.pretty_print()


    # Node
    def assistant(self, state: MessagesState):
        return {"messages": [ self.llm_tools.invoke([self.sys_msg] + state["messages"], 
                                                    config={"callbacks":[langfuse_callback_handler]})]}

    @staticmethod
    def multiply(a: int, b: int) -> int:
        """Multiply a and b.

            Args:
                a: first int
                b: second int
            """
        return a * b

    @staticmethod
    def add(a: int, b: int) -> int:
        """Adds a and b.

        Args:
            a: first int
            b: second int
        """
        return a + b
    
    @staticmethod
    def divide(a: int, b: int) -> float:
        """Divide a and b.

        Args:
            a: first int
            b: second int
        """
        return a / bss