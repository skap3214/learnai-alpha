import streamlit as st


def display_video(col1, video_url):
    if video_url:
        st.session_state.video_url = video_url
        with col1:
            st.video(video_url)


def notes_tab(tab):
    with tab:
        st.header("Notes")
        st.text_area("Take notes here:")


def mcq_tab(tab):
    with tab:
        st.header("MCQ")
        st.subheader(f"Question {1}")
        st.radio("Choices", ["A", "B", "C", "D"])
        if st.button("Submit"):
            st.success("Correct!")


def chat_tab(tab):
    with tab:
        st.header("Chat")

        if "conversation_history" not in st.session_state:
            st.session_state.conversation_history = []

        user_input = st.text_input("Enter your message:")

        with st.expander("Chat History", expanded=True):
            conversation = st.container()
            conversation.markdown(f'<span style="color:green">**Lenny:**</span> Hi! How can I help you?',
                                  unsafe_allow_html=True)

            for message in st.session_state.conversation_history:
                conversation.markdown(message, unsafe_allow_html=True)
            if user_input:
                user_message = f'<span style="color:blue">**User:**</span> {user_input}'
                conversation.markdown(user_message, unsafe_allow_html=True)
                st.session_state.conversation_history.append(user_message)
                lenny_response = "Ok"
                lenny_message = f'<span style="color:green">**Lenny:**</span> {lenny_response}'
                conversation.markdown(lenny_message, unsafe_allow_html=True)
                st.session_state.conversation_history.append(lenny_message)


def main():
    st.title("Learn.ai")

    if "video_url" not in st.session_state:
        st.session_state.video_url = ""

    video_url = st.text_input("Enter YouTube video URL:", value=st.session_state.video_url)

    col1, col2 = st.columns([2, 1])

    display_video(col1, video_url)

    with col2:
        tab1, tab2, tab3 = st.tabs(["Notes", "MCQ", "Chat"])
        notes_tab(tab1)
        mcq_tab(tab2)
        chat_tab(tab3)


if __name__ == "__main__":
    main()
