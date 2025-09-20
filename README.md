# AutonoGroq - Autonomous AI Agent 🤖

AutonoGroq is an autonomous AI agent designed to interact with users in a conversational manner. It can answer general queries, analyze uploaded sales reports (CSV, Excel, PDF), and remember facts for context-aware responses. The interface provides a dynamic left-right chat layout for smooth conversation flow.

## Features

- **Conversational AI:** Ask questions and get intelligent answers.
- **File Analysis:** Upload CSV, Excel, or PDF sales reports for insights.
- **Fact Memory:** Remembers key facts to provide contextual responses.
- **Dynamic Chat UI:** Left-right alignment for agent and user messages, similar to modern LLM interfaces.
- **Seamless Interaction:** Typing indicators and automatic chat input clearing.

## How to Use

1. Clone the repository:
   ```bash
   git clone https://github.com/YourUsername/AutonoGroq.git
   cd AutonoGroq
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Set your Groq API key:

bash
Copy code
export GROQ_API_KEY="your_api_key_here"  # Linux/Mac
setx GROQ_API_KEY "your_api_key_here"     # Windows
Run the app:

bash
Copy code
streamlit run app.py
Upload a sales file (CSV, Excel, PDF) and start chatting with the agent.

Example Queries
"What is machine learning?"

"Summarize the last week's sales report."

"Which product sold the most last week?"

Technologies Used
Python 3.12

Streamlit for UI

Groq AI API for LLM responses

LangGraph for fact memory

LlamaIndex for document indexing
