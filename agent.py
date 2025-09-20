import os
import json
import pandas as pd
import pdfplumber
from groq import Groq
from langgraph_helper import add_fact, query_fact

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

def query_groq_api(prompt: str):
    chat_completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return chat_completion.choices[0].message.content

def summarize_sales_report(file_path):
    """Reads CSV, Excel, or PDF file and returns a brief summary."""
    try:
        if file_path.endswith(".csv"):
            df = pd.read_csv(file_path)
            summary_text = f"Sales report summary:\nTotal rows: {len(df)}\nColumns: {', '.join(df.columns)}\n"
            if "Sales" in df.columns and "Product" in df.columns:
                top_product = df.groupby("Product")["Sales"].sum().idxmax()
                summary_text += f"Top-selling product: {top_product}\n"
            return summary_text

        elif file_path.endswith((".xlsx", ".xls")):
            df = pd.read_excel(file_path)
            summary_text = f"Sales report summary:\nTotal rows: {len(df)}\nColumns: {', '.join(df.columns)}\n"
            if "Sales" in df.columns and "Product" in df.columns:
                top_product = df.groupby("Product")["Sales"].sum().idxmax()
                summary_text += f"Top-selling product: {top_product}\n"
            return summary_text

        elif file_path.endswith(".pdf"):
            text = ""
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() + "\n"
            # Optionally, truncate very long PDFs
            if len(text) > 2000:
                text = text[:2000] + "\n...(truncated)"
            return f"Sales report extracted from PDF:\n{text}"
        else:
            return "Unsupported file type."
    except Exception as e:
        return f"Could not read the file: {e}"

def agent_respond(user_input, memory=[], sales_file=None):
    facts = query_fact()

    # Summarize file if provided
    file_summary = ""
    if sales_file:
        file_summary = summarize_sales_report(sales_file)

    prompt = f"""
You are an autonomous AI agent.
Memory: {memory}
Knowledge: {facts}
Sales Report Summary: {file_summary}
User said: "{user_input}"
Respond clearly and include new facts in JSON format:
{{
    "response_text": "...",
    "facts": [
        {{"subject": "...", "relation": "...", "object": "..."}}
    ],
    "actions": []
}}
    """

    text = query_groq_api(prompt)

    try:
        json_output = json.loads(text)
    except:
        json_output = {"response_text": text, "facts": [], "actions": []}

    for fact in json_output.get("facts", []):
        add_fact(fact["subject"], fact["relation"], fact["object"])

    return json_output
