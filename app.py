import streamlit as st
from text_grabber import ToText
from text_conversions import Converter
st.set_page_config(
    page_title="LearnAI",
    layout="wide"
)
def display_video(col1, video_url):
    if video_url:
        st.session_state.video_url = video_url
        with col1:
            st.video(video_url)
            st.write("Transcript:")
            if "transcript" not in st.session_state:
                st.session_state.transcript = ToText().youtube(video_url)
            st.write(st.session_state.transcript)



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
        converter = Converter(st.session_state.transcript)
        st.header("Chat")

        if "conversation_history" not in st.session_state:
            st.session_state.conversation_history = []

        with st.expander("Chat History", expanded=True):
            conversation = st.container()
            
            st.markdown("""
            <style>
                .message-container {
                    margin-bottom: 10px;
                    overflow: auto;
                }
                .message-container .message {
                    margin: 5px 10px;
                    padding: 5px 10px;
                    border-radius: 10px;
                    max-width: 60%;
                }
                .message-container .user-message {
                    background-color: #007AFF;
                    color: white;
                    float: right;
                }
                .message-container .bot-message {
                    background-color: #1c1c1e;
                    color: white;
                    float: left;
                }
                .loader {
                    border-top: 5px solid rgba(255, 255, 255, 0.2);
                    border-right: 5px solid rgba(255, 255, 255, 0.2);
                    border-bottom: 5px solid rgba(255, 255, 255, 0.2);
                    border-left: 5px solid white;
                    animation: spin 0.8s linear infinite;
                }
                @keyframes spin {
                    from {
                        transform: rotate(0deg);
                    }
                    to {
                        transform: rotate(360deg);
                    }
                }
            </style>

            """, unsafe_allow_html=True)
            
            conversation.markdown(f'<div class="message-container"><div class="message bot-message">Hi! How can I help you?</div></div>',
                                  unsafe_allow_html=True)

            for message in st.session_state.conversation_history:
                conversation.markdown(message, unsafe_allow_html=True)
            
            user_input = st.text_input("Enter your message:")
            
            if user_input:
                user_message = f'<div class="message-container"><div class="message user-message">{user_input}</div></div>'
                conversation.markdown(user_message, unsafe_allow_html=True)
                st.session_state.conversation_history.append(user_message)
                
                with st.spinner("Thinking..."):
                    lenny_response = converter.chatbot(user_input)
                    lenny_message = f'<div class="message-container"><div class="message bot-message">{lenny_response}</div></div>'
                    conversation.markdown(lenny_message, unsafe_allow_html=True)
                    st.session_state.conversation_history.append(lenny_message)
                
                user_input = ''



def main():
    st.title("Learn.ai")

    if "video_url" not in st.session_state:
        st.session_state.video_url = ""

    video_url = st.text_input("Enter YouTube video URL:", value=st.session_state.video_url)
    if video_url:
        col1, col2 = st.columns([2, 1])

        display_video(col1, video_url)

        with col2:
            tab1, tab2, tab3 = st.tabs(["Notes", "MCQ", "Chat"])
            notes_tab(tab1)
            mcq_tab(tab2)
            chat_tab(tab3)


if __name__ == "__main__":
    main()