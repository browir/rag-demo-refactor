# RAG Demo – Refactored Version

This repository contains a refactored version of a simple Retrieval-Augmented Generation (RAG) demo application.  
The purpose of this project is to demonstrate clean code structure, separation of concerns, and basic object-oriented design principles in a realistic backend scenario.

The external behavior of the application remains the same as the original implementation, while the internal design has been improved for readability, maintainability, and testability.

## Project Structure

```text
.
├── app/
│   ├── __init__.py
│   ├── main.py          # Application entrypoint and dependency wiring
│   ├── api.py           # FastAPI routes (HTTP layer)
│   ├── workflow.py      # RAG business logic
│   ├── embeddings.py    # Embedding service
│   ├── storage.py       # Document storage abstractions and implementations
│   └── models.py        # Request schemas
├── notes.md             # Design decisions and trade-offs
└── README.md
```

# Requirements

- Python 3.9+
- (Optional) Qdrant running locally at `http://localhost:6333`

If Qdrant is not available, the application will automatically fall back to an in-memory document store.


# How to Run the Application

1. Clone the repository:
`
git clone https://github.com/browir/rag-demo-refactor.git`
`cd rag-demo-refactor`

2. Install Dependencies:
` pip install fastapi uvicorn qdrant-client langgraph `

3. Run the application:
`uvicorn app.main:app --reload`

4. Open Swagger UI in your browser:
` http://127.0.0.1:8000/docs `

# Notes
Please refer to `notes.md` for a short explanation of:
1. Main design decisions
2. Trade-off considered
3. How the refactor improves maintainability


