from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the CO2 Prediction API!"})

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Ensure data is sent as JSON
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['engine_size', 'cylinders', 'fuel_city', 'fuel_hwy', 'fuel_comb', 'transmission', 'fuel_type', 'vehicle_class']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required parameters"}), 400
        
        # Extract data
        engine_size = float(data['engine_size'])
        cylinders = int(data['cylinders'])
        fuel_city = float(data['fuel_city'])
        fuel_hwy = float(data['fuel_hwy'])
        fuel_comb = float(data['fuel_comb'])
        transmission = data['transmission']
        fuel_type = data['fuel_type']
        vehicle_class = data['vehicle_class']

        # Dummy prediction logic (Replace with actual model prediction)
        predicted_co2 = (engine_size * 20) + (cylinders * 5) + (fuel_comb * 10)

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

@app.route('/test', methods=['GET'])
def test():
    return jsonify({"message": "API is working!"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Use default port 10000
    app.run(host='0.0.0.0', port=port, debug=True)
