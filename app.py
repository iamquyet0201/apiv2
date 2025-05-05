from flask import Flask, request, jsonify
from flask_cors import CORS  # 👈 Thêm dòng này
import numpy as np
import joblib

app = Flask(__name__)
CORS(app)  # 👈 Cho phép tất cả origin truy cập

# Load mô hình và scaler như cũ
model = joblib.load("mo.pkl")
scaler = joblib.load("scaler.pkl")
label_encoder = joblib.load("label_encoder.pkl")

@app.route("/")
def home():
    return "✅ Landslide Prediction API is running!"

@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "GET":
        return jsonify({"message": "Use POST method."})

    try:
        data = request.get_json()
        print("Received data:", data)

        required = ['c', 'L', 'gamma', 'h', 'u', 'phi', 'beta', 'FS']
        if not all(f in data for f in required):
            return jsonify({"error": f"Missing fields. Required: {required}"}), 400

        input_data = np.array([data[f] for f in required]).reshape(1, -1)
        scaled_input = scaler.transform(input_data)
        prediction = model.predict(scaled_input)[0]
        label = label_encoder.inverse_transform([prediction])[0]

        return jsonify({
            "prediction": label,
            "label_index": int(prediction)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
