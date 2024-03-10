import streamlit as st
from tools.generate_text import generate_text
from tools.prompts import prompt, clean_text_prompt
from gtts import gTTS
import speech_recognition as sr
from io import BytesIO

recording_flag = True

def start_recording():
    global recording_flag
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        st.text("Recording... Speak now!")
        audio = recognizer.listen(source)

    try:
        # Check the recording flag before updating the session state
        if recording_flag:
            st.session_state.humans_debate_round = recognizer.recognize_google(audio)
        else:
            st.session_state.humans_debate_round = "Recording stopped."
    except sr.UnknownValueError:
        st.session_state.humans_debate_round = "Error: Could not understand audio."
    except sr.RequestError as e:
        st.session_state.humans_debate_round = f"Error: {e}"

def stop_recording():
    global recording_flag
    recording_flag = False

def read():
    if st.session_state.ai_debate_round:
        sound_file = BytesIO()
        tts = gTTS(text=st.session_state.ai_debate_round, lang='en')
        tts.write_to_fp(sound_file)
        st.audio(sound_file)

def clean_recorded_text():
    st.session_state.humans_debate_round = generate_text(clean_text_prompt(st.session_state.humans_debate_round))

def generate_debate_round(motion, debate_position):
    if st.session_state.humans_debate_round == "" and st.session_state.rounds_count != 0 and debate_position != "Proposition":
        st.session_state.ai_debate_round = "Error: there is no arguments to debate about"
        return
    st.session_state.ai_debate_round = generate_text(prompt=prompt(debate_position, st.session_state.rounds_count, motion), history=st.session_state.history)
    history = st.session_state.history
    if st.session_state.ai_debate_round:
        history.append({'role':'user','parts':st.session_state.humans_debate_round})
    else:
        history.append({'role':'user','parts':f"Let us debate about this motion: {motion}"})
    if st.session_state.ai_debate_round:
        history.append({'role':'model','parts':st.session_state.ai_debate_round})
    print(history)
    st.session_state.history = history


def next_round():
    st.session_state.rounds_count += 1
    st.session_state.humans_debate_round = ""
    st.session_state.ai_debate_round = ""

def new_debate():
    st.session_state.humans_debate_round = ""
    st.session_state.ai_debate_round = ""
    st.session_state.history = []

st.set_page_config(layout="wide", initial_sidebar_state="expanded")


if 'history' not in st.session_state:
    st.session_state.history = []

motion = st.sidebar.selectbox(options=[
    "This house believes that social media has done more harm than good.",
    "This house supports a universal basic income.",
    "This house believes that genetically modified organisms (GMOs) should be widely embraced in agriculture.",
    "This house believes that governments should prioritize space exploration over other public expenditures."
    ],
    label="The motion:"
    )
debate_position = st.sidebar.selectbox(options=["Proposition", "Opposition"], label="Your position is: ")

if 'rounds_count' not in st.session_state:
    st.session_state.rounds_count = 0


st.sidebar.button(label="Generate the debate round", on_click=lambda: generate_debate_round(motion, debate_position))
st.sidebar.button(label="Next round", on_click=next_round)
st.sidebar.button(label="New Debate", on_click=new_debate)


st.title("Artificial Intelligence Debater")
st.markdown("---")
st.subheader(f"Round Number {st.session_state.rounds_count + 1}")

opponent_debate_position = "Opposition" if debate_position == "Proposition" else "Proposition"

if 'humans_debate_round' not in st.session_state:
    st.session_state.humans_debate_round = ""
st.text_area(label=f"Arguments provided by the {opponent_debate_position} team:", value=st.session_state.humans_debate_round)
st.button(label="Start recording", on_click=start_recording)
st.button(label="Stop recording", on_click=stop_recording)
st.button(label="Clean recorded text", on_click=clean_recorded_text)

if 'ai_debate_round' not in st.session_state:
    st.session_state.ai_debate_round = ""
st.text_area(label="Generated debate round:", value=st.session_state.ai_debate_round)
st.button(label="Read", on_click=read)

