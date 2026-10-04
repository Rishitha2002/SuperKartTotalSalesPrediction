import streamlit as st
import pandas as pd
import requests
import os


# ---------------------------------------------------------
# Backend configuration
# ---------------------------------------------------------

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:7860")


# ---------------------------------------------------------
# Page configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="SuperKart Total Sales Prediction",
    page_icon="🛒",
    layout="centered"
)

st.title("🛒 SuperKart Total Sales Prediction")


# =========================================================
# ONLINE PREDICTION
# =========================================================

st.subheader("Online Prediction")


# ---------------------------------------------------------
# Product features
# ---------------------------------------------------------

product_weight = st.number_input(
    "Product Weight",
    min_value=0.0,
    value=10.0,
    step=0.1
)

product_sugar_content = st.selectbox(
    "Product Sugar Content",
    [
        "Low Sugar",
        "Regular",
        "No Sugar"
    ]
)

product_allocated_area = st.number_input(
    "Product Allocated Area",
    min_value=0.0,
    max_value=1.0,
    value=0.10,
    step=0.01
)

product_type = st.selectbox(
    "Product Type",
    [
        "Meat",
        "Snack Foods",
        "Hard Drinks",
        "Dairy",
        "Canned",
        "Soft Drinks",
        "Health and Hygiene",
        "Baking Goods",
        "Bread",
        "Breakfast",
        "Frozen Foods",
        "Fruits and Vegetables",
        "Household",
        "Seafood",
        "Starchy Foods",
        "Others"
    ]
)

product_mrp = st.number_input(
    "Product MRP",
    min_value=0.0,
    value=100.0,
    step=1.0
)


# ---------------------------------------------------------
# Store features
# ---------------------------------------------------------

store_id = st.selectbox(
    "Store ID",
    [
        "OUT001",
        "OUT002",
        "OUT003",
        "OUT004"
    ]
)

store_establishment_year = st.number_input(
    "Store Establishment Year",
    min_value=1900,
    max_value=2026,
    value=2000,
    step=1
)

store_size = st.selectbox(
    "Store Size",
    [
        "Small",
        "Medium",
        "High"
    ]
)

store_location_city_type = st.selectbox(
    "Store Location City Type",
    [
        "Tier 1",
        "Tier 2",
        "Tier 3"
    ]
)

store_type = st.selectbox(
    "Store Type",
    [
        "Departmental Store",
        "Supermarket Type 1",
        "Supermarket Type 2",
        "Food Mart"
    ]
)


# ---------------------------------------------------------
# Create input dataframe
# ---------------------------------------------------------

input_data = pd.DataFrame({
    "Product_Weight": [product_weight],
    "Product_Sugar_Content": [product_sugar_content],
    "Product_Allocated_Area": [product_allocated_area],
    "Product_Type": [product_type],
    "Product_MRP": [product_mrp],
    "Store_Id": [store_id],
    "Store_Establishment_Year": [store_establishment_year],
    "Store_Size": [store_size],
    "Store_Location_City_Type": [store_location_city_type],
    "Store_Type": [store_type]
})


# ---------------------------------------------------------
# Predict
# ---------------------------------------------------------

if st.button("Predict Sales", type="primary"):

    try:

        response = requests.post(
            f"{BACKEND_URL}/v1/totalsales",
            json=input_data.to_dict(orient="records")[0],
            timeout=30
        )

        if response.status_code == 200:

            prediction = response.json()["Predicted total sales"]

            st.success(
                f"Predicted Total Sales: ₹{prediction:,.2f}"
            )

        else:

            error_message = response.json().get(
                "error",
                "Unknown error"
            )

            st.error(
                f"Prediction failed: {error_message}"
            )

    except requests.exceptions.RequestException as e:

        st.error(
            f"Unable to connect to prediction API: {e}"
        )


# =========================================================
# BATCH PREDICTION
# =========================================================

st.subheader("Batch Prediction")


uploaded_file = st.file_uploader(
    "Upload CSV file for batch prediction",
    type=["csv"]
)


if uploaded_file is not None:

    if st.button("Predict Batch", type="primary"):

        try:

            response = requests.post(
                f"{BACKEND_URL}/v1/totalsalesbatch",
                files={
                    "file": uploaded_file
                },
                timeout=60
            )

            if response.status_code == 200:

                predictions = response.json()

                st.success(
                    "Batch predictions completed!"
                )

                result_df = pd.DataFrame(predictions)

                st.dataframe(
                    result_df,
                    use_container_width=True
                )

                # Download predictions
                csv = result_df.to_csv(index=False)

                st.download_button(
                    label="Download Predictions",
                    data=csv,
                    file_name="superkart_predictions.csv",
                    mime="text/csv"
                )

            else:

                error_message = response.json().get(
                    "error",
                    "Unknown error"
                )

                st.error(
                    f"Batch prediction failed: {error_message}"
                )

        except requests.exceptions.RequestException as e:

            st.error(
                f"Unable to connect to prediction API: {e}"
            )
