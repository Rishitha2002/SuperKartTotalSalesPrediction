

import os
import joblib
import pandas as pd
from flask import Flask, request, jsonify


# ---------------------------------------------------------
# Initialize Flask application
# ---------------------------------------------------------

superkart_total_sales_predictor_api = Flask(
    "SuperKart Total Sales Predictor"
)


# ---------------------------------------------------------
# Load trained model
# ---------------------------------------------------------

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "superkart-total-sales-prediction.joblib"
)

model = joblib.load(MODEL_PATH)


# ---------------------------------------------------------
# Home endpoint
# ---------------------------------------------------------

@superkart_total_sales_predictor_api.get("/")
def home():
    return jsonify({
        "message": "Welcome to the SuperKart Total Sales Prediction API!"
    })


# ---------------------------------------------------------
# Single prediction endpoint
# ---------------------------------------------------------

@superkart_total_sales_predictor_api.post("/v1/totalsales")
def predict_total_sales():

    try:
        # Get JSON request body
        product_data = request.get_json()

        if not product_data:
            return jsonify({
                "error": "No JSON data provided"
            }), 400

        # Expected features
        required_features = [
            "Product_Weight",
            "Product_Sugar_Content",
            "Product_Allocated_Area",
            "Product_Type",
            "Product_MRP",
            "Store_Id",
            "Store_Establishment_Year",
            "Store_Size",
            "Store_Location_City_Type",
            "Store_Type"
        ]

        # Check for missing features
        missing_features = [
            feature
            for feature in required_features
            if feature not in product_data
        ]

        if missing_features:
            return jsonify({
                "error": "Missing required features",
                "missing_features": missing_features
            }), 400

        # Create DataFrame
        input_data = pd.DataFrame(
            [product_data],
            columns=required_features
        )

        # Make prediction
        predicted_sales = model.predict(input_data)[0]

        # Convert NumPy value to Python float
        predicted_sales = round(float(predicted_sales), 2)

        return jsonify({
            "Predicted total sales": predicted_sales
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# ---------------------------------------------------------
# Batch prediction endpoint
# ---------------------------------------------------------

@superkart_total_sales_predictor_api.post("/v1/totalsalesbatch")
def predict_total_sales_batch():

    try:

        # Check whether file was uploaded
        if "file" not in request.files:
            return jsonify({
                "error": "No CSV file uploaded"
            }), 400

        file = request.files["file"]

        # Read CSV
        input_data = pd.read_csv(file)

        required_features = [
            "Product_Weight",
            "Product_Sugar_Content",
            "Product_Allocated_Area",
            "Product_Type",
            "Product_MRP",
            "Store_Id",
            "Store_Establishment_Year",
            "Store_Size",
            "Store_Location_City_Type",
            "Store_Type"
        ]

        # Check required columns
        missing_features = [
            feature
            for feature in required_features
            if feature not in input_data.columns
        ]

        if missing_features:
            return jsonify({
                "error": "Missing required columns",
                "missing_columns": missing_features
            }), 400

        # Make predictions
        predicted_sales = model.predict(
            input_data[required_features]
        )

        # Add predictions to dataframe
        input_data["Predicted_Total_Sales"] = predicted_sales

        # Return results
        return jsonify(
            input_data.to_dict(orient="records")
        )

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# ---------------------------------------------------------
# Run application
# ---------------------------------------------------------

if __name__ == "__main__":

    superkart_total_sales_predictor_api.run(
        host="0.0.0.0",
        port=7860,
        debug=False
    )
