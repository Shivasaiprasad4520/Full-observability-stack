# Full-observability-stack

## Full observability stack using Prometheus + Grafana + Alertmanager
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
---
### Step👍:2
___
#### Install Prometheus
___
       sudo apt update && sudo apt upgrade -y
       
       wget https://github.com/prometheus/prometheus/releases/download/v2.51.0/prometheus-2.51.0.linux-amd64.tar.gz
       tar xvf prometheus-2.51.0.linux-amd64.tar.gz
       sudo mv prometheus-2.51.0.linux-amd64 /opt/prometheus

       sudo useradd --no-create-home --shell /bin/false prometheus
       sudo chown -R prometheus:prometheus /opt/prometheus   

##### Create Prometheus.yml config
         sudo nano/opt/prometheus/prometheus.yml
---
### Step👍:3
___

---
### Step👍:4
___

---
### Step👍:5
___

---
### Step👍:6
___

---
### Step👍:7
___
