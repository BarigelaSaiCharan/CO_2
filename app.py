from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np

app = Flask(__name__)

# Load the trained model and preprocessing tools
model = pickle.load(open("best_model.pkl", "rb"))
encoder = pickle.load(open("encoder.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Extract data from form
        engine_size = float(request.form['engine_size'])
        cylinders = int(request.form['cylinders'])
        fuel_city = float(request.form['fuel_city'])
        fuel_hwy = float(request.form['fuel_hwy'])
        fuel_comb = float(request.form['fuel_comb'])
        transmission = request.form['transmission']
        fuel_type = request.form['fuel_type']
        vehicle_class = request.form['vehicle_class']

        # Encode categorical values
        transmission_encoded = encoder.transform([[transmission]])[0][0]
        fuel_type_encoded = encoder.transform([[fuel_type]])[0][0]
        vehicle_class_encoded = encoder.transform([[vehicle_class]])[0][0]

        # Prepare input for model
        features = np.array([[engine_size, cylinders, fuel_city, fuel_hwy, fuel_comb, 
                              transmission_encoded, fuel_type_encoded, vehicle_class_encoded]])
        features_scaled = scaler.transform(features)

        # Make prediction
        predicted_co2 = model.predict(features_scaled)[0]

        return jsonify({
            "engine_size": engine_size,
            "cylinders": cylinders,
            "fuel_city": fuel_city,
            "fuel_hwy": fuel_hwy,
            "fuel_comb": fuel_comb,
            "transmission": transmission,
            "fuel_type": fuel_type,
            "vehicle_class": vehicle_class,
            "predicted_CO2_emission": round(predicted_co2, 2)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
