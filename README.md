**AI App Builder**

AI App Builder is a small FastAPI-based project that demonstrates an LLM-driven pipeline for intent processing, validation, and simple dashboard/analytics endpoints. It's designed as a clear, interview-ready sample showing integration with an LLM client, pipeline modules, and an API surface suitable for demos and evaluations.

**Why This Project**
- **Focus:** Shows LLM integration, prompt handling, and validation pipeline.
- **Complete Stack:** API server, pipeline modules, and utility LLM client.
- **Interview-Ready:** Clear setup, runnable locally, and testable endpoints.

**Quick Start**
- Install dependencies:

```bash
python -m pip install -r requirements.txt
```

- Set environment variables (example `.env`):

```
GROQ_API_KEY=your_groq_api_key_here
```

- Run the app locally (use no space around the colon):

```bash
uvicorn main:app --reload
```

**API Endpoints**
- **GET /contacts:** Get all contacts
- **POST /contacts:** Create a new contact
- **GET /dashboard:** Get dashboard data
- **POST /payments:** Create a new payment
- **GET /analytics:** Get analytics data

**Key Files**
- `main.py` - FastAPI application and route definitions
- `pipeline/intent.py` - Intent processing pipeline
- `pipeline/repair.py` - Repair helpers for prompt outputs
- `pipeline/schema.py` - Schema utilities
- `pipeline/validator.py` - Validation logic
- `utils/llm_client.py` - LLM client wrapper (Groq integration)
- `models/schema_models.py` - Data models

**Notes & Tips**
- When launching with `uvicorn`, use `main:app` (no spaces) to avoid the "unexpected extra argument" error.
- If prompts sometimes don't appear, check logs and ensure `utils/llm_client.py` responses are valid JSON (the client strips fences and comments). The project enforces strict JSON responses from the model.

**Contributing / Selection Tips**
- Showcase your understanding by explaining how the pipeline validates and repairs LLM outputs.
- Run the server and exercise the `/dashboard` and `/analytics` endpoints to demonstrate data flow.

**License**
- MIT
