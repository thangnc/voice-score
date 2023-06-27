import os

import numpy as np
import noisereduce as nr
import openai
import yaml
import json
import whisper
import streamlit as st
from yaml.loader import SafeLoader
from openai import OpenAIError
from tempfile import NamedTemporaryFile
from json import JSONDecodeError

st.set_page_config(page_title="Voice score", layout="wide")

with open('./config.yml') as file:
    config = yaml.load(file, Loader=SafeLoader)

st.session_state["OPENAI_API_KEY"] = config["openai"]["api_key"]
if st.session_state["OPENAI_API_KEY"]:
    st.session_state["api_key_configured"] = True
else:
    st.session_state["api_key_configured"] = False


def clear_submit():
    st.session_state["submit"] = False


def intro():
    st.sidebar.success("Select a demo above.")

    st.header("Voice score")

    st.markdown(
        """
        ### How to use\n
        1. Upload sound files under mp3 format. Please use file with length less than 5min and size less than 1MB\n
        2. Receives extracted text and score by categories by OpenAI policy https://openai.com/policies/usage-policies.\n
        """
    )

    st.markdown(
        """
        ---
        ### Is my data safe? \n
        Yes, your data is safe. It does not store your sound files.
        All uploaded data is deleted after you close the browser tab.
        """
    )


def score_audio():
    st.header('Score an audio whether content complies with OpenAI\'s usage policies')

    with st.form("upload-form", clear_on_submit=True):
        uploaded_file = st.file_uploader(
            "Upload a mp3 file",
            type=["mp3"],
            help="Video files are not supported yet!"
        )
        upload_submitted = st.form_submit_button("Upload")

        if upload_submitted and uploaded_file is not None:
            if uploaded_file.name.endswith(".mp3"):
                if not st.session_state.get("api_key_configured"):
                    st.error("Please configure your OpenAI API key!")
                else:
                    with st.spinner("Uploading file and transcript... This may take a while⏳"):
                        try:
                            openai.api_key = st.session_state["OPENAI_API_KEY"]
                            transcript = openai.Audio.transcribe("whisper-1", uploaded_file, language="vi",
                                                                 temperature=0.2,
                                                                 prompt="The transcript is the conversation between the caller and the borrower who lend money")
                            st.markdown("#### Script")
                            st.markdown(f'{transcript["text"]}')

                            # model = whisper.load_model("base")
                            # with NamedTemporaryFile(suffix="mp3") as temp:
                            #     temp.write(uploaded_file.getvalue())
                            #     temp.seek(0)
                            #     temperature = 0.2
                            #     # decode_options = dict(beam_size=5, patience=2)
                            #     decode_options = dict()
                            #     transcript = model.transcribe(temp.name, verbose=True,
                            #                                   language="vi", fp16=True,
                            #                                   **decode_options)
                            #     # beam_size = 5
                            #     # best_of = None
                            #     # temperature = 0.0
                            #     #
                            #     # decode_options = dict(language="vi", best_of=best_of, beam_size=beam_size,
                            #     #                       temperature=temperature)
                            #     # transcribe_options = dict(task="transcribe", **decode_options)
                            #     #
                            #     # transcript = model.transcribe(temp.name, **transcribe_options)
                            #
                            #     st.markdown("#### Answer")
                            #     st.markdown(f'{transcript["text"]}')

                            response = openai.Moderation.create(input=transcript["text"])
                            st.markdown('#### Moderation')
                            st.json(f'{response["results"][0]["category_scores"]}')

                        except OpenAIError as e:
                            st.error(e.message)
            else:
                raise ValueError("File type not supported!")


page_names_to_funcs = {
    "—": intro,
    "Score an audio": score_audio,
    # "Chat with full content": chat_with_full_content,
}

demo_name = st.sidebar.selectbox("Choose a demo", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()
