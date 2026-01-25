# BasicAgenticChatBot

A sophisticated agentic chatbot application built with LangGraph and Streamlit that provides multiple AI-powered use cases including basic chat, tool-augmented chat, and AI news summarization.

## 🎯 Features

- **Multiple Use Cases**
  - Basic Chatbot: Simple conversational AI
  - Chatbot with Tools: Enhanced chatbot with web search capabilities using Tavily
  - AI News Summarization: Automatically fetch and summarize the latest AI news

- **LLM Support**: Powered by Groq LLMs with configurable model selection
- **Interactive UI**: Streamlit-based user interface for seamless interaction
- **Message History**: Maintains conversation history within session state
- **Tool Integration**: Integrated Tavily search tool for web search capabilities
- **Vector Search**: FAISS integration for semantic search capabilities

## 📋 Prerequisites

- Python 3.8+
- API Keys:
  - Groq API Key (for LLM access)
  - Tavily API Key (for news/search functionality)

## 🚀 Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd BasicAgenticChatBot
```

2. **Create a virtual environment** (recommended)
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

## 🔧 Configuration

The application uses a configuration system located in `src/langgraphagenticai/ui/uiconfig.ini` and `src/langgraphagenticai/ui/uiconfig.py`.

You can configure:
- LLM model selection
- API keys for Groq and Tavily
- Page title and UI settings

## 📦 Project Structure

```
BasicAgenticChatBot/
├── app.py                          # Entry point
├── requirements.txt                # Project dependencies
├── AINews/                         # AI news output storage
│   └── daily_summary.md           # Generated news summaries
└── src/
    └── langgraphagenticai/
        ├── main.py                # Main application logic
        ├── LLMs/
        │   └── groqllm.py        # Groq LLM configuration
        ├── graph/
        │   └── graph_builder.py  # LangGraph setup
        ├── nodes/
        │   ├── basic_chatbot_node.py           # Basic chat node
        │   ├── chatbot_with_tool_nodes.py      # Tool-augmented chat node
        │   └── ai_news_node.py                 # News summarization node
        ├── state/
        │   └── state.py          # State management
        ├── tools/
        │   └── search_tool.py    # Tavily search integration
        └── ui/
            ├── uiconfig.py       # UI configuration
            ├── uiconfig.ini      # Configuration file
            └── streamlitui/
                ├── load_ui.py           # Streamlit UI loader
                └── display_results.py   # Result display
```

## 🏃 Running the Application

1. **Start the Streamlit app**
```bash
streamlit run app.py
```

2. The application will open in your default browser at `http://localhost:8501`

3. **Configure your settings**:
   - Select your preferred LLM model
   - Enter your API keys
   - Choose a use case (Basic Chat, Chat with Tools, or AI News)

4. **Interact with the chatbot**:
   - Type your messages in the chat input
   - For AI News: Enter the timeframe (daily, weekly, monthly, yearly)
   - View responses in real-time

## 🛠️ Use Cases

### 1. Basic Chatbot
Simple conversational AI that responds to user queries without external tools.

### 2. Chatbot with Tools
Enhanced chatbot that can search the web using Tavily to provide current information and answer questions based on real-time data.

### 3. AI News Summarization
Automatically fetches and summarizes the latest AI technology news from around the world with:
- Configurable timeframe (daily, weekly, monthly, yearly)
- Markdown-formatted summaries
- Automatic storage of summaries in `AINews/daily_summary.md`

## 📚 Dependencies

- **langchain**: LLM framework and utilities
- **langgraph**: Graph-based workflow orchestration
- **langchain_community**: Community integrations
- **langchain_core**: Core LLM abstractions
- **langchain_groq**: Groq API integration
- **streamlit**: Web UI framework
- **tavily-python**: Web search API
- **faiss-cpu**: Vector similarity search

See `requirements.txt` for complete list and versions.

## 🔑 API Keys

### Groq API Key
Get your Groq API key from [Groq Console](https://console.groq.com)

### Tavily API Key
Get your Tavily API key from [Tavily Dashboard](https://tavily.com)

## 📝 Example Usage

```python
# The app runs via:
streamlit run app.py

# Then interact through the web UI to:
# 1. Select your LLM model
# 2. Enter API credentials
# 3. Choose a use case
# 4. Chat or fetch news
```

## 🔄 Workflow

1. User enters message or selects timeframe
2. Message is added to session state
3. LLM configuration is initialized with Groq
4. Graph is built based on selected use case
5. Graph processes the input through appropriate nodes
6. Result is returned and displayed in chat
7. Message history is updated in session state

## 📄 Output

- **Chat responses**: Displayed in real-time in the Streamlit UI
- **AI News**: Saved to `AINews/daily_summary.md` with formatted summaries

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📄 License

See LICENSE file for details.

## ✨ Notes

- Conversation history is maintained within the Streamlit session
- News summaries are automatically formatted in Markdown
- Tool integration enables real-time web search capabilities
- All API calls are configured through the UI sidebar