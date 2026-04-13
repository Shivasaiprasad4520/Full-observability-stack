from flask import Flask
from prometheus_client import Counter, Histogram, generate_latest, Gauge
import time, random

app = Flask(__name__)

REQUEST_COUNT = Counter('app_requests_total', 'Total requests', ['method', 'endpoint'])
REQUEST_LATENCY = Histogram('app_request_latency_seconds', 'Request latency')
ERROR_COUNT = Counter('app_errors_total', 'Total errors')
ACTIVE_USERS = Gauge('app_active_users', 'Simulated active users')

@app.route('/')
def index():
    REQUEST_COUNT.labels(method='GET', endpoint='/').inc()
    with REQUEST_LATENCY.time():
        time.sleep(random.uniform(0.01, 0.3))
        ACTIVE_USERS.set(random.randint(10, 200))
        if random.random() < 0.05:   # 5% error rate
            ERROR_COUNT.inc()
            return "Error", 500
    return "Hello from monitored app!", 200

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': 'text/plain'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
