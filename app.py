import streamlit as st
import main as back
import os

st.title("Learn-:blue[AI]")
st.cache_data()
pdf = st.file_uploader("Upload your PDF files here", help="We currently only support .pdf files.",accept_multiple_files=True)
submit = st.button("Submit",type='primary')
if pdf and submit:
    with st.spinner("Creating Interactive Learning Experience"):
        merged_output = 'output.pdf'
        docsearch, chain = back.preprocess_text(pdf, merged_output)
        st.subheader("Summary")
        summary = back.pdf_summary(docsearch, chain)  # Print part_1 (summary)
        st.write(summary)
        st.subheader("Interactive Q&A")
        qa = back.pdf_questions_answers(docsearch, chain)  # Print part_2 (questions and answers)
        st.write(qa.replace("Question", "\n**Question**").replace("Answer", "\n**_Answer_**"))
        os.remove(merged_output)


