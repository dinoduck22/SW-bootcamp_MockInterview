import streamlit as st
import base64
from openai import OpenAI
# speech to text
from bokeh.models import CustomJS, Button
from streamlit_bokeh_events import streamlit_bokeh_events
# video
import cv2
import numpy as np
import tempfile

# 레이아웃
st.set_page_config(layout="wide")
# 초기화
if 'caption' not in st.session_state:  # 버튼 내용
    st.session_state.caption = ""

# Set OpenAI API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# AI response
question = "Hello, this is AI mock Interview."

# Initialize chat history
if 'messages' not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": question}]

# 자막 버튼
def caption():
    begin = st.container()
    st.text('')  # 줄바꿈
    col_buttonl, col_buttonr = st.columns([1, 1])  # 비율 col_buttonl : col_buttonr
    with col_buttonl:
        if st.button('caption'):
            begin.text("AI : " + st.session_state.messages[-1].get("content"))
            with col_buttonr:
                st.button('cancel')


# speech to text
def record():
    # speech to text
    stt_button = Button(label="Speak", width=100, align='center')

    stt_button.js_on_event("button_click", CustomJS(code="""
        
        var recognition = new webkitSpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = true;
        
        recognition.onresult = function(e) {
            var value = "";
            for (var i = e.resultIndex; i < e.results.length; ++i) {
                if (e.results[i].isFinal) {
                    value += e.results[i][0].transcript;
                }
            }
            if (value != "") {
                document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
            }
        }
        recognition.start();
        """))

    result = streamlit_bokeh_events(
        stt_button,
        events="GET_TEXT",
        key="listen",
        refresh_on_update=False,
        override_height=75,
        debounce_time=0)

    if result:
        if "GET_TEXT" in result:
            userinput = result.get("GET_TEXT")
            st.write(userinput)
            return userinput


# 사이드 바
def chat():
    userinput = record()
    if userinput is not None:
        prompt = userinput
        userinput = None
    st.sidebar.title("Chat Log")
    # Display chat history
    for messages in st.session_state.messages:
        with st.sidebar.chat_message(messages["role"]):
            st.markdown(messages["content"])
    # Chat Input & AI question
    if prompt := st.chat_input("Type in your answer"):
        st.session_state.messages.append({"role": "user", "content": prompt})  # Add to chat history
        with st.sidebar.chat_message("user"):
            st.markdown(prompt)  # Display user message
        with st.sidebar.chat_message("assistant"):  # Display assistant response in chat message container
            message_placeholder = st.empty()
            full_response = ""
        for response in client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                stream=True,
        ):
            full_response += (response.choices[0].delta.content or "")
            message_placeholder.markdown(full_response + " ")
        message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})


# AI 화면
def aivideo():
    video_file = open('jobinterview.mp4', 'rb')
    video_bytes = video_file.read()
    st.video(video_bytes)

# 사용자 화면
def uservideo():
    cap = cv2.VideoCapture(0)
    frame_placeholder = st.empty()
    stop_button_pressed = st.button("Stop")
    while cap.isOpened() and not stop_button_pressed:
        ret, frame = cap.read()

        if not ret:
            st.write("The video capture has ended.")
            break

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        frame_placeholder.image(frame, channels="RGB")

        if stop_button_pressed:
            break
    cap.release()


# 메인
def main():
    # 제목 및 내용
    st.title("AI mock interview")
    st.text("To start the mock Interview, answer the following question")
    # 사이드 바
    chat()
    # 버튼
    caption()
    # 화면
    col1, col2, col3 = st.columns([0.2, 1, 0.2])  # 비율 col1:col2:col3
    with col2:
        # AI 화면
        aivideo()
        # 사용자 화면
        uservideo()



if __name__ == '__main__':
    main()
