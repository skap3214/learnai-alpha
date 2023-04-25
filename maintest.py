import streamlit as st
from text_grabber import Text
from text_conversions import Converter
from streamlit_ace import st_ace

st.set_page_config(
    page_title="LearnAI",
    layout="wide"
)

@st.cache_data
def get_data(video_url):
    if not (video_url):
        return False
    #Add video url to session state
    if 'video_url' not in st.session_state:
        st.session_state['video_url'] = video_url
    
    #Get transcript
    transcript = Text().youtube(video_url)
    if 'transcript' not in st.session_state:
        st.session_state['transcript'] = transcript
    else:
        st.session_state['transcript'] = transcript
    converter = Converter(transcript)
    #Get mcqs
    mcq = converter.mcq_other()
    mcq = "MCQ"

    #Get Notes
    cheat_sheet = converter.cheat_sheet()


    #Get code_question
    code_question = converter.generate_code(video_url)

    


    return cheat_sheet, mcq, code_question



video_input = st.text_input("Enter YouTube URL", placeholder="Please keep the video under 9 minutes")
video_col, features_col = st.columns([2,1])
with video_col:
    if video_input:
        st.video(video_input)
    else:
        st.write("Add a YouTube URL Link to get started!!")

with features_col:
    if video_input:
        cheat_sheet, mcq, code_question = get_data(video_input)
        notes_tab, mcq_tab, chat_tab = st.tabs(["Notes","MCQ's","Chat With Lenny"])
        with notes_tab:
            st.write("Notes")
            st.text_area("Write your notes here", value=cheat_sheet)
        with mcq_tab:
            st.write("MCQs")
            st.write(mcq)
            prompt = code_question['prompt']
            answer = code_question['answer']
        with chat_tab:
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
                if 'user_input' not in st.session_state:
                    st.session_state['user_input'] = user_input
                else:
                    st.session_state['user_input'] = user_input
                if st.session_state.user_input:
                    user_message = f'<div class="message-container"><div class="message user-message">{user_input}</div></div>'
                    conversation.markdown(user_message, unsafe_allow_html=True)
                    st.session_state.conversation_history.append(user_message)
                    
                    with st.spinner("Thinking..."):
                        lenny_response = converter.chatbot(user_input)
                        lenny_message = f'<div class="message-container"><div class="message bot-message">{lenny_response}</div></div>'
                        conversation.markdown(lenny_message, unsafe_allow_html=True)
                        st.session_state.conversation_history.append(lenny_message)
    
