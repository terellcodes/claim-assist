# ClaimMate 🏥📋

> **AI-Powered Insurance Claim Evaluation & Professional Email Drafting**

ClaimMate is an intelligent insurance claim processing application that combines AI-powered policy analysis with professional claim drafting. Upload your insurance policy, describe your claim situation, and receive an expert evaluation with a professionally drafted email ready to send to your insurance company.

## 🚀 Features

- **📄 Smart Policy Upload**: Upload and parse insurance policy PDFs with automatic metadata extraction
- **🤖 AI-Powered Evaluation**: Advanced claim analysis using RAG (Retrieval Augmented Generation) and web search
- **✍️ Professional Email Drafting**: Automatically generate professional claim emails with policy citations
- **📊 Detailed Analysis**: Comprehensive evaluation with supporting citations and actionable suggestions
- **🔄 Interactive Workflow**: Step-by-step guided process from upload to final evaluation
- **🎯 Accuracy-Focused**: Grounds decisions in actual policy text with external fact verification

## 🏗️ Technical Architecture

### System Overview

ClaimMate follows a modern microservices architecture with AI agent orchestration:

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Next.js       │    │   FastAPI        │    │   AI Services   │
│   Frontend      │◄──►│   Backend        │◄──►│   & Vector DB   │
│                 │    │                  │    │                 │
│ • React 19      │    │ • LangChain      │    │ • OpenAI GPT    │
│ • TypeScript    │    │ • LangGraph      │    │ • Qdrant VectorDB│
│ • Tailwind CSS │    │ • Pydantic       │    │ • Tavily Search │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### Detailed Architecture

The architecture diagram shows the complete data flow from frontend user interactions through AI processing and back to the user:

### Core Components

#### 🎨 Frontend Layer (Next.js 15)
- **React 19** with TypeScript for type safety
- **Tailwind CSS** for responsive, modern UI
- **Component Architecture**: Modular components for each workflow step
- **State Management**: React hooks for local state and API integration

#### 🚀 API Layer (FastAPI)
- **FastAPI** with automatic OpenAPI documentation
- **Pydantic** for request/response validation
- **CORS middleware** for cross-origin requests
- **Mangum adapter** for Vercel serverless deployment

#### 🧠 AI Agent Layer (LangGraph)
- **LangGraph orchestration** for multi-step AI workflows
- **GPT-4o-mini** as the primary reasoning engine
- **RAG Tool**: Retrieves relevant policy clauses from vector database
- **Web Search Tool**: Tavily API for external fact-checking and definitions

#### 💾 Data Layer
- **Qdrant Vector Database** for semantic policy document search
- **PDF Processing** with PyMuPDF4LLM for document parsing and chunking
- **Namespace separation** for multi-tenant policy storage

## 📁 Project Structure

```
claim-mate/
├── 🎨 frontend/                    # Next.js React application
│   ├── src/
│   │   ├── app/                    # App Router pages
│   │   │   ├── layout.tsx          # Root layout
│   │   │   └── page.tsx            # Home page
│   │   ├── components/             # React components
│   │   │   ├── ClaimWiseApp.tsx    # Main application component
│   │   │   ├── PolicyUpload.tsx    # PDF upload & processing
│   │   │   ├── ClaimForm.tsx       # Claim details form
│   │   │   └── EvaluationResults.tsx # Results display
│   │   └── config/
│   │       └── api.ts              # API configuration
│   ├── package.json                # Dependencies & scripts
│   └── tailwind.config.js          # Tailwind CSS config
│
├── 🚀 api/                         # FastAPI backend
│   ├── config/
│   │   └── settings.py             # Environment & app settings
│   ├── models/
│   │   ├── domain/                 # Domain models
│   │   ├── schemas/                # Pydantic schemas
│   │   │   ├── claim.py            # Claim request/response models
│   │   │   └── policy.py           # Policy models
│   │   └── database/               # Database models (future)
│   ├── services/
│   │   ├── agents/
│   │   │   └── claim_consultant.py # LangGraph AI agent
│   │   ├── rag/
│   │   │   ├── document_processor.py # PDF processing
│   │   │   └── vector_store.py     # Vector database management
│   │   ├── claim_service.py        # Claim processing logic
│   │   └── policy_service.py       # Policy management logic
│   ├── routes/
│   │   ├── claims.py               # Claim API endpoints
│   │   ├── policies.py             # Policy API endpoints
│   │   └── health.py               # Health check endpoints
│   ├── utils/
│   │   └── constants.py            # Application constants
│   ├── tests/                      # Test suite
│   │   ├── unit/                   # Unit tests
│   │   ├── integration/            # Integration tests
│   │   └── fixtures/               # Test fixtures
│   ├── main.py                     # FastAPI application entry
│   ├── pyproject.toml              # Dependencies & project config
│   └── requirements.txt            # Legacy requirements
│
├── 📓 notebooks/                   # Research & prototyping
│   ├── data/                       # Sample insurance policies
│   └── prototype.ipynb             # Original prototype logic
│
├── 📄 Documentation
│   ├── README.md                   # This file
│   ├── CHANGELOG.md                # Version history
│   ├── TODO.md                     # Development roadmap
│   └── CLAUDE.md                   # AI assistant guidance
│
└── ⚙️ Configuration
    ├── vercel.json                 # Vercel deployment config
    └── .gitignore                  # Git ignore patterns
```

