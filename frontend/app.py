import streamlit as st
import requests
import pandas as pd
import plotly.express as px   # ✅ Use Plotly for interactive charts

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Smart Personal Finance Assistant", page_icon="💰")
st.title("💰 Smart Personal Finance Assistant")

# Upload file
uploaded_file = st.file_uploader("Upload Expense CSV/Excel", type=["csv", "xlsx"])

if uploaded_file:
    with st.spinner("Uploading and processing expenses..."):
        files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
        try:
            res = requests.post(f"{API_URL}/upload-expenses/", files=files)
            if res.status_code == 200:
                summary = res.json()["summary"]

                st.success(f"✅ Total spent: {summary['total_spent']:.2f}")
                st.write("### 📊 Spending by Category")
                st.json(summary["by_category"])

                # ✅ Interactive Pie Chart
                categories = list(summary["by_category"].keys())
                amounts = list(summary["by_category"].values())

                df_chart = pd.DataFrame({
                    "Category": categories,
                    "Amount": amounts
                })

                fig = px.pie(df_chart, values="Amount", names="Category",
                             title="Expense Distribution",
                             hole=0.3,  # donut style
                             color_discrete_sequence=px.colors.qualitative.Set3)

                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig, use_container_width=True)

            else:
                st.error(f"Failed to process file. Error {res.status_code}: {res.text}")
        except requests.exceptions.ConnectionError:
            st.error("⚠️ Cannot connect to backend. Is FastAPI running?")

# Ask LLM
st.subheader("💡 Ask your finance assistant")
user_q = st.text_input("Type your question about your expenses:")

if st.button("Ask"):
    if not user_q.strip():
        st.warning("Please enter a question first.")
    else:
        try:
            res = requests.post(f"{API_URL}/ask/", data={"question": user_q})
            if res.status_code == 200:
                st.write("🤖 **Assistant:**", res.json().get("answer", "No answer"))
            else:
                st.error(f"Backend error: {res.status_code}")
        except requests.exceptions.ConnectionError:
            st.error("⚠️ Cannot connect to backend. Make sure FastAPI is running.")