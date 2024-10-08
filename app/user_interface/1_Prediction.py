import streamlit as st

import src.etl_neerslag.functions.get_average as avg
from app.user_interface.funcs import bind_socket, get_response, set_page_confic

# Set the name and icon of the page
set_page_confic()
# Set endpoint credentials
scoring_uri, headers = bind_socket()
# Parameters for the rainfall slider
min_value = 0
max_value = 500

st.title("Deliverable - Predict the number of orders")
st.write("This app provides a user interface for a prediction model for the orders of Deliverable.")

date = st.date_input("Choose a date to predict orders for")

if st.checkbox("I want to pass my own rainfall", value=False):
    if st.checkbox("Specify a number using an input box", value=False):
        rainfall = st.number_input("Give a number", min_value=min_value)
    else:
        rainfall = st.slider("Choose amount of rainfall in 10th mm", min_value=min_value, max_value=max_value)

    if rainfall == 0:
        st.write(":mostly_sunny: No rain")
    elif 0 < rainfall < 30:
        st.write(":rain_cloud: Small amount of rain")
    elif 30 <= rainfall <= 70:
        st.write(":rain_cloud::rain_cloud: Medium amount of rain")
    else:
        st.write(":rain_cloud::rain_cloud::rain_cloud: Heavy amount of rain")
    user_input = [[date, rainfall]]
else:
    avg_rainfall = avg.get_rainfall(date=date)
    user_input = [[date, avg_rainfall]]

# new_input = [["2024-09-27", 45], ["2024-09-28", 55]]

if st.button("Make prediction"):
    output_list = get_response(user_input, headers, scoring_uri)
    st.write(f"The predicted amount of orders is **{int(output_list[0])}**")

# Command to run streamlit: python -m streamlit run 'user_interface/1_Prediction.py'
