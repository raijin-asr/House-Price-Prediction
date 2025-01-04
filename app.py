from flask import Flask, render_template, request
import numpy as np
import pickle

# Initialize Flask app
app = Flask(__name__)

# Load the trained model
try:
    model = pickle.load(open('model.pkl', 'rb'))
except FileNotFoundError:
    raise FileNotFoundError("Model file 'model.pkl' not found. Train and save the model first.")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get input values from the form
        bedrooms = float(request.form['bedrooms'])
        bathrooms = float(request.form['bathrooms'])
        floors = float(request.form['floors'])
        yr_built = float(request.form['yr_built'])

        # Prepare the input array for prediction
        features = np.array([[bedrooms, bathrooms, floors, yr_built]])

        # Predict the house price
        prediction = model.predict(features)

        # Return the prediction to the HTML template
        return render_template('index.html', data=f"Rs.{int(prediction[0]):,}")
    except Exception as e:
        # Handle errors gracefully
        return render_template('index.html', data=f"Error: {str(e)}")


if __name__ == '__main__':
    app.run(debug=True)
