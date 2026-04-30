# 🚀 AI APP COMPILER

An AI-powered system that converts natural language into a **structured, validated application schema** using a multi-stage pipeline.

This project behaves like a **compiler for software generation**:

**Prompt → Intent → Architecture → Schema → Validation → Repair → JSON Output**

---

##  Objective

Build a reliable system that transforms open-ended user instructions into a **complete, consistent, and usable application configuration**, including:

* UI schema
* API schema
* Database schema
* Authentication system

---

## System Architecture

The system follows a **multi-stage pipeline**:

1. **Intent Extraction**

   * Parses user input into structured intent

2. **Schema Generation**

   * Generates:

     * UI structure
     * API endpoints
     * Database schema
     * Auth + roles
     

3. **Validation**

   * Ensures:

     * Valid JSON
     * Required fields present
     * Type correctness

4. **Repair Engine**

   * Fixes:

     * Missing fields
     * Schema inconsistencies
     * Logical errors

---

## ⚙️ Tech Stack

* **Backend:** FastAPI
* **LLM:** Groq (Llama 3 models)
* **Language:** Python
* **Frontend:** Simple HTML + JS dashboard

---

## 🌐 Live Demo

👉 https://ai-app-compiler-xte4.onrender.com/

---

##  Installation

```bash
git clone https://github.com/your-username/ai-app-compiler.git
cd ai-app-compiler
pip install -r requirements.txt
```

---

##  Environment Setup

Create a `.env` file:

```env
GROQ_API_KEY=your_api_key_here
MODEL_NAME=llama3-70b-8192
```

---

## ▶️ Run Locally

```bash
uvicorn main:app --reload
```

Open:

```
http://127.0.0.1:8000
```

---

##  Example Prompt

```
Build a SaaS project management tool with login, roles, dashboard, task board, and subscription plans.
```

---

##  Example Output

```json
{
  "ui_schema": {...},
  "api_schema": {...},
  "db_schema": {...},
  "auth_schema": {...}
 }
```

---

