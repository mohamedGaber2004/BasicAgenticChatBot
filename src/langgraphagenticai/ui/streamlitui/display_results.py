import streamlit as st
from langchain_core.messages import HumanMessage , AIMessage , ToolMessage
import json

class DisplayResultStreamlit : 
    def __init__(self,usecase,graph,user_message) : 
        self.usecase = usecase
        self.graph = graph
        self.user_message = user_message

    def display_result_on_ui(self):
        """
        Display user message and assistant response on Streamlit UI with streaming.
        Maintains full chat history using st.session_state.
        """
        user_message = self.user_message
        graph = self.graph
        usecase = self.usecase.lower().strip()

        if "messages" not in st.session_state:
            st.session_state.messages = []

        if "basic chatbot" in usecase:
            st.session_state.messages.append({"role": "user", "content": user_message})

            with st.chat_message("user"):
                st.write(user_message)

            with st.chat_message("assistant"):
                response_container = st.empty()
                full_response = ""

                try:
                    for event in graph.stream({"messages": [HumanMessage(content=user_message)]}):
                        for value in event.values():
                            msgs = value.get("messages", [])
                            if not isinstance(msgs, list):
                                msgs = [msgs]
                            for msg in msgs:
                                if isinstance(msg, AIMessage):
                                    full_response += msg.content
                                    response_container.markdown(full_response)

                except Exception as e:
                    st.error(f"Graph streaming error: {e}")

            st.session_state.messages.append({"role": "assistant", "content": full_response})

            for msg in st.session_state.messages:
                with st.chat_message(msg["role"]):
                    st.write(msg["content"])

        elif usecase =="Basic Chatbot With Web" : 
            st.session_state.messages.append({"role": "user", "content": user_message})

            with st.chat_message("user"):
                st.write(user_message)

            with st.chat_message("assistant"):
                response_container = st.empty()
                full_response = ""

                try:
                    for event in graph.stream({"messages": [HumanMessage(content=user_message)]}):
                        for value in event.values():
                            msgs = value.get("messages", [])
                            if not isinstance(msgs, list):
                                msgs = [msgs]
                            for msg in msgs:
                                if isinstance(msg, AIMessage):
                                    full_response += msg.content
                                    response_container.markdown(full_response)

                except Exception as e:
                    st.error(f"Graph streaming error: {e}")

            st.session_state.messages.append({"role": "assistant", "content": full_response})

            st.write("WEB SEARCH RESULTS ...")
            for msg in st.session_state.messages:
                with st.chat_message(msg["role"]):
                    st.write(msg["content"])