# app.py

from flask import Flask, render_template, request, jsonify
import math
import requests

app = Flask(__name__)

# ---------- Scientific Calculator Logic ----------
def scientific_calculation(expression, mode):
    try:
        expression = expression.replace('^', '**')
        if mode == "deg":
            expression = expression.replace("sin", "math.sin(math.radians")
            expression = expression.replace("cos", "math.cos(math.radians")
            expression = expression.replace("tan", "math.tan(math.radians")
        else:
            expression = expression.replace("sin", "math.sin")
            expression = expression.replace("cos", "math.cos")
            expression = expression.replace("tan", "math.tan")
        expression = expression.replace("log", "math.log10")
        expression = expression.replace("ln", "math.log")
        result = eval(expression + (')' * expression.count('(')))
        return result
    except Exception as e:
        return str(e)

# ---------- Unit Conversion Logic ----------
unit_factors = {
    'length': {'meter': 1, 'kilometer': 1000, 'centimeter': 0.01, 'millimeter': 0.001, 'mile': 1609.34, 'yard': 0.9144, 'foot': 0.3048, 'inch': 0.0254},
    'weight': {'kilogram': 1, 'gram': 0.001, 'milligram': 1e-6, 'pound': 0.453592, 'ounce': 0.0283495},
    'area': {'sq_meter': 1, 'sq_kilometer': 1e6, 'sq_centimeter': 0.0001, 'sq_millimeter': 1e-6, 'sq_mile': 2.59e+6, 'sq_yard': 0.836127, 'sq_foot': 0.092903, 'sq_inch': 0.00064516},
    'volume': {'cubic_meter': 1, 'liter': 0.001, 'milliliter': 1e-6, 'cubic_inch': 1.6387e-5, 'cubic_foot': 0.0283168, 'gallon': 0.00378541},
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    expression = data.get('expression')
    mode = data.get('mode', 'deg')
    result = scientific_calculation(expression, mode)
    return jsonify({'result': result})

@app.route('/convert', methods=['POST'])
def convert():
    data = request.get_json()
    value = float(data.get('value'))
    from_unit = data.get('from_unit')
    to_unit = data.get('to_unit')
    category = data.get('category')

    try:
        base_value = value * unit_factors[category][from_unit]
        converted_value = base_value / unit_factors[category][to_unit]
        return jsonify({'result': converted_value})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/currency', methods=['POST'])
def currency():
    data = request.get_json()
    from_curr = data.get('from_currency')
    to_curr = data.get('to_currency')
    amount = data.get('amount')

    try:
        url = f"https://api.frankfurter.app/latest?amount={amount}&from={from_curr}&to={to_curr}"
        response = requests.get(url)
        result = response.json()
        converted_amount = result['rates'][to_curr]
        return jsonify({'result': converted_amount})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
