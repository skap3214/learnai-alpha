import requests
import json
import streamlit as st
import text_conversions as tc
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
                response = requests.post("http://127.0.0.1:5000/transcript", json={"url": video_url})
                st.session_state.transcript = response.json()["response"]
            st.write(st.session_state.transcript)

def notes_tab(tab):
    with tab:
        st.header("Notes")
        converter = tc.Converter(st.session_state.transcript)
        cheat_sheet = converter.cheat_sheet()
        st.text_area("Take notes here:",value=cheat_sheet)

def display_quiz(quiz_questions):
    with st.form("quiz"):
        num_questions = len(quiz_questions)
        correct_count = 0
        
        for number, question in quiz_questions.items():
            st.write(f"{number}. {question['question']}")
            
            user_answer = st.radio("", list(question.values())[1:5], index=0)
            correct_option = question['correct']
            correct = question[correct_option]
            
            if user_answer == correct:
                correct_count += 1
            
            st.write("---")
        if st.form_submit_button("Submit"):
            st.write(f"You scored {correct_count} out of {num_questions}!")

@st.cache_data
def get_json():
    transcript = st.session_state.transcript
    convert = tc.Converter(transcript)
    get_mcq = convert.mcq()

@st.cache
def mcq_tab(tab):
    with open('mcq.json', 'r') as f:
        quiz_questions = json.load(f)
    
    display_quiz(quiz_questions)    

def chat_tab(tab):
    with tab:
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
                    response = requests.post("http://127.0.0.1:5000/chatbot", json={"text": st.session_state.transcript, "question": user_input})
                    lenny_response = response.json()["response"]
                    lenny_message = f'<div class="message-container"><div class="message bot-message">{lenny_response}</div></div>'
                    conversation.markdown(lenny_message, unsafe_allow_html=True)
                    st.session_state.conversation_history.append(lenny_message)

def main():
    st.title("Learn.ai")
    if "video_url" not in st.session_state:
        st.session_state.video_url = ""

    video_url = st.text_input("Enter YouTube video URL:", value=st.session_state.video_url)
    if video_url:
        col1, col2 = st.columns([2, 1])

        display_video(col1, video_url)

        with col2:
            tab1, tab2, tab3 = st.tabs(["Notes", "Chat", "MCQ"])
            notes_tab(tab1)
            chat_tab(tab2)
            get_json()
            mcq_tab(tab3)

if __name__ == "__main__":
    main()