import os

# Bind to the port provided by Render
bind = f"0.0.0.0:{os.environ.get('PORT', 5000)}"

# Worker configuration
workers = 1  # Single worker untuk model ML yang besar
worker_class = "sync"
worker_connections = 1000

# Timeout settings
timeout = 120  # 2 menit untuk prediksi ML
keepalive = 5

# Memory management
max_requests = 100
max_requests_jitter = 10

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"