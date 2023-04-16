import streamlit as st
import main as back
import os

pdf = st.file_uploader("Upload your PDF files here", help="We currently only support .pdf files.",accept_multiple_files=True)
if pdf:
    merged_output = 'output.pdf'
    docsearch, chain = back.preprocess_text(pdf, merged_output)
    st.write(back.pdf_summary(docsearch, chain))  # Print part_1 (summary)
    st.write(back.pdf_questions_answers(docsearch, chain))  # Print part_2 (questions and answers)
    os.remove(merged_output)


