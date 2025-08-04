"""
Simple Claim Consultant Agent

Ported from notebook prototype. Keeps the core logic simple.
"""

from typing import TypedDict, Annotated, Dict, Any
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
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
        
        # Tools setup - make Tavily optional
        self.tools = []
        try:
            self.tavily_tool = TavilySearch(max_results=5)
            self.tools.append(self.tavily_tool)
        except Exception:
            # Tavily API key not available - continue without web search
            self.tavily_tool = None
        
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
5. **Return your response in JSON format with these exact fields:**

```json
{
  "is_valid": true/false,
  "evaluation": "Detailed explanation of your analysis and reasoning",
  "citations": "List of citations from the policy that support your analysis",
  "email_draft": "Professional email to send to insurance company (only if is_valid is true)",
  "suggestions": "Actionable suggestions for the user (especially if is_valid is false)"
}
```

**IMPORTANT**: You must ALWAYS return a valid JSON response with these exact field names. 
- Set "is_valid" to true only if you are confident the claim should be covered based on the policy
- Set "is_valid" to false if the claim is excluded, not covered, or you have significant doubts
- Always provide a detailed "evaluation" explaining your reasoning
- Only include "email_draft" if is_valid is true
- Always provide helpful "suggestions" for the user

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
        from services.rag.vector_store import get_vector_store_manager
        
        @tool
        def retrieve_insurance_policy(
            query: Annotated[str, "query to ask the retrieve insurance policy tool"]
        ):
            """Use Retrieval Augmented Generation to retrieve information insurance policy clauses to determine if a claim is covered"""
            vector_store_manager = get_vector_store_manager()
            policy_store = vector_store_manager.get_policy_store(policy_id)
            retriever = policy_store.as_retriever(search_kwargs={"k": 5})
            return retriever.invoke(query)
        
        # Update tools and rebuild LLM
        self.tools = [retrieve_insurance_policy]
        if self.tavily_tool:
            self.tools.append(self.tavily_tool)
        self.llm_with_tools = self.llm.bind_tools(self.tools)
        
        # Rebuild the agent graph with the new tools
        self.agent = self._build_agent()
    
    def evaluate_claim(self, user_input: str, policy_id: str) -> Dict[str, Any]:
        """
        Evaluate a claim against a policy.
        
        Args:
            user_input: User's claim description
            policy_id: ID of the uploaded policy
            
        Returns:
            Dictionary with structured evaluation results
        """
        import json
        
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
        
        # Parse JSON response from LLM
        try:
            # Clean up the response (remove markdown code blocks if present)
            cleaned_response = response_content.strip()
            if cleaned_response.startswith('```json'):
                cleaned_response = cleaned_response[7:]
            if cleaned_response.endswith('```'):
                cleaned_response = cleaned_response[:-3]
            cleaned_response = cleaned_response.strip()
            
            # Parse JSON
            parsed_response = json.loads(cleaned_response)
            
            # Validate required fields
            if not isinstance(parsed_response.get('is_valid'), bool):
                raise ValueError("is_valid field must be a boolean")
            
            return {
                "is_valid": parsed_response["is_valid"],
                "evaluation": parsed_response.get("evaluation", ""),
                "citations": parsed_response.get("citations"),
                "email_draft": parsed_response.get("email_draft"),
                "suggestions": parsed_response.get("suggestions"),
                "policy_id": policy_id,
                "status": "completed"
            }
            
        except (json.JSONDecodeError, ValueError, KeyError) as e:
            # Fallback: if JSON parsing fails, treat as unstructured response
            return {
                "is_valid": False,  # Default to invalid if we can't parse
                "evaluation": f"Error parsing agent response: {str(e)}\n\nRaw response: {response_content}",
                "email_draft": None,
                "suggestions": "Please try submitting your claim again.",
                "policy_id": policy_id,
                "status": "error"
            }


# Global instance - lazy initialization to avoid API key issues at import time
_claim_consultant = None


def get_claim_consultant() -> SimpleClaimConsultant:
    """Get the global claim consultant instance (lazy initialization)."""
    global _claim_consultant
    if _claim_consultant is None:
        _claim_consultant = SimpleClaimConsultant()
    return _claim_consultant