## 🚀 Quick Start

### Prerequisites

- **Node.js** 18+ and npm/yarn
- **Python** 3.11-3.13
- **UV** package manager (recommended) or pip
- **OpenAI API Key** for GPT models
- **Tavily API Key** for web search (optional)

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/claim-mate.git
cd claim-mate
```

### 2. Backend Setup (FastAPI)

```bash
# Navigate to API directory
cd api

# Install dependencies with UV (recommended)
uv sync

# OR with pip
pip install -r requirements.txt

# Create environment file
cp .env.example .env

# Edit .env with your API keys
# Required:
OPENAI_API_KEY=your_openai_api_key_here

# Optional but recommended:
TAVILY_API_KEY=your_tavily_api_key_here
LANGCHAIN_TRACING_V2=true
LANGSMITH_API_KEY=your_langsmith_api_key_here

# Start the development server
uv run uvicorn main:app --reload
# OR with pip
uvicorn main:app --reload
```

API will be available at `http://localhost:8000`
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### 3. Frontend Setup (Next.js)

```bash
# Navigate to frontend directory (in new terminal)
cd frontend

# Install dependencies
npm install
# OR
yarn install

# Start development server
npm run dev
# OR
yarn dev
```

Frontend will be available at `http://localhost:3000`

### 4. Test the Application

1. **Upload a Policy**: Go to `http://localhost:3000` and upload a PDF insurance policy
2. **Describe Your Claim**: Fill out the claim form with incident details
3. **Get AI Evaluation**: Receive professional analysis and email draft

## 🔧 Development

### Code Quality Tools

The project includes comprehensive development tools:

```bash
# Backend (in api/ directory)
uv run black .              # Code formatting
uv run isort .              # Import sorting
uv run flake8 .             # Linting
uv run mypy .               # Type checking
uv run pytest              # Run tests
uv run pytest --cov=app    # Test coverage

# Frontend (in frontend/ directory)
npm run lint                # ESLint
npm run build               # Production build
```

### Environment Variables

#### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key for GPT models | `sk-...` |

#### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `TAVILY_API_KEY` | Tavily search API key | None |
| `LANGCHAIN_TRACING_V2` | Enable LangSmith tracing | `false` |
| `LANGSMITH_API_KEY` | LangSmith API key | None |
| `ENVIRONMENT` | Deployment environment | `development` |
| `DEBUG` | Debug mode | `true` |

### API Endpoints

#### Policy Management
- `POST /api/policies/upload` - Upload and process insurance policy PDF
- `GET /api/policies/{policy_id}` - Get policy metadata and summary

#### Claim Processing  
- `POST /api/claims/submit` - Submit claim for AI evaluation
- `GET /api/claims/{claim_id}` - Get claim evaluation status

#### System Health
- `GET /api/health` - System health check
- `GET /api/info` - API information and version

## 🤖 AI Agent Architecture

### Claim Consultant Agent

