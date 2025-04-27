from flask import Flask, request, jsonify, render_template
import math
import requests

app = Flask(__name__)

CURRENCY_API = "https://api.exchangerate.host/convert"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    expression = data['expression']
    mode = data['mode']

    try:
        allowed = {'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
                   'sqrt': math.sqrt, 'log': math.log, 'pi': math.pi,
                   'pow': math.pow, 'abs': abs, 'exp': math.exp, 'pow': pow}
        if mode == 'deg':
            allowed.update({'radians': math.radians})
            expression = expression.replace('sin', 'sin(radians').replace('cos', 'cos(radians').replace('tan', 'tan(radians')
        result = eval(expression, {"__builtins__": None}, allowed)
    except Exception as e:
        result = f"Error: {str(e)}"

    return jsonify({'result': result})

@app.route('/convert', methods=['POST'])
def convert_units():
    data = request.get_json()
    value = float(data['value'])
    from_unit = data['from_unit']
    to_unit = data['to_unit']
    category = data['category']

    conversion_factors = {
        'length': {
            'meter': 1, 'kilometer': 1000, 'centimeter': 0.01, 'millimeter': 0.001,
            'mile': 1609.34, 'yard': 0.9144, 'foot': 0.3048, 'inch': 0.0254
        },
        'weight': {
            'kilogram': 1, 'gram': 0.001, 'milligram': 0.000001,
            'pound': 0.453592, 'ounce': 0.0283495
        },
        'area': {
            'sq_meter': 1, 'sq_kilometer': 1e6, 'sq_centimeter': 0.0001,
            'sq_millimeter': 0.000001, 'sq_mile': 2.59e6,
            'sq_yard': 0.836127, 'sq_foot': 0.092903, 'sq_inch': 0.00064516
        },
        'volume': {
            'cubic_meter': 1, 'liter': 0.001, 'milliliter': 0.000001,
            'cubic_inch': 1.6387e-5, 'cubic_foot': 0.0283168, 'gallon': 0.00378541
        }
    }

    try:
        factor_from = conversion_factors[category][from_unit]
        factor_to = conversion_factors[category][to_unit]
        base_value = value * factor_from
        result = base_value / factor_to
    except Exception as e:
        result = f"Error: {str(e)}"

    return jsonify({'result': result})

@app.route('/currency', methods=['POST'])
def currency_convert():
    data = request.get_json()
    amount = float(data['amount'])
    from_currency = data['from_currency']
    to_currency = data['to_currency']

    try:
        response = requests.get(f"{CURRENCY_API}?from={from_currency}&to={to_currency}&amount={amount}")
        result = response.json()['result']
    except Exception as e:
        result = f"Error: {str(e)}"

    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
