"""
Simple Claim Consultant Agent

Ported from notebook prototype. Keeps the core logic simple.
"""

from typing import TypedDict, Annotated, Dict, Any, Optional
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
    
    Supports multiple retrieval strategies:
    - basic: Simple k=5 vector search
    - advanced_flashrank: k=20 with FlashRank reranking to top 5
    - advanced_cohere: k=20 with Cohere reranking to top 5
    """
    
    # Supported retrieval strategies
    RETRIEVAL_STRATEGIES = {
        "basic": {
            "initial_k": 5,
            "final_k": 5,
            "reranker": None,
            "description": "Fast and efficient for most claims"
        },
        "advanced_flashrank": {
            "initial_k": 20,
            "final_k": 5,
            "reranker": "flashrank",
            "description": "More accurate context selection using AI reranking"
        },
        "advanced_cohere": {
            "initial_k": 20,
            "final_k": 5,
            "reranker": "cohere",
            "description": "Premium accuracy with Cohere reranking (requires API key)"
        }
    }
    
    def __init__(self, retrieval_strategy: str = "basic"):
        """
        Initialize the claim consultant agent.
        
        Args:
            retrieval_strategy: Strategy for document retrieval
                - "basic": Simple k=5 vector search (default)
                - "advanced_flashrank": k=20 with FlashRank reranking (offline)
                - "advanced_cohere": k=20 with Cohere reranking (requires API key)
        """
        if retrieval_strategy not in self.RETRIEVAL_STRATEGIES:
            raise ValueError(f"Invalid retrieval strategy: {retrieval_strategy}. "
                           f"Must be one of: {list(self.RETRIEVAL_STRATEGIES.keys())}")
        
        self.retrieval_strategy = retrieval_strategy
        strategy_info = self.RETRIEVAL_STRATEGIES[retrieval_strategy]
        
        print(f"📊 Initializing ClaimConsultant with '{retrieval_strategy}' strategy")
        print(f"   📋 {strategy_info['description']}")
        print(f"   🔍 Retrieval: k={strategy_info['initial_k']} → {strategy_info['final_k']} (reranker: {strategy_info['reranker'] or 'none'})")
        
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
        strategy_info = self.RETRIEVAL_STRATEGIES[self.retrieval_strategy]
        return f"""
You are a highly experienced Insurance Claim Consultant using the {self.retrieval_strategy} retrieval strategy ({strategy_info['description']}).

Your job is to evaluate whether a user's insurance claim is valid, based on the uploaded insurance policy. You have access to two tools:

