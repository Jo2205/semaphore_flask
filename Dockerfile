# Gunakan base image Python yang lebih ramping
FROM python:3.9-slim

# Set direktori kerja di dalam container
WORKDIR /app

# ---- LANGKAH KRUSIAL: Instal dependensi sistem untuk OpenCV & MediaPipe ----
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Salin file requirements terlebih dahulu untuk memanfaatkan caching Docker
COPY requirements.txt .

# Instal paket Python
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Salin sisa kode aplikasi Anda
COPY . .

# Beri tahu Hugging Face port mana yang digunakan aplikasi
EXPOSE 7860

# Perintah untuk menjalankan aplikasi menggunakan Gunicorn
CMD ["gunicorn", "--worker-tmp-dir", "/dev/shm", "-w", "1", "-b", "0.0.0.0:7860", "app:app"]
