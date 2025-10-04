from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io

# Import your LLM logic
from llm_agent import set_expenses, query_llm

app = FastAPI()

# Allow CORS (frontend can call API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

EXPENSE_DF: pd.DataFrame | None = None


def clean_expense_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generic cleanup of uploaded expense data
    """
    df = df.copy()

    # Identify amount column
    amount_col = None
    for col in df.columns:
        if "amount" in col.lower() or "price" in col.lower() or "cost" in col.lower():
            amount_col = col
            break
    if not amount_col:
        amount_col = df.select_dtypes(include="number").columns[0]

    df["amount"] = df[amount_col]

    # Identify category column
    category_col = None
    for col in df.columns:
        if "category" in col.lower() or "type" in col.lower():
            category_col = col
            break
    if not category_col:
        category_col = df.select_dtypes(include="object").columns[0]

    df["category"] = df[category_col]

    # Optional: Date column
    date_col = None
    for col in df.columns:
        if "date" in col.lower():
            date_col = col
            break
    if date_col:
        df["date"] = pd.to_datetime(df[date_col], errors="coerce")

    return df


@app.post("/upload-expenses/")
async def upload_expenses(file: UploadFile):
    global EXPENSE_DF

    # Read file
    content = await file.read()
    if file.filename.endswith(".csv"):
        df = pd.read_csv(io.BytesIO(content))
    else:
        df = pd.read_excel(io.BytesIO(content))

    # Clean & store
    EXPENSE_DF = clean_expense_data(df)
    set_expenses(EXPENSE_DF)  # handoff to llm_agent

    total_spent = float(EXPENSE_DF["amount"].sum())
    by_category = EXPENSE_DF.groupby("category")["amount"].sum().to_dict()

    return {
        "summary": {
            "total_spent": total_spent,
            "by_category": by_category
        }
    }


@app.post("/ask/")
async def ask(question: str = Form(...)):
    """
    Forward user question to LLM (via llm_agent)
    """
    answer = query_llm(question)
    return {"answer": answer}