from flask import Flask, request, jsonify
import numpy as np
import joblib

# Load mô hình, scaler và encoder
model = joblib.load("mo_hinh_du_bao_sat_lo.pkl")
scaler = joblib.load("scaler.pkl")
label_encoder = joblib.load("label_encoder.pkl")

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Landslide Prediction API is running!"

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        # Kiểm tra đủ input
        required = ['c', 'L', 'gamma', 'h', 'u', 'phi', 'beta', 'FS']
        if not all(f in data for f in required):
            return jsonify({"error": f"Missing fields. Required: {required}"}), 400

        # Chuẩn hóa và dự đoán
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
