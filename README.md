# 💰 AI Expense Tracker (FastAPI + Streamlit + Ollama)

A simple yet powerful **AI-powered Expense Tracker** built with **FastAPI (Backend)**, **Streamlit (Frontend)**, and **Ollama (Local LLM)**.  
The system tracks expenses, visualizes insights through interactive charts, and uses an LLM to analyze spending patterns.

---

## 🚀 Overview

This project demonstrates a **modular AI microservice** setup:
- **Backend (FastAPI)** → Handles data storage, processing, and AI calls.  
- **Frontend (Streamlit)** → User interface with real-time expense input and visualization.  
- **Ollama LLM** → Local inference for expense insights and natural language analytics.

---

## 🧠 Architecture Sketch

```text
User → Streamlit UI (input + visualization)
          ↓
FastAPI Backend (receives expense data)
          ↓
Ollama (local LLM for insights)
          ↓
Response → Streamlit (shows charts + analysis)

```

## 📊 Key Features

✅ Add and view expenses \
✅ Interactive Pie Chart (Plotly) visualization \
✅ Real-time summary stats \
✅ Local AI insight generation (Ollama) \
✅ Modular architecture (Frontend ↔ Backend \ separation)

## Tech Stack

| Layer                   | Tech                                      |
| ----------------------- | ----------------------------------------- |
| **Frontend**            | Streamlit                                 |
| **Backend**             | FastAPI                                   |
| **AI Engine**           | Ollama (local LLM like Mistral or Llama3) |
| **Visualization**       | Plotly                                    |

## 📈 Performance Snapshot

| Metric             | Value                                            |
| ------------------ | ------------------------------------------------ |
| **p95 latency**    | ~250–400 ms (local inference, small input)       |
| **Cost / request** | $0 (fully local)                                 |

## 🧩 Project Structure

```text
smart_finance_assistant/
│── backend
│   ├── main.py                
│   ├── expense_handler.py      
│   ├── llm_agent.py           
│   ├── models/                 
│
│── frontend/
│   ├── app.py                 
│
│── data/
│   ├── sample_expenses.csv   
│── requirements.txt

```

## Setup & Run Instructions

### Clone the Repo

```bash
git clone https://github.com/yourusername/ai-expense-tracker.git
cd ai-expense-tracker
```

### Install Dependencies

```python
pip install -r requirements.txt
```
### Install and Run Ollama

Download Ollama from https://ollama.ai

Then pull a local model (e.g., Mistral):

```bash
ollama pull mistral
```

Run ollama in CMD

```bash
ollama run MODELNAME
```

### Start FastAPI Backend

```bash
cd backend
uvicorn main:app --reload --port 8000
```

### Start Streamlit Frontend

```bash
cd frontend
streamlit run app.py
```

### How the AI Works

- Streamlit sends expense data to FastAPI.
- FastAPI sends structured text to Ollama model.
- Ollama analyzes and returns human-like insights.
- Results are displayed in the frontend with graphs + summaries.

### Example Insight

“You spent 45% of your budget on Food this week. Consider reducing dining expenses or planning home-cooked meals.”

### Future Improvements

- Add authentication & multi-user support
- Store expenses in database (SQLite or PostgreSQL)
- Connect with Google sheet using MCP

### ⭐ Star this repo if you find it useful!

<p align="center">
<img src="https://github.com/uzairafridi00/smart_finance_assistant/blob/main/images/smart_personal_finance_assistant.png" alt="Image Not Found"/>
</p>

<p align="center">
<img src="https://github.com/uzairafridi00/smart_finance_assistant/blob/main/images/newplot.png" alt="Image Not Found"/>
</p>
