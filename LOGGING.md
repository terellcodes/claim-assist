# Retrieval Strategy Logging Guide

This document outlines the comprehensive logging system added to track the retrieval strategy flow in ClaimAssist.

## Backend Logging

### 1. Agent Initialization
```
📊 Initializing ClaimConsultant with 'advanced_flashrank' strategy
   📋 More accurate context selection using AI reranking
   🔍 Retrieval: k=20 → 5 (reranker: flashrank)
```

### 2. Retriever Creation

#### Basic Strategy
```
🔍 Creating basic retriever for policy 12345678... (k=5)
✅ Basic retriever created successfully
```

#### FlashRank Strategy
```
🎯 Creating FlashRank retriever for policy 12345678... (k=20 → rerank → top 5)
   📝 Base retriever created (k=20)
   🔧 FlashRank compressor initialized (offline)
✅ FlashRank retriever created successfully
```

#### Cohere Strategy (with fallback)
```
⭐ Creating Cohere retriever for policy 12345678... (k=20 → rerank → top 5)
   📦 Cohere package imported successfully
   📝 Base retriever created (k=20)
   🔧 Cohere compressor initialized (model: rerank-v3.5)
✅ Cohere retriever created successfully
```

### 3. Service Layer
```
📥 ClaimService: Received claim submission
   🏷️  Policy ID: 12345678...
   📊 Strategy: advanced_flashrank
   📝 Description length: 245 chars

🤖 ClaimService: Getting agent for 'advanced_flashrank' strategy
   🆕 Creating new agent instance for advanced strategy

🔍 Starting claim evaluation with advanced_flashrank strategy...
✅ Claim evaluation completed successfully
```

### 4. RAG Tool Usage
```
🔧 Adding RAG tool for policy 12345678... using 'advanced_flashrank' strategy
   🛠️  Tools updated: RAG + Tavily
✅ RAG tool added successfully with 'advanced_flashrank' strategy

🔍 RAG tool invoked with query: My roof was damaged during a storm last month...
   📄 Retrieved 5 documents
```

## Frontend Logging (Development Mode Only)

### 1. Strategy Selection
```javascript
🎯 Strategy changed: basic → advanced_flashrank
   📊 New strategy: More accurate context selection using AI reranking
```

### 2. Form Submission
```javascript
ℹ️ Submitting claim for evaluation {policy_holder_name: "John Doe", ...}
📊 Using retrieval strategy: advanced_flashrank
```

### 3. API Response
```javascript
✅ Claim evaluated successfully {claim_status: "valid", ...}
✅ Evaluation completed using 'advanced_flashrank' strategy
📊 Result: valid - Your claim appears to be covered under Section 4...
```

## Visual Indicators

### 1. Strategy Selector Component
- Icons: ⚡ (Basic), 🎯 (FlashRank), ⭐ (Cohere)
- Performance indicators with speed/accuracy bars
- Expandable details with descriptions

### 2. Results Display
Shows which strategy was used:
```
🎯 Analyzed using Advanced AI Reranking strategy
```

## Error Handling & Fallbacks

### FlashRank Fallback
```
❌ Failed to create FlashRank retriever: Module not found
   🔄 Falling back to basic retriever
```

### Cohere Fallback
```
❌ CohereRerank not available. Install with: pip install langchain-cohere
   🔄 Falling back to FlashRank retriever
```

## Benefits for Debugging

1. **Strategy Verification**: Confirm which strategy is actually being used
2. **Performance Monitoring**: Track retrieval times and document counts
3. **Error Tracking**: Clear fallback chains when advanced strategies fail
4. **User Experience**: Visual feedback on strategy selection and usage
5. **Development**: Detailed console logs for debugging API flows

## Log Levels

- **Production**: Only critical errors and status updates
- **Development**: Full detailed logging including query contents and performance metrics

This logging system provides complete visibility into the retrieval strategy flow, making it easy to debug issues and monitor performance across different strategies.