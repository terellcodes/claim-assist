"""
Simple Claim Consultant Agent

Ported from notebook prototype. Keeps the core logic simple.
"""

from typing import TypedDict, Annotated, Dict, Any
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode


class AgentState(TypedDict):
    """Simple state for the claim consultant agent."""
    user_input: str
    policy_id: str
    messages: Annotated[list, add_messages]


class SimpleClaimConsultant:
    """
    Simple claim consultant agent ported from notebook.
    Evaluates insurance claims against uploaded policies.
    """
    
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o-mini")
        self.system_prompt = self._get_system_prompt()
        
        # Tools setup
        self.tavily_tool = TavilySearchResults(max_results=5)
        self.tools = [self.tavily_tool]  # RAG tool will be added dynamically
        
        # LLM with tools
        self.llm_with_tools = self.llm.bind_tools(self.tools)
        
        # Build graph
        self.agent = self._build_agent()
    
    def _get_system_prompt(self) -> str:
        """System prompt for the claim consultant (simplified from notebook)."""
        return """
You are a highly experienced Insurance Claim Consultant.

Your job is to evaluate whether a user's insurance claim is valid, based on the uploaded insurance policy. You have access to two tools:

1. **RAG Search on Insurance Policy** – Use this to search and retrieve relevant clauses from the user's uploaded policy.
2. **Web Search Tool** – Use this to research any external facts (e.g., explanations of storm mechanics, typical standards for valid claims, or definitions of insurance terminology) to help clarify or strengthen your response.

## Tool Usage Guidelines

- **Always use the RAG Search first.** Your primary responsibility is to validate the claim strictly based on the user's uploaded policy. Use this tool as often as needed to understand the policy and how it applies to the user's claim.
- **Only use the Web Search if needed**, after the RAG Search:
  - If the policy is unclear or lacks specific wording on the situation described
  - If the user mentions a complex or technical situation that may require external explanation (e.g., "derecho wind event", "burst pipe due to negative pressure")
- **Do not overuse the Web Search.** Your main objective is to help the user understand whether their claim is supported by the actual policy document.

## Agent Behavior

1. **Parse the user's claim** — Identify the scenario, cause of loss, location, date, and keywords (e.g., water damage, wind, theft).
2. **Query the Insurance Policy using the RAG Search tool** to find clauses that mention covered perils, exclusions, and conditions.
3. **Determine if the claim is valid or not.** Base your decision primarily on what the policy says.
4. If necessary, **use the Web Search tool** to clarify any uncertain facts or explain why a technical detail supports or weakens the claim.
5. **Generate a response to the user:**
   - If the claim is valid: write a professional email the user can send to their insurance company, referencing relevant clauses.
   - If the claim is not valid: explain why not, and give clear, actionable suggestions on what the user can do to strengthen or reframe the claim.

Always ground your decision in the uploaded policy first, and be concise, helpful, and accurate.
"""
    
    def _build_agent(self) -> StateGraph:
        """Build the simple agent graph."""
        def prepare_input(state):
            messages = []
            messages.append(SystemMessage(content=self.system_prompt))
            messages.append(HumanMessage(content=state["user_input"]))
            return {"messages": messages}
        
        def call_model(state):
            messages = state["messages"]
            response = self.llm_with_tools.invoke(messages)
            return {"messages": [response]}
        
        def should_continue(state):
            last_message = state["messages"][-1]
            if last_message.tool_calls:
                return "action"
            return END
        
        # Create tool node
        tool_node = ToolNode(self.tools)
        
        # Build graph
        graph = StateGraph(AgentState)
        graph.add_node("prepare_input", prepare_input)
        graph.add_node("agent", call_model)
        graph.add_node("action", tool_node)
        graph.set_entry_point("prepare_input")
        
        graph.add_conditional_edges("agent", should_continue)
        graph.add_edge("prepare_input", "agent")
        graph.add_edge("action", "agent")
        
        return graph.compile()
    
    def add_rag_tool(self, policy_id: str):
        """
        Add RAG tool for a specific policy.
        This will be called when processing a claim.
        """
        from ..rag.vector_store import vector_store_manager
        
        @tool
        def retrieve_insurance_policy(
            query: Annotated[str, "query to ask the retrieve insurance policy tool"]
        ):
            """Use Retrieval Augmented Generation to retrieve information insurance policy clauses to determine if a claim is covered"""
            policy_store = vector_store_manager.get_policy_store(policy_id)
            retriever = policy_store.as_retriever(search_kwargs={"k": 5})
            return retriever.invoke(query)
        
        # Update tools and rebuild LLM
        self.tools = [retrieve_insurance_policy, self.tavily_tool]
        self.llm_with_tools = self.llm.bind_tools(self.tools)
    
    def evaluate_claim(self, user_input: str, policy_id: str) -> Dict[str, Any]:
        """
        Evaluate a claim against a policy.
        
        Args:
            user_input: User's claim description
            policy_id: ID of the uploaded policy
            
        Returns:
            Dictionary with evaluation results
        """
        # Add RAG tool for this policy
        self.add_rag_tool(policy_id)
        
        # Run agent
        input_data = {
            "user_input": user_input,
            "policy_id": policy_id
        }
        
        result = self.agent.invoke(input_data)
        
        # Extract final response
        final_message = result["messages"][-1]
        if hasattr(final_message, 'content'):
            response_content = final_message.content
        else:
            response_content = str(final_message)
        
        return {
            "response": response_content,
            "policy_id": policy_id,
            "status": "completed"
        }


# Global instance
claim_consultant = SimpleClaimConsultant()