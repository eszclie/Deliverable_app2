from datetime import datetime, timedelta

import pandas as pd
import plotly.express as px
import streamlit as st

import src.etl_neerslag.functions.get_average as avg
from app.user_interface.funcs import bind_socket, get_response, set_page_confic

# Set the name and icon of the page
set_page_confic()
# Set endpoint credentials
scoring_uri, headers = bind_socket()

st.title("Deliverable - Predict the number of orders")
st.write("This app provides a user interface for a prediction model for the orders of Deliverable.")

st.markdown("""
### Prediction for the coming months
""")

# Define the start and end of the slider range
start_date = datetime.now().date()
end_date = start_date + timedelta(days=90)

# Add a date range slider in Streamlit
date_range = st.slider(
    "Select a date range",
    min_value=start_date,
    max_value=end_date,
    value=(start_date, end_date),
    format="YYYY-MM-DD",
)
option = st.selectbox("Output choices", ("Graph", "Table"))

# if st.button("Make prediction for a given period"):
selected_dates = [date_range[0] + timedelta(days=i) for i in range((date_range[1] - date_range[0]).days + 1)]

# Create input data with dates and predicted rainfall
input_data = [[str(date), avg.get_rainfall(date=date)] for date in selected_dates]

out = get_response(input_data, headers, scoring_uri)
output_list = list(map(int, out))

if option == "Table":
    # Create a table
    df = pd.DataFrame(columns=["Date", "Weekday", "Predicted number of orders"])
    df["Date"] = selected_dates
    df["Weekday"] = [dt.strftime("%A") for dt in selected_dates]
    df["Predicted number of orders"] = output_list
    st.dataframe(
        df,
        column_config={
            "Date": st.column_config.Column(width="medium"),
            "Weekday": st.column_config.Column(width="medium"),
            "Predicted number of orders": st.column_config.Column(width="medium"),
        },
    )
else:  # option == "Graph"
    # Create a figure
    fig = px.line(
        x=selected_dates, y=output_list, title="Prediction of orders for a given period", markers=True
    )
    fig.update_layout(xaxis_title="Date", yaxis_title="Orders")
    st.plotly_chart(fig)
