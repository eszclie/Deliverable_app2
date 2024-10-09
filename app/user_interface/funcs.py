import json
import os

import requests
import streamlit as st
from dotenv import load_dotenv

from cyclical_encoding_new_inputs import extract_cyclical_features


@st.cache_resource
def bind_socket():
    # Load configuration from environment variables
    load_dotenv()
    scoring_uri = os.environ["score"]
    key = os.environ["key"]
    headers = {"Authorization": ("Bearer " + key)}
    return scoring_uri, headers


def get_response(in_data, h, score):
    # Display the selected dates and predicted rainfall
    input_encoded = extract_cyclical_features(in_data)
    input_dict = {"input_data": input_encoded.tolist()}

    # Send the POST request
    response = requests.post(score, json=input_dict, headers=h).text
    out = json.loads(response)
    return out


def set_page_confic():
    st.set_page_config(
        page_title="Deliverable App",
        page_icon="app/images/Deliverable_logo.png",
    )
