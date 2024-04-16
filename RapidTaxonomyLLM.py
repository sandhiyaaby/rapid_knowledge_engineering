import os

import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain_core.messages import HumanMessage, SystemMessage
from openai import AzureOpenAI
from openai import OpenAI
from Utilities import json_to_bullet_points, extract_json_from_text


# api_base = "https://derai-vision.openai.azure.com/"
# api_key = os.environ["OPENAI_AZURE_API_KEY"]
# model_v = "derai-gpt4-vision"
# model_t = "derai-gpt4-text-0613"

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# client_v = AzureOpenAI(
#     api_key=api_key,
#     api_version='2023-12-01-preview',
#     base_url=f"{api_base}openai/deployments/{model_v}/extensions",
# )
#
# client_t = AzureOpenAI(
#     api_key=api_key,
#     api_version='2023-10-01-preview',
#     azure_endpoint=f"{api_base}"
# )





# LLM calls------------------------------------------------


def stage1_knowledge_summary(knowledge, domain, usecase, system_message="", user_message=""):

    if(system_message==""):
        system_message = f"""You are an expert in {domain} and knowledge graph construction.
            """
    if(user_message==""):
        user_message = f"""  
      
        The following is a knowledge source that you must base your answer on:
        {knowledge}
        
        Recall your knowledge about {domain}. What knowledge can you gather from the above text regarding {usecase}.   
         
         Your output should be only your train of thought, written in unstructured, free-associative paragraphs.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=4000
        )
        # Extracting the content from gpt-4's response (which contains a bunch of other stuff)
        response1 = response.choices[0].message.content
        print(response1)
        # append_response_to_dataframe(style_and_furn)

    except Exception as e:
        print(e)
    return response1


def stage2_identify_categories(domain, usecase, stage1response, system_message="", user_message=""):
    if (system_message == ""):
        system_message = f"""You are an expert in {domain} and in generating a taxonomy for the purpose of {usecase}
                """
    if(user_message==""):
        user_message =  f""" 1. Read the content below, and recollect your general {domain} knowledge and determine the domain and its edges. In other words, figure out what concepts are included in this domain, and what are not. Also, understand the edge-cases to stress-test the borders of the domain that you establish, to confirm or adjust them.
    
    2. Identify all the possible "things" in this domain. What are ALL the possible, mutually-exclusive concepts that exist within the domain you've defined, and how can they be termed in a way that they are distinguishable, understandable and mutually-exclusive from a semantic perspective.
    
    3. Come up with consistent rules/logic for how you will subdivide into classes all the things you've identified in this domain. The logic of your subdividing approach should make sense for the nature of this particular domain.
    
    4. Following the logic/rules you've decided on, subdivide all the "things" in the domain into subclasses. Then repeat, dividing further into subclasses of that. And then subclasses of that. And so on, until you have reached the bottom of the taxonomy. Critically analyze the categories and subcategories you've identified. Make revisions to enhance clarity, coverage, and practical utility.
    
    5. Output your thinking for each of these steps.
    
    CONTENT:
    {stage1response}
    
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=4000
        )
        # Extracting the content from gpt-4's response (which contains a bunch of other stuff)
        response2 = response.choices[0].message.content
        print(response2)
        # append_response_to_dataframe(style_and_furn)

    except Exception as e:
        print(e)
    return response2


def stage3_make_taxonomy(domain, usecase, stage2response, system_message="", user_message=""):
    if(system_message==""):
        system_message = f"""You are an expert in {domain} and in generating a taxonomy for the purpose of {usecase} "
                """
    if(user_message==""):
        user_message = f"""  
    Below you will find the information to generate a taxonomy for {usecase}. Generate a taxonomomy with categories/concepts relevent specifically for {usecase}. Ensure the naming of the categories and subcategories are according to the naming conventions of taxonomies.
    
    Give the taxonomy in a JSON format. 
    CONTENT:
    {stage2response}
    
    ..
        """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ],
            response_format={"type": "json_object"},
            temperature=0.5,
            max_tokens=1000
        )
        # Extracting the content from gpt-4's response (which contains a bunch of other stuff)
        response3 = response.choices[0].message.content
        print(response3)
        # append_response_to_dataframe(style_and_furn)

    except Exception as e:
        print(e)
    return response3


def stage4_convert_JSON(stage3response):

    tax_json = extract_json_from_text(stage3response)
    print(tax_json)
    response4 = json_to_bullet_points(tax_json)

    return response4


