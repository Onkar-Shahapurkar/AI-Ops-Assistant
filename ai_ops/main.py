# main.py  (VERY IMPORTANT FILE)

import streamlit as st

# IMPORT TOOLS FIRST SO THEY REGISTER THEMSELVES
import tools.weather_tool
import tools.news_tool

# THEN IMPORT UI
from ui.streamlit_app import app

if __name__ == "__main__":
    app()
