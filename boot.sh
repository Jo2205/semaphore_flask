#!/bin/bash

echo "[runtime] Menghubungkan pustaka bersama yang hilang..."

GL=$(find /nix/store -name 'libGL.so.1' | head -n 1)
GLIB=$(find /nix/store -name 'libglib-2.0.so.0' | head -n 1)
GTHREAD=$(find /nix/store -name 'libgthread-2.0.so.0' | head -n 1)

# Gunakan /opt/venv/lib karena /usr/lib read-only di Railway
ln -sf "$GL" /opt/venv/lib/libGL.so.1
ln -sf "$GLIB" /opt/venv/lib/libglib-2.0.so.0
ln -sf "$GTHREAD" /opt/venv/lib/libgthread-2.0.so.0

echo "[runtime] Mengaktifkan virtual environment..."
source /opt/venv/bin/activate

echo "[runtime] Menjalankan aplikasi..."
exec gunicorn -c gunicorn_config.py app:app
