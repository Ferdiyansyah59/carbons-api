from joblib import load
import numpy as np
import os
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import requests



filename = 'carbons.joblib'
model = load(filename)


def prediction(electriccity, gas, transportation, food, organic_waste, inorganic_waste, food_type):
    try:
        data = [
            ("Daging Sapi", 2),
            ("Daging Ayam", 1),
            ("Ikan", 3),
            ("Susu", 6),
            ("Telur", 7),
            ("Sayuran", 5),
            ("Buah", 0),
            ("Kacang", 4)
        ]
        for item in data:
            if food_type == item[0]:
                food_type =  item[1]
                input_data = np.array([[electriccity, gas, transportation, food, organic_waste, inorganic_waste, food_type]], dtype='object')
                prediction = model.predict(input_data)
                return prediction[0]
    except Exception as e:
        print(e)




app = Flask(__name__)
CORS(app)

@app.route('/carbons', methods=['POST'])
def sampah():
#     img_param = request.args.get('img')
    electriccity = request.form['electriccity']
    gas = request.form['gas']
    transportation = request.form['transportation']
    food = request.form['food']
    organic_waste = request.form['organic_waste']
    inorganic_waste = request.form['inorganic_waste']
    food_type = request.form['food_type']
    
    print(food_type)
    res = prediction(float(electriccity), float(gas), float(transportation), float(food), float(organic_waste), float(inorganic_waste), food_type)
    try:
        data = {
            'code': 200,
            'message': 'Berhasil memprediksi!',
            'prediksi': float(f"{res:.2f}")
        }
        
        return make_response(jsonify(data)), 200
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)

@app.route('/test', methods=['GET'])
def test():
    return 'Hallow ddd'

if __name__ == "__main__":
    app.run(port=int(os.environ.get("PORT", 8017)),host='0.0.0.0',debug=True)

