import streamlit as st

def main():
    st.title("Learn.ai")

    # Input for YouTube video URL
    video_url = st.text_input("Enter YouTube video URL:")

    col1, col2 = st.columns(2)

    # col1
    if video_url:
        with col1:
            st.video(video_url)

    # col2
    with col2:
        button_col1, button_col2, button_col3 = st.columns(3)
        with button_col1:
            notes_button = st.button("Notes")
        with button_col2:
            mcq_button = st.button("MCQ")
        with button_col3:
            chatbot_button = st.button("Chatbot")

        if notes_button:
            # Display notes section
            st.header("Notes")
            st.text_area("Take notes here:")

        elif mcq_button:
            # Display MCQ section
            st.header("MCQ")
            # Add sample MCQs or user-defined MCQs

        elif chatbot_button:
            # Display chatbot section
            st.header("Chatbot")
            # Add your chatbot implementation

if __name__ == "__main__":
    main()