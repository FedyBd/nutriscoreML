from flask import Flask, request, jsonify
import requests
import joblib
import json
app = Flask(__name__)

def parse_nutrition(data, item):
    for key, value in data.items():
        if key == item:
            return value
        elif isinstance(value, dict):
            result = parse_nutrition(value, item)
            if result is not None:
                return result
    return None


@app.route('/predict', methods=['GET'])
def predict():
    # Retrieve the barcode from the query parameter
    barcode = request.args.get('barcode')
    print(barcode)

    if barcode is None:
        return jsonify({'error': 'Barcode parameter is missing'}), 400
    api_url = 'https://world.openfoodfacts.org/api/v3/product/'
    url = api_url + barcode + '.json'

    # Send a GET request to the webpage
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Extract the JSON text from the webpage content
        json_text = response.text
        # Parse the JSON data
        parsed_data = json.loads(json_text)

        # Access the parent tag
        product_data0 = parsed_data['product']
        nutriments = parse_nutrition(product_data0, 'nutriments')
        if nutriments is not None:
            x1 = parse_nutrition(nutriments, 'energy-kcal_100g') if parse_nutrition(nutriments,
                                                                                    'energy_100g') is not None else 0
            x2 = parse_nutrition(nutriments, 'fat_100g') if parse_nutrition(nutriments, 'fat_100g') is not None else 0
            x3 = parse_nutrition(nutriments, 'saturated-fat_100g') if parse_nutrition(nutriments,
                                                                                      'saturated-fat_100g') is not None else 0
            x4 = parse_nutrition(nutriments, 'cholesterol_100g') if parse_nutrition(nutriments,
                                                                                    'cholesterol_100g') is not None else 0
            x5 = parse_nutrition(nutriments, 'carbohydrates_100g') if parse_nutrition(nutriments,
                                                                                      'carbohydrates_100g') is not None else 0
            x6 = parse_nutrition(nutriments, 'sugars_100g') if parse_nutrition(nutriments,
                                                                               'sugars_100g') is not None else 0
            x7 = parse_nutrition(nutriments, 'fiber_100g') if parse_nutrition(nutriments,
                                                                              'fiber_100g') is not None else 0
            x8 = parse_nutrition(nutriments, 'proteins_100g') if parse_nutrition(nutriments,
                                                                                 'proteins_100g') is not None else 0
            x9 = parse_nutrition(nutriments, 'salt_100g') if parse_nutrition(nutriments, 'salt_100g') is not None else 0
            x10 = parse_nutrition(nutriments, 'sodium_100g') if parse_nutrition(nutriments,
                                                                                'sodium_100g') is not None else 0
            x11 = parse_nutrition(nutriments, 'potassium_100g') if parse_nutrition(nutriments,
                                                                                   'potassium_100g') is not None else 0
            x12 = parse_nutrition(nutriments, 'chloride_100g') if parse_nutrition(nutriments,
                                                                                  'chloride_100g') is not None else 0
            x13 = parse_nutrition(nutriments, 'calcium_100g') if parse_nutrition(nutriments,
                                                                                 'calcium_100g') is not None else 0
            x14 = parse_nutrition(nutriments, 'iron_100g') if parse_nutrition(nutriments,
                                                                              'iron_100g') is not None else 0
            x15 = parse_nutrition(nutriments, 'magnesium_100g') if parse_nutrition(nutriments,
                                                                                   'magnesium_100g') is not None else 0
            x16 = parse_nutrition(nutriments, 'caffeine_100g') if parse_nutrition(nutriments,
                                                                                  'caffeine_100g') is not None else 0
            x17 = parse_nutrition(nutriments, 'fruits-vegetables-nuts_100g') if parse_nutrition(nutriments,
                                                                                                'fruits-vegetables-nuts_100g') is not None else 0
            x18 = parse_nutrition(nutriments, 'cocoa_100g') if parse_nutrition(nutriments,
                                                                               'cocoa_100g') is not None else 0

            example_data = [[x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13, x14, x15, x16, x17, x18]]
        else:
            return jsonify({'error': 'Nutriments not found'}), 400
    else:
        return jsonify({'error': 'Failed to fetch webpage', 'status_code': response.status_code}), 400

    # Load the joblib model
    model = joblib.load('xgboost_model18.joblib')

    # Make predictions using the loaded model
    predictions = model.predict(example_data)
    print(predictions)
    return jsonify({'predictions': predictions.tolist()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
