import os
import streamlit as st
from src.langgraphagenticai.ui.uiconfig import Config


class LoadStreamlitUI:
    """
    Robust Streamlit sidebar UI for selecting LLM, usecase and API keys (Groq, TAVILY).
    This version:
      - normalizes various shapes returned by Config (list, dict, tuples, etc.)
      - pre-initializes session_state keys BEFORE instantiating widgets
      - never assigns to st.session_state[key] after a widget with that key exists
      - keeps self.user_controls updated with current widget values
    """

    def __init__(self, debug: bool = False):
        self.config = Config()
        self.user_controls = {}
        self.debug = debug

    def _normalize_options(self, opts):
        """Convert many shapes into a list of strings suitable for st.selectbox."""
        if opts is None:
            return []
        # dict -> keys
        if isinstance(opts, dict):
            return [str(k) for k in opts.keys()]

        # If it's an iterable of tuples like [(label, value), ...], prefer the first element (label)
        try:
            # convert to list to allow multiple passes
            lst = list(opts)
            normalized = []
            for item in lst:
                # common case: tuple (label, value)
                if isinstance(item, (list, tuple)) and len(item) >= 1:
                    normalized.append(str(item[0]))
                else:
                    normalized.append(str(item))
            return normalized
        except Exception:
            return [str(opts)]

    def load_streamlit_ui(self):
        # Page setup (call once)
        st.set_page_config(page_title=self.config.get_page_title(), layout="wide")
        st.header(self.config.get_page_title())

        # Pre-init session state keys (safe to assign BEFORE widget creation)
        if "GROQ_API_KEY" not in st.session_state:
            st.session_state["GROQ_API_KEY"] = ""
        if "TAVILY_API_KEY" not in st.session_state:
            st.session_state["TAVILY_API_KEY"] = ""

        with st.sidebar:
            # --- LLM selection ---
            llm_options = self._normalize_options(self.config.get_llm_options())
            if not llm_options:
                llm_options = ["Groq", "Other"]
            selected_llm = st.selectbox("Select LLM", llm_options, key="selected_llm")
            self.user_controls["selected_llm"] = selected_llm

            # If Groq is chosen show model + API key
            if isinstance(selected_llm, str) and selected_llm.strip().lower() == "groq":
                model_options = self._normalize_options(self.config.get_groq_model_options())
                if not model_options:
                    model_options = ["groq-1", "groq-2"]
                selected_groq_model = st.selectbox("Select Model", model_options, key="selected_groq_model")
                self.user_controls["selected_groq_model"] = selected_groq_model

                # Groq API key widget (session_state pre-initialized above)
                groq_api_key = st.text_input(
                    "Groq API Key",
                    type="password",
                    key="GROQ_API_KEY",
                    placeholder="Enter Groq API key"
                )
                # Do NOT assign st.session_state["GROQ_API_KEY"] after this line; widget manages it.
                self.user_controls["GROQ_API_KEY"] = groq_api_key
                if groq_api_key:
                    os.environ["GROQ_API_KEY"] = groq_api_key
                else:
                    st.info("Enter Groq API key to enable Groq usage.")

            # --- Usecase selection ---
            usecase_options = self._normalize_options(self.config.get_usecase_options())
            if not usecase_options:
                usecase_options = ["Basic Chatbot With Web", "Other Usecase"]
            selected_usecase = st.selectbox("Select Usecase", usecase_options, key="selected_usecase")
            self.user_controls["selected_usecase"] = selected_usecase

            # Optional debug expander to see exactly what the selectbox returned
            if self.debug:
                with st.expander("DEBUG: raw values"):
                    st.write("llm_options (normalized):", llm_options)
                    st.write("selected_llm (repr):", repr(selected_llm))
                    st.write("usecase_options (normalized):", usecase_options)
                    st.write("selected_usecase (repr):", repr(selected_usecase))
                    st.write("st.session_state keys:", list(st.session_state.keys()))

            # --- TAVILY API Key: show when Basic Chatbot With Web is selected ---
            # Matching is robust: case-insensitive and trimmed
            target_label = "Basic Chatbot With Web"
            if (
                isinstance(selected_usecase, str)
                and selected_usecase.strip().lower() == target_label.lower()
            ):
                # TAVILY widget (session_state pre-init above)
                tavily_api_key = st.text_input(
                    "TAVILY API Key",
                    type="password",
                    key="TAVILY_API_KEY",
                    placeholder="Enter TAVILY API key"
                )
                # Widget manages st.session_state["TAVILY_API_KEY"], so don't reassign it.
                self.user_controls["TAVILY_API_KEY"] = tavily_api_key
                if tavily_api_key:
                    os.environ["TAVILY_API_KEY"] = tavily_api_key
                else:
                    st.info("Enter TAVILY API Key to enable the Basic Chatbot With Web usecase.")
            else:
                # Show a disabled hint so the user sees where the key will appear
                st.text_input(
                    "TAVILY API Key (choose 'Basic Chatbot With Web' to enable)",
                    type="password",
                    disabled=True,
                    key="TAVILY_API_KEY_disabled"
                )

        return self.user_controls
