from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)

API_URL = "http://localhost:8000"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    features = [float(x) for x in request.form.values()]
    
    # Make API request to FastAPI service
    response = requests.post(
        f"{API_URL}/predict",
        json={"features": features}
    )
    
    prediction = response.json()['prediction']
    return render_template('index.html', prediction=prediction)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