The core AI system uses **LangGraph** to orchestrate a sophisticated claim evaluation workflow:

#### Agent Flow
1. **Input Processing**: Parse structured claim data and unstructured description
2. **Policy Retrieval**: Use RAG to find relevant policy clauses
3. **External Research**: Web search for clarifications when needed
4. **Decision Making**: GPT-4o-mini evaluates claim validity
5. **Response Generation**: Create professional email or detailed feedback

#### Tools Available
- **RAG Tool**: Semantic search through uploaded policy documents
- **Web Search Tool**: Tavily API for external fact-checking and definitions
- **Memory Management**: Maintains context throughout evaluation process

#### System Prompt Strategy
The agent is prompted as an expert insurance claims consultant with:
- Deep knowledge of insurance policies and claim procedures
- Ability to interpret complex policy language
- Professional communication skills for email drafting
- Conservative approach - only approves clearly valid claims

### Vector Database (Qdrant)

- **Document Chunking**: Policies are split into semantically meaningful chunks
- **Namespace Separation**: Each policy gets a unique namespace for isolation
- **Semantic Search**: Uses OpenAI embeddings for accurate clause retrieval
- **Metadata Storage**: Preserves document structure and source references

## 🚀 Deployment

### Vercel Deployment (Recommended)

Both frontend and backend are configured for Vercel deployment:

#### Backend (API)
```bash
# Deploy from api/ directory
vercel --prod
```

#### Frontend
```bash  
# Deploy from frontend/ directory
vercel --prod
```

#### Environment Variables in Vercel
Set these in your Vercel project settings:

**Production:**
```
OPENAI_API_KEY=your_key_here
TAVILY_API_KEY=your_key_here
ENVIRONMENT=production
DEBUG=false
ALLOWED_ORIGINS=https://your-domain.vercel.app
```

### Alternative Deployment Options

#### Docker (Backend)
```bash
cd api
docker build -t claim-mate-api .
docker run -p 8000:8000 claim-mate-api
```

#### Self-Hosted
- **Backend**: Any server supporting Python 3.11+ with FastAPI
- **Frontend**: Static hosting (Netlify, GitHub Pages, etc.)
- **Database**: Self-hosted Qdrant or Qdrant Cloud

## 📊 Monitoring & Observability

### LangSmith Integration
Track AI agent performance and debugging:
- **Trace Collection**: Complete agent execution traces
- **Performance Monitoring**: Token usage and latency metrics  
- **Debug Insights**: Step-by-step agent decision logging

### Health Monitoring
- **API Health Checks**: `/api/health` endpoint
- **Component Status**: Individual service health verification
- **Error Tracking**: Comprehensive error logging and reporting

## 🔒 Security & Privacy

- **Data Isolation**: Each policy stored in separate vector database namespace
- **API Key Security**: Environment-based configuration
- **Input Validation**: Pydantic schemas for all API requests
- **CORS Protection**: Configurable origin restrictions
- **No Data Persistence**: Policies processed in-memory (configurable)

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** following the code style guidelines
4. **Run tests**: `pytest` and `npm test`
5. **Commit changes**: `git commit -m 'Add amazing feature'`
6. **Push to branch**: `git push origin feature/amazing-feature`
7. **Open a Pull Request**

### Development Guidelines

- **Code Style**: Black formatting, isort imports, flake8 linting
- **Type Safety**: Full MyPy type checking
- **Testing**: Comprehensive test coverage with pytest
- **Documentation**: Update README and docstrings for new features
- **Commit Messages**: Clear, descriptive commit messages

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **LangChain/LangGraph** - AI agent orchestration framework
- **FastAPI** - High-performance Python web framework  
- **Next.js** - Modern React framework
- **OpenAI** - GPT language models
- **Qdrant** - Vector similarity search engine
- **Tavily** - Web search API for AI applications

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/your-username/claim-mate/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-username/claim-mate/discussions)
- **Documentation**: Check the `/docs` folder and inline code documentation

---

**⚠️ Important Notice**: ClaimMate provides AI-assisted claim analysis for informational purposes only. Always consult with insurance professionals and carefully review your policy terms before submitting actual claims. 