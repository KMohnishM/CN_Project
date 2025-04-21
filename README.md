
# Cloud-Based Network Traffic Monitoring and Anomaly Detection for Healthcare Infrastructure

![Architecture](./assets/architecture-diagram.png) <!-- Optional image placeholder -->

## 🩺 Project Overview

This project provides a scalable, Dockerized monitoring system designed for cloud-based healthcare infrastructures. It simulates a multi-tier hospital network and collects real-time medical metrics (SpO2, heart rate, ECG, etc.) from patient devices. The system is deployed on AWS and leverages Prometheus, Grafana, and Alertmanager to visualize and alert on anomalies.

> 🔍 Focused on ensuring reliability, real-time observability, and early anomaly detection within hospital networks using cloud-native tooling.

---

## ⚙️ Features

- 🚑 **Healthcare-specific metric simulation**: Heart rate, SpO2, BP, etc.
- ☁️ **Cloud-native deployment** on AWS EC2 using Docker.
- 📈 **Prometheus-based metric scraping** with 5s interval.
- 📊 **Grafana dashboards** for visualization (per ward, department, patient).
- 🚨 **Alertmanager** with threshold-based anomaly detection.
- 🧠 (Coming Soon) **ML-based anomaly detection** pipeline for vitals.

---

## 🧱 Project Structure

```
CN_Project/
│
├── app.py               # Flask service exposing /metrics
├── send_data.py         # Real-time medical metric simulator
├── docker-compose.yml   # Multi-container deployment definition
├── prometheus.yml       # Prometheus scrape & alert rules
├── grafana/             # Grafana provisioning and dashboards
├── assets/              # (Add images/diagrams/screenshots here)
└── README.md
```

---

## 🚀 Deployment Instructions

### Prerequisites

- Docker & Docker Compose
- AWS EC2 (Ubuntu)
- Python 3.9+

### Step-by-Step Guide

1. **Clone the repository**
   ```bash
   git clone https://github.com/KMohnishM/CN_Project.git
   cd CN_Project
   ```

2. **Configure Docker Compose**
   - Add `docker-compose.override.yml` if needed.
   - Ensure port 9090 (Prometheus) and 3000 (Grafana) are open.

3. **Launch the system**
   ```bash
   docker-compose up --build
   ```

4. **Access interfaces**
   - Prometheus: `http://localhost:9090`
   - Grafana: `http://localhost:3000`

---

## 📊 Dashboards

> Add screenshots inside the `/assets` folder and reference them here.

- Real-time ECG, HR, and SpO2 dashboards
- Department-wise heatmaps
- Alert timelines and incident patterns

---

## ⚠️ Alerting Rules (Prometheus)

```yaml
groups:
- name: healthcare-alerts
  rules:
  - alert: HypoxiaDetected
    expr: spo2_percent < 90
    for: 10s
    labels:
      severity: critical
    annotations:
      summary: "Patient is hypoxic!"
```

---

## 🧪 Simulated Metrics

- Heart Rate (BPM)
- Blood Pressure (Systolic/Diastolic)
- SpO2 (%)
- Respiratory Rate
- ECG waveform (synthetic)
- FiO2 (%), EtCO2, WBC Count, Glucose, Lactate

---

## 📦 Future Improvements

- Integrate ML-based alerting microservice
- Expand to Kubernetes-based orchestration
- Federated monitoring for multi-hospital use
- Real-time collaboration and logging pipeline

---

## 🧠 Author

**Kodukulla Mohnish Mythreya**  
2nd Year CSE, VIT Vellore  
[LinkedIn](https://linkedin.com/in/kmohnishm) | [GitHub](https://github.com/KMohnishM)

---

## 📜 License

This project is open-sourced under the MIT License. See [LICENSE](./LICENSE) for more details.
