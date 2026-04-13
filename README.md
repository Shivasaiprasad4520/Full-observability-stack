# Full-observability-stack

Full observability stack using Prometheus + Grafana + Alertmanager
===
Architecture of Full Observability-stack

<img width="1440" height="656" alt="image" src="https://github.com/user-attachments/assets/c7e604bd-5cb3-43c9-a715-5ae3f6a45631" />

---
### Step👍:1
___
#### Launch EC2 Instance with Following Inbound Rules

       Port 22       - SSH
       Port 9090     - Prometheus
       Port 3000     - Grafana
       Port 9100     - Node Exporter
       Port 9093     - Alertmanager
       Port 8000     - Sample app

change modification 400 to the keypair
     chmod 400 ~/ .ssh/your-key.pem
connect to instance
     ssh -i ~/ .ssh/your-key.pem ubuntu@publice_ip_address