1. **RAG Search on Insurance Policy** – Use this to search and retrieve relevant clauses from the user's uploaded policy. This uses {strategy_info['description'].lower()} for finding the most relevant policy sections.
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
    
    def _create_basic_retriever(self, policy_id: str):
        """Create basic k=5 retriever."""
        print(f"🔍 Creating basic retriever for policy {policy_id[:8]}... (k=5)")
        from services.rag.vector_store import get_vector_store_manager
        
        vector_store_manager = get_vector_store_manager()
        policy_store = vector_store_manager.get_policy_store(policy_id)
        retriever = policy_store.as_retriever(search_kwargs={"k": 5})
        print(f"✅ Basic retriever created successfully")
        return retriever
    
    def _create_advanced_flashrank_retriever(self, policy_id: str):
        """Create advanced retriever with FlashRank reranking."""
        print(f"🎯 Creating FlashRank retriever for policy {policy_id[:8]}... (k=20 → rerank → top 5)")
        from services.rag.vector_store import get_vector_store_manager
        from langchain.retrievers.contextual_compression import ContextualCompressionRetriever
        from langchain.retrievers.document_compressors import FlashrankRerank
        
        try:
            # Get base retriever with k=20
            vector_store_manager = get_vector_store_manager()
            policy_store = vector_store_manager.get_policy_store(policy_id)
            base_retriever = policy_store.as_retriever(search_kwargs={"k": 20})
            print(f"   📝 Base retriever created (k=20)")
            
            # Create FlashRank compressor (offline, no API key needed)
            compressor = FlashrankRerank()
            print(f"   🔧 FlashRank compressor initialized (offline)")
            
            # Create compression retriever
            compression_retriever = ContextualCompressionRetriever(
                base_compressor=compressor,
                base_retriever=base_retriever
            )
            print(f"✅ FlashRank retriever created successfully")
            return compression_retriever
            
        except Exception as e:
            print(f"❌ Failed to create FlashRank retriever: {str(e)}")
            print(f"   🔄 Falling back to basic retriever")
            return self._create_basic_retriever(policy_id)
    
    def _create_advanced_cohere_retriever(self, policy_id: str):
        """Create advanced retriever with Cohere reranking."""
        print(f"⭐ Creating Cohere retriever for policy {policy_id[:8]}... (k=20 → rerank → top 5)")
        from services.rag.vector_store import get_vector_store_manager
        from langchain.retrievers.contextual_compression import ContextualCompressionRetriever
        
        try:
            from langchain_cohere import CohereRerank
            print(f"   📦 Cohere package imported successfully")
        except ImportError:
            print(f"❌ CohereRerank not available. Install with: pip install langchain-cohere")
            print(f"   🔄 Falling back to FlashRank retriever")
            return self._create_advanced_flashrank_retriever(policy_id)
        
        try:
            # Get base retriever with k=20
            vector_store_manager = get_vector_store_manager()
            policy_store = vector_store_manager.get_policy_store(policy_id)
            base_retriever = policy_store.as_retriever(search_kwargs={"k": 20})
            print(f"   📝 Base retriever created (k=20)")
            
            # Create Cohere compressor (requires API key)
            compressor = CohereRerank(model="rerank-v3.5")
            print(f"   🔧 Cohere compressor initialized (model: rerank-v3.5)")
            
            # Create compression retriever
            compression_retriever = ContextualCompressionRetriever(
                base_compressor=compressor,
                base_retriever=base_retriever,
                search_kwargs={"k": 5}
            )
            print(f"✅ Cohere retriever created successfully")
            return compression_retriever
            
        except Exception as e:
            print(f"❌ Failed to create Cohere retriever: {str(e)}")
            print(f"   🔄 Falling back to FlashRank retriever")
            return self._create_advanced_flashrank_retriever(policy_id)
    
    def add_rag_tool(self, policy_id: str, strategy: Optional[str] = None):
        """
        Add RAG tool for a specific policy using the specified retrieval strategy.
        
        Args:
            policy_id: ID of the policy to create retriever for
            strategy: Override the instance strategy for this specific policy
                     If None, uses self.retrieval_strategy
        """
        # Use provided strategy or fall back to instance strategy
        strategy = strategy or self.retrieval_strategy
        
        print(f"🔧 Adding RAG tool for policy {policy_id[:8]}... using '{strategy}' strategy")
        
        if strategy not in self.RETRIEVAL_STRATEGIES:
            raise ValueError(f"Invalid strategy: {strategy}. "
                           f"Must be one of: {list(self.RETRIEVAL_STRATEGIES.keys())}")
        
        # Create appropriate retriever based on strategy
        if strategy == "basic":
            retriever = self._create_basic_retriever(policy_id)
        elif strategy == "advanced_flashrank":
            retriever = self._create_advanced_flashrank_retriever(policy_id)
        elif strategy == "advanced_cohere":
            retriever = self._create_advanced_cohere_retriever(policy_id)
        else:
            raise ValueError(f"Strategy {strategy} not implemented")
        
        @tool
        def retrieve_insurance_policy(
            query: Annotated[str, "query to ask the retrieve insurance policy tool"]
        ):
            """Use Retrieval Augmented Generation to retrieve information insurance policy clauses to determine if a claim is covered"""
            print(f"🔍 RAG tool invoked with query: {query[:100]}{'...' if len(query) > 100 else ''}")
            result = retriever.invoke(query)
            print(f"   📄 Retrieved {len(result)} documents")
            return result
        
        # Update tools and rebuild LLM
        self.tools = [retrieve_insurance_policy]
        if self.tavily_tool:
            self.tools.append(self.tavily_tool)
        self.llm_with_tools = self.llm.bind_tools(self.tools)
        print(f"   🛠️  Tools updated: RAG + {'Tavily' if self.tavily_tool else 'no web search'}")
        
        # Rebuild the agent graph with the new tools
        self.agent = self._build_agent()
        print(f"✅ RAG tool added successfully with '{strategy}' strategy")
    
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