import streamlit as st
from src.langgraphagenticai.ui.streamlitui.load_ui import LoadStreamlitUI
from src.langgraphagenticai.LLMs.groqllm import GroqLLM
from src.langgraphagenticai.graph.graph_builder import GraphBuilder
from src.langgraphagenticai.ui.streamlitui.display_results import DisplayResultStreamlit

def load_langgraph_agentic_ai_app():
    ui = LoadStreamlitUI()
    user_input = ui.load_streamlit_ui()

    if not user_input : 
        st.error("Error : Failed to load user input from the UI.")
        return


    user_message = st.chat_input("Enter Your Message")

    if user_message : 
        try : 
            obj_llm_config = GroqLLM(user_controls_input=user_input)
            model = obj_llm_config.get_llm_model()

            if not model :
                st.error("Error : LLM Model Not intialized")
                return
            
            usecase = user_input.get("selected_usecase")

            if not usecase :
                st.error("Error : No usecase selected")
                return
            
            grah_builder = GraphBuilder(model)

            try : 
                graph = grah_builder.setup_graph(usecase)
                DisplayResultStreamlit(usecase,graph,user_message).display_result_on_ui()
            except Exception as e : 
                st.error(f"Error:{e}")
                return
                
        except Exception as e : 
            st.error(f"Error:{e}")
            return 
