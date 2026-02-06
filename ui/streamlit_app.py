import streamlit as st
from agents.planner import generate_plan
from agents.executor import execute_plan
from agents.verifier import verify_execution
from core.tool_registry import ToolRegistry

def app():
    st.set_page_config(page_title="AI Operations Assistant", layout="wide")

    st.title("🤖 AI Operations Assistant (Production System)")

    st.sidebar.header("Available Tools")
    st.sidebar.json(ToolRegistry.list_tools())

    user_task = st.text_area("Enter your task:", height=120)

    if st.button("Run Assistant"):
        if not user_task.strip():
            st.error("Please enter a task first.")
            return

        try:
            with st.spinner("🧠 Planner is thinking..."):
                plan = generate_plan(user_task)

            st.subheader("📋 Planner Output")
            st.json(plan.dict())

        except Exception as e:
            st.error(f"❌ Planner Failed: {str(e)}")
            return

        try:
            with st.spinner("⚙️ Executor running tools..."):
                execution = execute_plan(plan)

            st.subheader("🔧 Executor Results")
            st.json(execution.dict())

        except Exception as e:
            st.error(f"❌ Executor Failed: {str(e)}")
            return

        try:
            with st.spinner("🔍 Verifier checking output..."):
                final = verify_execution(execution)

            st.subheader("✅ Final Verified Output")
            st.json(final.dict())

        except Exception as e:
            st.error(f"❌ Verifier Failed: {str(e)}")
