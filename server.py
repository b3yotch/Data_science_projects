from flask import Flask, request, jsonify
import util

app = Flask(__name__)
@app.route('/get_location_names', methods=['GET'])
def get_location_names():
    response = jsonify({
        'locations': util.get_location_names()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

@app.route('/predict_home_price', methods=['GET', 'POST'])
def predict_home_price():
    try:
        Area = float(request.form['Area'])
        Locality = request.form['Locality']
        BHK = int(request.form['BHK'])
        Bathroom = int(request.form['Bathroom'])
    except (KeyError, ValueError) as e:
        app.logger.error(f"Error processing form data: {e}")
        app.logger.error(f"Received form data: {request.form}")
        return jsonify({'error': 'Invalid form data'}), 400

    app.logger.info(f"Received form data: Area={Area}, Locality={Locality}, BHK={BHK}, Bathroom={Bathroom}")

    try:
        estimated_price = util.get_estimated_price(Locality, Area, BHK, Bathroom)
    except Exception as e:
        app.logger.error(f"Error getting estimated price: {e}")
        return jsonify({'error': 'Error occurred while processing the request'}), 500

    response = jsonify({
        'estimated_price': estimated_price
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# ... (other routes and code)
if __name__ == "__main__":
    print("Starting Python Flask Server For Home Price Prediction...")
    util.load_saved_artifacts()
    app.run()