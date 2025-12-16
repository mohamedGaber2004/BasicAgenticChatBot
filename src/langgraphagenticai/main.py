import streamlit as st
from src.langgraphagenticai.ui.streamlitui.load_ui import LoadStreamlitUI
from src.langgraphagenticai.LLMs.groqllm import GroqLLM
from src.langgraphagenticai.graph.graph_builder import GraphBuilder
from src.langgraphagenticai.ui.streamlitui.display_results import DisplayResultStreamlit

def load_langgraph_agentic_ai_app():
    ui = LoadStreamlitUI()
    user_input = ui.load_streamlit_ui()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_message = st.chat_input("Enter Your Message")

    if user_message:
        with st.chat_message("user"):
            st.write(user_message)

        st.session_state.messages.append(
            {"role": "user", "content": user_message}
        )

        try:
            obj_llm_config = GroqLLM(user_controls_input=user_input)
            model = obj_llm_config.get_llm_model()

            usecase = user_input.get("selected_usecase")
            graph_builder = GraphBuilder(model)
            graph = graph_builder.setup_graph(usecase)

            result = graph.invoke({
                "messages": st.session_state.messages
            })

            ai_message = result["messages"][-1].content

            with st.chat_message("assistant"):
                st.write(ai_message)

            st.session_state.messages.append(
                {"role": "assistant", "content": ai_message}
            )

        except Exception as e:
            st.error(f"Error: {e}")

