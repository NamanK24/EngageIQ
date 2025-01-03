import streamlit as st
from flow_runner import run_flow
import json

st.title("EngageIQ: Social Media Analytics Module")
st.markdown(
    """
This is to analyze engagement data from mock social media accounts, leveraging LangFlow 
and DataStax Astra DB. The module will provide actionable insights into the performance of different types of 
social media posts (e.g., carousels, reels, and static images).

"""
)

endpoint = "3302a42e-83d3-4918-87e2-f15ed4b2240a"
application_token = "AstraCS:SQMDBBmkKicNitbfFeMpCWby:38d6ef33b0a5ea5fc693693727d338e2cba0c7fcfb041a87f3ccb3542e23fb2c"
output_type = "chat"
input_type = "chat"

message = st.text_area("Enter your message", placeholder="Type your message here...")

if st.button("Run Flow"):
    try:
        response = run_flow(
            message=message,
            endpoint=endpoint,
            output_type=output_type,
            input_type=input_type,
            application_token=application_token,
        )

        st.subheader("Response")
        if isinstance(response, dict):
            try:
                parsed_value = response["outputs"][0]["outputs"][0]["results"][
                    "message"
                ]["data"]["text"]
                st.write(parsed_value)

                if "visualization" in response["outputs"][0]["outputs"][0]["results"]:
                    visualization_data = response["outputs"][0]["outputs"][0][
                        "results"
                    ]["visualization"]
                    st.json(visualization_data)

            except KeyError:
                st.error("The expected key structure is missing in the response.")
        elif isinstance(response, str):
            st.write(response)
        else:
            st.error(
                "Unexpected response format. Check the API or tweaks configuration."
            )

    except json.JSONDecodeError:
        st.error("Invalid JSON in Tweaks")
    except Exception as e:
        st.error(f"Error: {e}")
