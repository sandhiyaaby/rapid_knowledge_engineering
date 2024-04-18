import os
import sys

import streamlit as st
from openai import OpenAI
from io import StringIO
sys.path.insert(1, os.getcwd())
from RapidTaxonomyLLM import stage2_identify_categories, stage1_knowledge_summary, stage3_make_taxonomy, stage4_convert_JSON


client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


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

st.title("Rapid Taxonomy (Explained)")

st.markdown(
    """
    <style>
        [data-testid="stAppViewContainer"]{
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
            background-color: #eeeeee;
        }
        
        [data-testid="stHeader"]{
            background-color: #eeeeee;
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

        input[type="text"]{
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



with st.container(border=True):
    st.session_state.domain = st.text_input("", placeholder="Describe the Domain")
    st.session_state.use_case = st.text_input("", placeholder="Describe the use-case")


    uploaded_file = st.file_uploader("")
    if uploaded_file is not None:
        # To convert to a string based IO:
        st.session_state.knowledge = uploaded_file.read()

    # ------------------------------------------------------------------------

systemmessage1 = f"""You are an expert in {st.session_state.domain} and knowledge graph construction."""
usermessage1= f"""  Below is a knowledge source that you must base your answer on. 
    Recall your knowledge about {st.session_state.domain}. 
    What knowledge can you gather from the above text regarding {st.session_state.use_case}?
    Your output should be only your train of thought, written in unstructured, free-associative paragraphs.
  KNOWLEDGE SOURCE:
  {st.session_state.knowledge}
"""

with st.container(border=True):
    sm1=st.text_input("Prompt 1 System Message", value=systemmessage1)
    um1=st.text_area("Prompt 1 User Message", value=usermessage1)
    if st.button("Stage 1"):
        st.session_state.response1 = stage1_knowledge_summary(st.session_state.knowledge, st.session_state.domain, st.session_state.use_case, sm1, um1)
        st.write(st.session_state.response1)


# ------------------------------------------------------------------------

  # ------------------------------------------------------------------------

systemmessage2 = f"""You are an expert in {st.session_state.domain} and in generating a taxonomy for the purpose of {st.session_state.use_case}
            """
usermessage2= f""" 1. Read the content below, and recollect your general {st.session_state.domain} knowledge and determine the domain and its edges. In other words, figure out what concepts are included in this domain, and what are not. Also, understand the edge-cases to stress-test the borders of the domain that you establish, to confirm or adjust them.
2. Identify all the possible "things" in this domain. What are ALL the possible, mutually-exclusive concepts that exist within the domain you've defined, and how can they be termed in a way that they are distinguishable, understandable and mutually-exclusive from a semantic perspective.
3. Come up with consistent rules/logic for how you will subdivide into classes all the things you've identified in this domain. The logic of your subdividing approach should make sense for the nature of this particular domain.
4. Following the logic/rules you've decided on, subdivide all the "things" in the domain into subclasses. Then repeat, dividing further into subclasses of that. And then subclasses of that. And so on, until you have reached the bottom of the taxonomy. Critically analyze the categories and subcategories you've identified. Make revisions to enhance clarity, coverage, and practical utility.
5. Output your thinking for each of these steps.

CONTENT:
{st.session_state.response1}
"""

with st.container(border=True):
    sm2=st.text_input("Prompt2 System Message", value=systemmessage2)
    um2=st.text_area("Prompt 2 User Message", value=usermessage2)
    if st.button("Stage 2"):
        st.session_state.response2 = stage2_identify_categories(st.session_state.domain, st.session_state.use_case, st.session_state.response1, sm2, um2)
        st.write(st.session_state.response2)

# ------------------------------------------------------------------------

  # ------------------------------------------------------------------------

systemmessage3=f"""You are an expert in {st.session_state.domain} and in generating a taxonomy for the purpose of {st.session_state.use_case} "
            """

usermessage3= f""" 
Below you will find the information to generate a taxonomy for {st.session_state.use_case}. 
Generate a taxonomomy with categories/conceots relevent specifically for {st.session_state.use_case}. Ensure the naming of the categories and subcategories are according to the naming conventions of taxonomies.
Give the taxonomy in a JSON format. 
CONTENT:
{st.session_state.response2}
"""

with st.container(border=True):
    sm3=st.text_input("Prompt 3 System Message", value=systemmessage3)
    um3=st.text_area("Prompt 3 User Message", value=usermessage3)
    if st.button("Stage 3"):
        st.session_state.response3 = stage3_make_taxonomy(st.session_state.domain, st.session_state.use_case, st.session_state.response2, sm3, um3)
        st.write(st.session_state.response3)

# ------------------------------------------------------------------------
# ------------------------------------------------------------------------

with st.container(border=True):
    if st.button("Stage 4 - Format Taxonomy"):
        st.session_state.response4 = stage4_convert_JSON(st.session_state.response3)
        st.text(st.session_state.response4)

# ------------------------------------------------------------------------




