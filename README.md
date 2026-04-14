# Full-observability-stack

## Full observability stack using Prometheus + Grafana + Alertmanager

Architecture of Full Observability-stack

<img width="1440" height="656" alt="image" src="https://github.com/user-attachments/assets/c7e604bd-5cb3-43c9-a715-5ae3f6a45631" />

---
### Step👍:1
___
#### Launch EC2 Instance with Following Inbound Rules
<img width="1239" height="636" alt="image" src="https://github.com/user-attachments/assets/dfef67c7-aba7-4f54-8aa1-771959b4bfe3" />


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

##### Create systemd service so Prometheus auto-starts

         sudo nano/etc/systemd/system/prometheus.service
         
##### Start the prometheus services

         sudo systemctl daemon-reload
         sudo systemctl enable prometheus
         sudo systemctl start prometheus
         sudo systemctl status promethueus

###### Test: Open browser -> http://EC2_IP Address:9090
<img width="1440" height="619" alt="image" src="https://github.com/user-attachments/assets/057b5a23-7266-47e7-9ffa-13057183cf3b" />


---
### Step👍:3
___
#### Install Node Exporter

        wget https://github.com/prometheus/node_exporter/releases/download/v1.7.0/node_exporter-1.7.0.linux-amd64.tar.gz
        tar xvf node_exporter-1.7.0.linux-amd64.tar.gz
        sudo mv node_exporter-1.7.0.linux-amd64/node_exporter /usr/local/bin/

        sudo useradd --no-create-home --shell /bin/false node_exporter

##### Create node_exporter.service

        sudo nano /etc/systemd/system/node_exporter.service
        
##### Start the exporter service

        sudo systemctl daemon-reload
        sudo systemctl enable node_exporter
        sudo systemctl start node_exporter
        
###### Test: Open browser -> http://EC2_IP Address:9100/metrics

<img width="1440" height="321" alt="image" src="https://github.com/user-attachments/assets/15660a4a-9b80-44ca-bdb9-6bebf9c0cfc1" />

<img width="790" height="759" alt="image" src="https://github.com/user-attachments/assets/79d5c1db-35e9-470d-af61-eebe9e4b93b0" />


---
### Step👍:4
___
#### Create a sample Python app with /metrics endpoint

Install Python and depended packages

         sudo apt install python3-pip -y
         pip3 install prometheus_client flask
         
write python file sample_app.py 

         nano~/sample_app.py
         
then execute the file

         python3 ~/sample_app.py &
         curl http://localhost:8000/metrics

---
### Step👍:5
___
#### Install Grafana

         sudo apt install -y apt-transport-https software-properties-common wget
         wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -
         echo "deb https://packages.grafana.com/oss/deb stable main" | sudo tee /etc/apt/sources.list.d/grafana.list
         sudo apt update && sudo apt install grafana -y
         sudo systemctl enable grafana-server
         sudo systemctl start grafana-server

###### Test: Login: http://YOUR_EC2_IP:3000 — default user: admin / password: admin

<img width="1429" height="769" alt="image" src="https://github.com/user-attachments/assets/74c7dc6d-93cd-4146-a20b-6f204435ffc5" />


##### Add Prometheus as data source in Grafana UI

         Grafana → Connections → Data sources → Add → Prometheus
         URL: http://localhost:9090
         Click: Save & test → should show green "Data source is working"
         
##### Import a pre-built Node Exporter dashboard

         Grafana → Dashboards → Import
         Dashboard ID: 1860    (Node Exporter Full — most popular)
         Select Prometheus as data source → Import

         <img width="1396" height="809" alt="image" src="https://github.com/user-attachments/assets/71c71dd7-09b1-4a22-a2d3-bd39754db47e" />

##### Create custom app dashboard — add these panels manually

         Panel 1 — Total requests (Stat panel)
           Query: sum(app_requests_total)

         Panel 2 — Request rate per second (Time series)
           Query: rate(app_requests_total[5m])

         Panel 3 — Error rate % (Gauge panel)
           Query: rate(app_errors_total[5m]) / rate(app_requests_total[5m]) * 100

         Panel 4 — Active users (Time series)
           Query: app_active_users

         Panel 5 — p95 request latency (Time series)
           Query: histogram_quantile(0.95, rate(app_request_latency_seconds_bucket[5m]))
           
---
### Step👍:6
___
#### Configure Alertmanager + alert rules

##### Install the Alertmanager

          wget https://github.com/prometheus/alertmanager/releases/download/v0.27.0/alertmanager-0.27.0.linux-amd64.tar.gz
          tar xvf alertmanager-0.27.0.linux-amd64.tar.gz
          sudo mv alertmanager-0.27.0.linux-amd64 /opt/alertmanager
          
###### Get free Slack webhook: Create Slack workspace → Apps → Incoming Webhooks → add to channel → copy URL.

###### Alertmanager config — sends alerts to Slack

          sudo nano /opt/alertmanager/alertmanager.yml

###### Create alert rules file

          sudo nano /opt/prometheus/alert_rules.yml
          
###### Create alert service file

          sudo nano /etc/systemd/system/alertmanager.service
          
###### start the service file

          sudo systemctl daemon-reload
          sudo systemctl enable alertmanager
          sudo systemctl start alertmanager

---
### Step👍:7
___
#### Test everything end-to-end

##### Stress test to trigger CPU alert

          sudo apt install stress -y
          stress --cpu 2 --timeout 180    # spikes CPU for 3 min — should trigger alert
          
##### Verify alert fired in Prometheus UI

          http://YOUR_EC2_IP:9090/alerts   # should show HighCPUUsage in FIRING state
          http://YOUR_EC2_IP:9093          # Alertmanager UI — shows active alerts

##### Load test your app to generate metrics

sudo apt install apache2-utils -y

ab -n 1000 -c 10 http://localhost:8000/

(# Then check your Grafana dashboard — you'll see request rate spike)


