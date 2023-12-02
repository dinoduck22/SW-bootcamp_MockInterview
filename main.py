import streamlit as st
from openai import OpenAI
# speech to text
from bokeh.models import CustomJS, Button, Toggle
from streamlit_bokeh_events import streamlit_bokeh_events
# video
from streamlit_webrtc import WebRtcMode, webrtc_streamer
from streamlit_float import *
# AI
from face_AI import faceanima
# chat LLM
from qa_vectordb import reply
# float
from streamlit_float import *


# 레이아웃
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

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
    with st.chat_message("assistant"):
        st.markdown(st.session_state.messages[-1].get("content"))



# TTS from AI
def tts():
    tts_button = Button(label="Speak AI", width=100)
    tts_button.js_on_event("button_click", CustomJS(code=f"""
                var u = new SpeechSynthesisUtterance();
                u.text = "{st.session_state.messages[-1].get("content")}";
                u.lang = 'en-US';

                speechSynthesis.speak(u);
                """))
    st.bokeh_chart(tts_button)


# speech to text
def record():
    # speech to text
    stt_button = Button(label="Voice Input", width=100, align='center')

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
        override_height=40,
        debounce_time=0)

    if result:
        if "GET_TEXT" in result:
            userinput = result.get("GET_TEXT")
            with st.chat_message("user"):
                st.write(userinput)
            return userinput


# 사이드 바
def chatlog():
    st.sidebar.title("Chat Log")

    # Display chat history
    for messages in st.session_state.messages:
        with st.sidebar.chat_message(messages["role"]):
            st.markdown(messages["content"])
    # recording & AI speaking
    tts()  # AI tts
    userinput = record()  # user recording
    # Chat Input & AI question
    query = st.chat_input("Type in your answer")
    if userinput is not None:
        response(userinput)
    if query:
        response(query)
    userinput = None


# AI chat response
def response(query):
    st.session_state.messages.append({"role": "user", "content": query})  # Add to chat history
    with st.sidebar.chat_message("user"):
        st.markdown(query)  # Display user message
    with st.sidebar.chat_message("assistant"):  # Display assistant response in chat message container
        message_placeholder = st.empty()
        full_response = reply(query)  # LLM
        message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})


# AI 화면
def aivideo():
    faceanima()


# 사용자 화면
def uservideo():
    webrtc_ctx = webrtc_streamer(
        key="object-detection",
        mode=WebRtcMode.SENDRECV,
        media_stream_constraints={"video": True, "audio": False},
        async_processing=True,
    )


def floating():
    # Float feature initialization
    float_init()

    # Initialize session variable that will open/close dialog
    if "show" not in st.session_state:
        st.session_state.show = False


    # Container with expand/collapse button
    button_container = st.container()
    with button_container:
        if st.session_state.show:
            if st.button("⭳", type="primary"):
                st.session_state.show = False
                st.experimental_rerun()
        else:
            if st.button("⭱", type="secondary"):
                st.session_state.show = True
                st.experimental_rerun()

    # Alter CSS based on expand/collapse state
    if st.session_state.show:
        vid_y_pos = "2rem"
        button_b_pos = "21rem"
    else:
        vid_y_pos = "-19.5rem"
        button_b_pos = "1rem"

    button_css = float_css_helper(width="2.2rem", right="2rem", bottom=button_b_pos, transition=0)

    # Float button container
    button_container.float(button_css)

    # Add Float Box
    float_box(
        '<iframe width="100%" height="100%" src="https://www.youtube.com/embed/J8TgKxomS2g?si=Ir_bq_E5e9jHAEFw" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>',
        width="29rem", right="2rem", bottom=vid_y_pos,
        css="padding: 0;transition-property: all;transition-duration: .5s;transition-timing-function: cubic-bezier(0, 1, 0.5, 1);",
        shadow=12)


# 메인
def main():
    # 화면
    col1, col2, col3 = st.columns([0.2, 1, 0.2])  # 비율 col1:col2:col3
    with col2:
        # AI 화면
        aivideo()
    # 사용자 화면
    floating()
    # AI 자막
    caption()
    # 사이드 바
    chatlog()


if __name__ == '__main__':
    main()
