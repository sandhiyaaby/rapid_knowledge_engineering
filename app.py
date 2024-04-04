import os
from langchain_community.llms import OpenAI
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from io import StringIO

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
llm = OpenAI(temperature=0.3, max_tokens=4000)


print("I ran now")
st.title("Make a Taxonomy with an LLM")

# check if response1 is already stored in the session
if "response1" not in st.session_state:
    st.session_state.response1=""
    st.session_state.knowledge=""



domain_template = PromptTemplate(
    input_variables=['domain'],
    template=f"{st.session_state.knowledge} \n"+" Can you analyse the above text based on {domain} in order to use it for Knowledge Graph Construction for a home furnishing company.Your output should be only your train of thought, written in unstructured, free-associative paragraphs."

)


# Chains
domain_chain=LLMChain(llm=llm, prompt=domain_template, verbose=True)




uploaded_file = st.file_uploader("Choose a knowledge source file")
if uploaded_file is not None:
    # To convert to a string based IO:
    st.session_state.knowledge = StringIO(uploaded_file.getvalue().decode("utf-8"))


prompt1 = st.text_input("Name a domain")

if st.button("Gen1") and prompt1:
    st.session_state.response1 = domain_chain.run(domain=prompt1)
    st.write(st.session_state.response1)


if st.session_state.response1:
    st.write(st.session_state.response1)


prompt2=st.text_input("Second Prompt")

if st.button("Gen2") and prompt2:
    response2 = llm(st.session_state.response1 + "\n" + prompt2)
    st.write(st.json(response2))
    print(st.json(response2))


