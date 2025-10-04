import pandas as pd
from io import BytesIO

def process_expense_file(data: bytes, filename: str):
    if filename.endswith(".csv"):
        df = pd.read_csv(BytesIO(data))
    elif filename.endswith(".xlsx"):
        df = pd.read_excel(BytesIO(data))
    else:
        raise ValueError("Unsupported file format")

    # Normalize columns (assume: Date, Category, Amount, Description)
    df.columns = [c.strip().lower() for c in df.columns]
    return df

def get_summary(df: pd.DataFrame):
    total_spent = df["amount"].sum()
    by_category = df.groupby("category")["amount"].sum().to_dict()
    return {
        "total_spent": total_spent,
        "by_category": by_category
    }