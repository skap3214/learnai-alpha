import streamlit as st
from text_grabber import Text
from text_conversions import Converter
from streamlit_ace import st_ace

st.set_page_config(
    page_title="LearnAI",
    layout="wide"
)

def display_video(col1, video_url):
    if video_url:
        st.session_state.video_url = video_url
        if 'conversation_history' in st.session_state:
            del st.session_state.conversation_history
        with col1:
            st.video(video_url)
            if "transcript" not in st.session_state:
                st.session_state.transcript = Text().youtube(video_url)
            st.session_state.transcript = Text().youtube(video_url)
            code_dict = Converter(st.session_state.transcript).generate_code(st.session_state.video_url)
            prompt = code_dict['prompt']
            answer = code_dict['answer']
            st.write("Question", prompt)
            content = st_ace(theme = "ambiance")
            with st.expander("Answer", expanded=False):
                st.write(answer)
def notes_tab(tab):
    with tab:
        st.header("Notes")
        cheat_sheet = Converter(st.session_state.transcript).cheat_sheet()
        st.text_area("Take notes here:", value = cheat_sheet)


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
                    background-color: #0885FF;
                    color: white;
                    float: right;
                }
                .message-container .bot-message {
                    background-color: #3B3B3D;
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
    st.title("Learn.:blue[ai]")

    if "video_url" not in st.session_state:
        st.session_state.video_url = ""

    video_url = st.text_input("Enter YouTube video URL:", value=st.session_state.video_url)
    if video_url:
        col1, col2 = st.columns([2, 1])

        display_video(col1, video_url)

        with col2:
            tab1, tab2, tab3 = st.tabs(["Notes", "MCQ", "Chat"])
            with st.spinner("Loading..."):
                notes_tab(tab1)
                mcq_tab(tab2)
                chat_tab(tab3)


if __name__ == "__main__":
    main()