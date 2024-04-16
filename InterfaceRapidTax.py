import os
import time

import streamlit as st
from RapidTaxonomyLLM import stage2_identify_categories, stage1_knowledge_summary, stage3_make_taxonomy, stage4_convert_JSON

# set session state variables
if "response1" not in st.session_state:
    st.session_state.response1=""

if "response2" not in st.session_state:
    st.session_state.response2=""

if "response3" not in st.session_state:
    st.session_state.response3=""

if "response4" not in st.session_state:
    st.session_state.response4=""


if "knowledge" not in st.session_state:
    st.session_state.knowledge=""

if "use_case" not in st.session_state:
    st.session_state.use_case=""

if "domain" not in st.session_state:
    st.session_state.domain=""



st.markdown(
    """
    <style>
        body, html {
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
            background-color: #E7717D;
        }

        .container {
            max-width: 600px;
            margin: 50px auto;
            padding: 20px;
            background-color: #fff;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }

        h1 {
            color: #333;
            text-align: center;
        }

        input[type="text"] {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
        }

        .stButton > button {
            width: 100%;
            padding: 10px;
            background-color: #007bff;
            color: #fff;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }

        .stButton > button:hover {
            background-color: #0056b3;
        }
        

        #output {
            margin-top: 20px;
        }
    </style>

    """,
    unsafe_allow_html=True
)

st.title("Brainstorm Taxonomies with AI")

prog_bar=""

with st.container(border=True):
    st.session_state.domain = st.text_input("", placeholder="Describe the Domain")
    st.session_state.use_case = st.text_input("", placeholder="Describe the use-case")



    uploaded_file = st.file_uploader("")
    if uploaded_file is not None:
        # To convert to a string based IO:
        st.session_state.knowledge = uploaded_file.read()
        print(st.session_state.knowledge)


    if st.button("Generate"):
        progress_text1 = ("AI is reading Knowledge Source, Please Wait.")
        prog_bar = st.progress(0.25, text=progress_text1)

        res1 = stage1_knowledge_summary(st.session_state.knowledge, st.session_state.domain, st.session_state.use_case)

        progress_text2 = (f"Identifying Categories for the {st.session_state.use_case}")
        prog_bar.progress(0.5, text=progress_text2)

        res2 = stage2_identify_categories(st.session_state.domain, st.session_state.use_case, res1)

        progress_text3 = ("Generating the Taxonomy")
        prog_bar.progress(0.75, text=progress_text3)

        res3 = stage3_make_taxonomy(st.session_state.domain, st.session_state.use_case, res2)

        prog_bar.progress(0.75, text=progress_text3)
        st.session_state.response4 = stage4_convert_JSON(res3)

        prog_bar.progress(1, text=progress_text3)
        time.sleep(1)
        prog_bar.empty()


if(st.session_state.response4):
    with st.container(border=True):
        st.text(st.session_state.response4)
        print(st.session_state.response4)
