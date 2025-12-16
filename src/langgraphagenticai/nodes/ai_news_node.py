import os
from tavily import TavilyClient
from langchain_core.prompts import ChatPromptTemplate


class Ai_News:
    def __init__(self, llm):
        self.llm = llm
        self.tavily = TavilyClient()

    # -----------------------------
    # NODE 1: Fetch News
    # -----------------------------
    def fetch_news(self, state: dict) -> dict:
        user_text = state["messages"][-1].content.lower().strip()

        allowed = {"daily", "weekly", "monthly", "yearly"}
        frequency = user_text if user_text in allowed else "daily"

        response = self.tavily.search(
            query="Top Artificial Intelligence (AI) technology news Egypt and globally",
            topic="news",
            time_range={"daily":"d","weekly":"w","monthly":"m","yearly":"y"}[frequency],
            max_results=20
        )

        return {
            **state,
            "frequency": frequency,
            "news_data": response.get("results", [])
        }

    # -----------------------------
    # NODE 2: Summarize
    # -----------------------------
    def summarize_news(self, state: dict) -> dict:
        articles = state.get("news_data", [])

        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
"""Summarize AI news articles into markdown.
For each item include:
- Date in **YYYY-MM-DD**
- Short concise summary
- Sort by latest first
- Source URL

Format:
### YYYY-MM-DD
- [Summary](URL)"""
            ),
            ("user", "{articles}")
        ])

        articles_text = "\n\n".join(
            f"Date: {a.get('published_date','')}\n"
            f"Content: {a.get('content','')}\n"
            f"URL: {a.get('url','')}"
            for a in articles
        )
        try:
            response = self.llm.invoke(prompt.format(articles=articles_text))
        except Exception as e :
            print(f"Error invoking the tool: {str(e)}")
            response = None

        summary = response.content if response else "No summary available."

        return {
            **state,
            "summary": summary
        }

    # -----------------------------
    # NODE 3: Save Result
    # -----------------------------
    def save_result(self, state: dict) -> dict:
        os.makedirs("AINews", exist_ok=True)
        frequency = state.get("frequency", "daily")
        summary = state.get("summary", "")
        filename = f"AINews/{state['frequency']}_summary.md"

        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"# {state['frequency'].capitalize()} AI News Summary\n\n")
            f.write(state["summary"])

        return {
            **state,
            "filename": filename
        }
