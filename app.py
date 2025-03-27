#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import joblib
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS to allow frontend requests

# Load the trained model and preprocessors
try:
    model = joblib.load("best_model.pkl")
    scaler = joblib.load("scaler.pkl")
    encoder = joblib.load("encoder.pkl")
    print("Model and preprocessors loaded successfully!")
except Exception as e:
    print(f"Error loading model/preprocessors: {e}")

# Define expected numerical and categorical features
num_features = ["engine_size", "cylinders", "fuel_city", "fuel_hwy", "fuel_comb"]
cat_features = ["transmission", "fuel_type", "vehicle_class"]

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "CO2 Emission Prediction API is running!"})

@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "GET":
        # Provide a sample input format for users
        sample_input = {
            "message": "Use a POST request to get predictions.",
            "sample_input": {
                "engine_size": 2.5,
                "cylinders": 4,
                "fuel_city": 10,
                "fuel_hwy": 8,
                "fuel_comb": 9,
                "transmission": "AUTO",
                "fuel_type": "Gasoline",
                "vehicle_class": "SUV"
            }
        }
        return jsonify(sample_input), 200

    elif request.method == "POST":
        try:
            data = request.get_json()

            # Validate input data
            if not all(feature in data for feature in num_features + cat_features):
                return jsonify({"error": "Missing required features in input"}), 400

            # Convert input into a DataFrame
            input_df = pd.DataFrame([data])

            # Preprocess input data
            X_scaled = scaler.transform(input_df[num_features])
            X_encoded = encoder.transform(input_df[cat_features])
            X_processed = np.hstack((X_scaled, X_encoded))

            # Make prediction
            prediction = model.predict(X_processed)[0]
            
            return jsonify({"CO2 Emission Prediction": round(prediction, 2)})

        except Exception as e:
            return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)

