import streamlit as st
import main as back
files = st.file_uploader("Upload your PDF files", help="We currently only support .pdf files.",accept_multiple_files=True)


