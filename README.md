# 🧠 Spot2 Challenge – Conversational Real Estate Assistant

This project is a technical challenge solution for Spot2.  
It implements a conversational AI system using an LLM to gather structured real estate information from users naturally and interactively.

---

## 🚀 Key Features

- Conversational flow powered by OpenAI GPT-3.5.
- Automatic extraction of required fields:
  - `budget`
  - `total_size_requirement`
  - `real_estate_type`
  - `city`
- Support for additional, user-provided fields.
- Session memory implemented via `fakeredis`.
- Full conversation history storage per session.
- Prompt injection prevention through strict role separation (system/user).
- Built with FastAPI for async, modern API handling.
- Fully tested with unit and integration tests.
- CI/CD pipeline configured with GitHub Actions.
- Docker-ready for production deployment.

---

## 📦 Local Setup

1. Clone the repository:

```bash
git clone https://github.com/pjvargas/spot2-challenge.git
```

2. Install dependencies using Poetry:

```bash
poetry install
```

3. Create a `.env` file with your OpenAI API key:

```env
OPENAI_API_KEY=sk-...
API_URL=http://localhost:8000  # (Optional, only needed to run the Streamlit frontend locally)
```

4. Start the server locally:

```bash
poetry run uvicorn spot2_challenge.main:app --reload --app-dir src
```

Access the interactive API documentation at:

```
http://localhost:8000/docs
```

---

## 🎨 Optional – Streamlit Frontend

A simple frontend was built using Streamlit for a more user-friendly interaction.

To run the Streamlit app locally:

```bash
poetry run streamlit run src/streamlit/app.py
```

The Streamlit app communicates with the FastAPI backend.

Access the frontend at:

```
http://localhost:8501
```

**Note:** Streamlit is not deployed to production; it is intended for local testing and visualization purposes only.

## 🐳 Run with Docker

1. Build the image:

```bash
docker build -t spot2-challenge .
```

2. Run the container:

```bash
docker run -p 8000:8000 -e OPENAI_API_KEY=sk-... spot2-challenge
```

Access the API documentation at:

```
http://localhost:8000/docs
```

**Note:**
Environment Variables like OPENAI_API_KEY must be provided at runtime.
In cloud platforms (e.g., Render, Railway), you should configure these Environment Variables in the dashboard.

---

## 🧪 Testing

To run all tests:

```bash
poetry run pytest
```

Test coverage includes:

- LLM logic with mocked OpenAI responses.
- Session and memory management.
- API endpoint integration.

---

## 🔐 Security Considerations

- Strict separation of system/user roles when interacting with the LLM to prevent prompt injection.
- No user input is directly interpolated into system-level prompts.
- All inputs are treated as conversational content only.

---

## ⚙️ Scalability and Architecture

- Stateless FastAPI server with in-memory session simulation via `fakeredis`.
- Easily replaceable with real Redis for production-grade scaling.
- Modular architecture separating concerns between session management, conversation logic, and API handling.
- Designed for easy horizontal scaling with multiple workers.

---

## ⚡ Continuous Integration

- GitHub Actions pipeline triggers on every `push` and `pull_request` to `main` branch.
- Automatically installs dependencies, runs all tests, ensures code integrity, and generates a Docker image.

---

## 🌐 Deployment

- Backend deployed at: `https://spot2-challenge.onrender.com`
- API Documentation live at: `https://spot2-challenge.onrender.com/docs`

---

## 👤 Author

Developed by Juan Vargas  
juan.vargasg2@gmail.com

---
