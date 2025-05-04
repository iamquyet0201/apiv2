import requests

# Địa chỉ API (thay đổi nếu bạn chạy trên server thật)
url = "http://127.0.0.1:5000/predict"

# Dữ liệu đầu vào (1 dòng đầy đủ)
data = {
    "c": 30,         # Lực dính (kPa)
    "L": 55,         # Chiều dài mái dốc (m)
    "gamma": 19.5,   # Trọng lượng riêng đất (kN/m3)
    "h": 11.0,       # Chiều cao mái dốc (m)
    "u": 6.0,        # Áp lực nước lỗ rỗng (kPa)
    "phi": 28.0,     # Góc ma sát trong (độ)
    "beta": 20.0,    # Góc nghiêng mái dốc (độ)
    "FS": 2.35       # Hệ số an toàn
}

# Gửi POST request
response = requests.post(url, json=data)

# Hiển thị kết quả
if response.status_code == 200:
    result = response.json()
    print("🧠 Dự báo sạt lở:", result["prediction"])
else:
    print("❌ Lỗi:", response.text)
