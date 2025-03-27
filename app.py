from flask import Flask, render_template, request, jsonify
import pickle
import os

app = Flask(__name__)

# Load model and preprocessing files
model_path = os.path.join(os.path.dirname(__file__), "best_model.pkl")
encoder_path = os.path.join(os.path.dirname(__file__), "encoder.pkl")
scaler_path = os.path.join(os.path.dirname(__file__), "scaler.pkl")

model = pickle.load(open(model_path, "rb"))
encoder = pickle.load(open(encoder_path, "rb"))
scaler = pickle.load(open(scaler_path, "rb"))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Extract input data from form
        engine_size = float(request.form['engine_size'])
        cylinders = int(request.form['cylinders'])
        fuel_city = float(request.form['fuel_city'])
        fuel_hwy = float(request.form['fuel_hwy'])
        fuel_comb = float(request.form['fuel_comb'])
        transmission = request.form['transmission']
        fuel_type = request.form['fuel_type']
        vehicle_class = request.form['vehicle_class']

        # Encode categorical variables
        encoded_transmission = encoder.transform([[transmission]])[0, 0]
        encoded_fuel_type = encoder.transform([[fuel_type]])[0, 0]
        encoded_vehicle_class = encoder.transform([[vehicle_class]])[0, 0]

        # Prepare input features
        input_data = [[engine_size, cylinders, fuel_city, fuel_hwy, fuel_comb,
                       encoded_transmission, encoded_fuel_type, encoded_vehicle_class]]

        # Scale the input
        input_data = scaler.transform(input_data)

        # Predict CO₂ emissions
        predicted_co2 = model.predict(input_data)[0]

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
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
