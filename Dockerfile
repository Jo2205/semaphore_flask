# Gunakan image Python yang ringan
FROM python:3.9-slim

# Install dependency Linux untuk OpenCV
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Salin requirements.txt dan install
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Salin seluruh file project
COPY . .

# Expose port yang digunakan Flask
EXPOSE 8080

# Jalankan app dengan gunicorn
CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:8080", "app:app"]
