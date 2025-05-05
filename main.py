
import threading
import time

import streamlit as st
import html_scraper as scraper

import names_parser

# Setup once
if 'stop_event' not in st.session_state:
    st.session_state.stop_event = threading.Event()
if 'running' not in st.session_state:
    st.session_state.running = False
if 'names_input' not in st.session_state:
    st.session_state.names_input = ""

def stop_running():
    st.text("Stopped running")
    st.session_state.stop_event.set()
    st.session_state.running = False
    st.session_state.names_input = ""

def start_running(name_str):
    st.text("Started scrapping...")
    st.session_state.names = names_parser.names_parser(name_str)
    st.session_state.stop_event.clear()

    t = threading.Thread(target=scraper.writeInformationToFiles,
                         args=(st.session_state.names, st.session_state.stop_event,))
    t.start()
    st.session_state.running = True


st.title("Vessel Position Extractor")
st.text_input("Please enter the names in the following format: vessel1,vessel2", key = "names_input")

if not st.session_state.running:
    st.button("Start scraping", on_click=start_running, args = (st.session_state.names_input,))

if st.session_state.running:
    st.button("🛑 Stop scraping", on_click=stop_running)


