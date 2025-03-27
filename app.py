#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get form data
        engine_size = float(request.form['engine_size'])
        cylinders = int(request.form['cylinders'])
        fuel_city = float(request.form['fuel_city'])
        fuel_hwy = float(request.form['fuel_hwy'])
        fuel_comb = float(request.form['fuel_comb'])
        transmission = request.form['transmission']
        fuel_type = request.form['fuel_type']
        vehicle_class = request.form['vehicle_class']

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

if __name__ == '__main__':
    app.run(debug=True)

