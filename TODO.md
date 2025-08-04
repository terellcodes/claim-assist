# TODO.md

We will be productionizing the insurance claim evaluation prototype described in the outline above. This includes both the API backend and the UI frontend. The application allows users to upload insurance policies, describe their claim, and get an AI-generated claim evaluation including a professionally written email.

From now on, "notebook" refers to the prototype logic found in the internal development notebooks used for LLM-based claim evaluation.

The notebook describes two different approaches to implement the agent. Please use the more advanced one.

---

## Task 1: UI

### A: Top Menu Bar
- Includes:
  - App Logo: ClaimAssist
  - Navigation Links:
    - API Docs
    - GitHub

### B: Main Content
- Hero Section:
  - Catchphrase: "Smart Claims, Backed by Policy"
  - Subtext: “Upload your insurance policy, describe your situation, and we’ll draft your claim – complete with matching clauses.”
- Row of 3 Feature Cards:
  - Upload and Understand Your Policy
  - AI-Powered Claim Evaluation
  - Professionally Drafted Emails
- "Try Now" Button that scrolls to the Functional UI

### C: Functional UI
- **Component 1**: Upload Insurance Policy PDF
  - On success, display extracted summary:
    - Insurance Company
    - Policy Holder Name
    - Policy Number
    - Date Issued
    - Brief Policy Summary

- **Component 2**: Input Claim Details
  - Structured Fields:
    - Name of Policy Holder
    - Date
    - Time
    - Location
  - Unstructured Field:
    - Text Area for Claim Description

- **Component 3**: Submit Claim Button

- **Component 4**: Results Panel
  - Output from Claim Consultant Agent:
    - If claim is valid: drafted email with policy references
    - If not valid: response with reasons and suggestions for improvement

---

## Task 2: API

### A: RAG Tooling
- Single vector store with namespace separation
- On policy upload:
  - Parse and chunk policy PDF
  - Load into vector store under unique namespace

### B: Endpoints
- **POST /upload_policy**
  - Accepts policy PDF
  - Parses metadata (e.g., company, policyholder, dates)
  - Chunks and stores in vector store
  - Returns policy summary

- **POST /submit_claim**
  - Accepts:
    - Structured + unstructured claim description
    - ID of uploaded policy
  - Calls Claim Consultant Agent to:
    - Validate against vector store (RAG)
    - Use reasoning to determine if claim is valid
    - Return results:
      - Email text if valid
      - Feedback if not valid

---

## Task 3: Agent Orchestration

### A: LLM Node
- Role: Expert Insurance Claims Consultant
- System Prompt Includes:
  - How to use RAG and Web tools
  - Instructions for determining claim validity
  - Logic for producing professional claim email or feedback

### B: Tools Node
- **Tool 1**: RAG on Uploaded Policy
  - Used to retrieve relevant clauses supporting or rejecting claim
- **Tool 2**: Web Search Tool using Tavily Search
  - Used only when policy lacks clarity or requires real-world definitions:
    - Legal standards for claim validity
    - Definitions or explanations (e.g., what constitutes "storm damage")

### C: Agent Flow
- Use LangGraph to wire:
  - LLM node for reasoning + decision making
  - Tool node for execution
  - Memory to manage policy namespace and user session