#!/bin/bash

echo "[runtime] Mengaktifkan virtual environment..."
source /opt/venv/bin/activate

echo "[runtime] Menjalankan aplikasi..."
exec gunicorn -w 1 -b 0.0.0.0:8080 app:app
