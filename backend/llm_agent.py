import requests
import pandas as pd
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "mistral:latest"

EXPENSE_DF: pd.DataFrame | None = None

def set_expenses(df: pd.DataFrame):
    """Store the uploaded dataframe in memory"""
    global EXPENSE_DF
    EXPENSE_DF = df


def summarize_data(df: pd.DataFrame) -> str:
    """Create a text summary of the dataframe for the LLM"""
    summary_parts = []

    # Detect numeric columns (like amount, value, price, etc.)
    numeric_cols = df.select_dtypes(include="number").columns
    if len(numeric_cols) > 0:
        for col in numeric_cols:
            total = df[col].sum()
            summary_parts.append(f"Total {col}: {total}")

            # Try to detect a categorical column to group by
            cat_cols = df.select_dtypes(include="object").columns
            for cat in cat_cols:
                grouped = df.groupby(cat)[col].sum().to_dict()
                summary_parts.append(f"By {cat} for {col}: {grouped}")

    # Trend analysis if Date column exists
    date_cols = [c for c in df.columns if "date" in c.lower()]
    if date_cols:
        date_col = date_cols[0]  # pick first date-like column
        try:
            df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
            df["Month"] = df[date_col].dt.to_period("M")
            for col in numeric_cols:
                monthly = df.groupby("Month")[col].sum().to_dict()
                summary_parts.append(f"Monthly trend for {col}: {monthly}")
        except Exception:
            pass

    return "\n".join(summary_parts)


def query_llm(question: str) -> str:
    """Query Ollama with expense context + user question"""
    if EXPENSE_DF is None:
        return "No data available. Please upload a CSV/Excel file first."

    try:
        # Generate context from dataframe
        context = summarize_data(EXPENSE_DF)

        system_prompt = f"""
        You are a financial assistant. Analyze the following dataset:

        {context}

        Answer the following question strictly based on the data.
        Provide insights such as overspending, savings tips, and comparisons if possible.
        """

        payload = {
            "model": MODEL_NAME,
            "prompt": f"{system_prompt}\n\nUser: {question}\nAssistant:",
            "options": {"num_predict": 300}
        }

        # Call Ollama (streaming)
        response = requests.post(OLLAMA_URL, json=payload, stream=True)

        answer = ""
        for line in response.iter_lines():
            if line:
                try:
                    data = json.loads(line.decode("utf-8"))
                    if "response" in data:
                        answer += data["response"]
                except Exception:
                    pass

        return answer.strip() if answer else "No response from Ollama."

    except Exception as e:
        return f"Error connecting to Ollama: {str(e)}"