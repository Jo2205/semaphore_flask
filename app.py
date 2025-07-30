# app.py - Flask backend API untuk prediksi pose secara real-time
from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
from tensorflow.keras.models import load_model
import base64
import cv2
import mediapipe as mp
from io import BytesIO
from PIL import Image
import logging

# Inisialisasi logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inisialisasi Flask
app = Flask(__name__)
CORS(app)  # Allow cross-origin untuk frontend React di localhost:3000

# Load model dan label
try:
    model = load_model("cnn_baru.h5")
    label_map = np.load("label_baru.npy", allow_pickle=True)
    logger.info("✅ Model dan label classes berhasil dimuat")
except Exception as e:
    logger.error(f"❌ Gagal memuat model atau label: {str(e)}")
    raise

# Inisialisasi MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5)

def preprocess_image(image_b64):
    try:
        # Decode base64 image
        header, encoded = image_b64.split(',', 1)
        img_bytes = base64.b64decode(encoded)
        img = Image.open(BytesIO(img_bytes)).convert('RGB')
        img_np = np.array(img)

        # Konversi ke format yang kompatibel dengan MediaPipe (BGR)
        img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

        # Proses gambar dengan MediaPipe Pose
        results = pose.process(img_bgr)
        if not results.pose_landmarks:
            logger.warning("⚠️ Tidak ada pose yang terdeteksi")
            return None

        # Ekstrak 33 landmarks (x, y, z, visibility) = 132 elemen
        keypoints = []
        for landmark in results.pose_landmarks.landmark:
            keypoints.extend([landmark.x, landmark.y, landmark.z, landmark.visibility])

        # Pastikan panjang keypoints adalah 132
        if len(keypoints) != 132:
            logger.error(f"❌ Jumlah keypoints tidak valid: {len(keypoints)}")
            return None

        return keypoints
    except Exception as e:
        logger.error(f"❌ Error saat preprocessing gambar: {str(e)}")
        return None

@app.route("/")
def index():
    return "✅ Backend pose prediction API aktif!"

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        keypoints = data.get("keypoints")
        image_b64 = data.get("image")

        if keypoints is not None:
            # Proses input keypoints langsung
            if len(keypoints) != 132:
                logger.error("❌ Keypoints tidak valid, harus 132 elemen")
                return jsonify({"error": "Keypoints tidak valid (harus 132 elemen)"}), 400
            input_data = np.array(keypoints).reshape(1, 132, 1)
        elif image_b64 is not None:
            # Proses gambar untuk ekstraksi keypoints
            keypoints = preprocess_image(image_b64)
            if keypoints is None:
                return jsonify({"error": "Gagal mengekstrak keypoints dari gambar"}), 400
            input_data = np.array(keypoints).reshape(1, 132, 1)
        else:
            logger.error("❌ Data tidak valid, harus ada keypoints atau image")
            return jsonify({"error": "Data tidak valid, harus ada keypoints atau image"}), 400

        # Lakukan prediksi
        probs = model.predict(input_data, verbose=0)
        pred_index = np.argmax(probs)
        confidence = float(probs[0][pred_index])

        logger.info(f"✅ Prediksi: label={label_map[pred_index]}, confidence={confidence:.4f}")

        return jsonify({
            "detected_letter": str(label_map[pred_index]),
            "confidence": round(confidence, 4)
        })

    except Exception as e:
        logger.error(f"❌ Error saat prediksi: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, threaded=True)  # Threaded untuk mendukung multiple requests