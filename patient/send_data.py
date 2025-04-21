import requests
import time
import pandas as pd
from datetime import datetime, timedelta
import os
import random
import numpy as np
import json

# URLs
MAIN_HOST = 'http://main_host:8000/track'
ML_MODEL_URL = 'http://ml_service:6000/predict'  # Change 'ml_service' based on your Docker network

# Read Excel file with multiple sheets
def read_patient_data_from_excel(file_path):
    if not os.path.exists(file_path):
        print(f"Error: The file '{file_path}' does not exist.")
        return []
    
    try:
        df_sheets = pd.read_excel(file_path, sheet_name=None)
    except Exception as e:
        print(f"Error reading the Excel file: {e}")
        return []
    
    return df_sheets

# Generate slightly updated vitals
def generate_updated_patient_data(meta, time_diff_minutes=1):
    heart_rate = meta['heart_rate'] + random.randint(-5, 5)
    bp_systolic = meta['bp_systolic'] + random.randint(-2, 2)
    bp_diastolic = meta['bp_diastolic'] + random.randint(-2, 2)
    respiratory_rate = meta['respiratory_rate'] + random.randint(-1, 1)
    spo2 = meta['spo2'] + random.randint(-1, 1)
    etco2 = meta['etco2'] + random.randint(-1, 1)
    temperature = round(meta['temperature'] + random.uniform(-0.1, 0.1), 1)
    wbc_count = round(meta['wbc_count'] + random.uniform(-0.2, 0.2), 1)
    lactate = round(meta['lactate'] + random.uniform(-0.1, 0.1), 1)
    blood_glucose = meta['blood_glucose'] + random.randint(-5, 5)

    timestamp = (datetime.utcnow() + timedelta(minutes=time_diff_minutes)).isoformat()

    return {
        "hospital": meta['hospital'],
        "dept": meta['dept'],
        "ward": meta['ward'],
        "patient": meta['patient'],
        "heart_rate": heart_rate,
        "bp_systolic": bp_systolic,
        "bp_diastolic": bp_diastolic,
        "respiratory_rate": respiratory_rate,
        "spo2": spo2,
        "etco2": etco2,
        "fio2": meta['fio2'],
        "temperature": temperature,
        "wbc_count": wbc_count,
        "lactate": lactate,
        "blood_glucose": blood_glucose,
        "timestamp": timestamp,
        "ecg_signal": "dummy_waveform_data"
    }

# Get anomaly score from ML service
def get_anomaly_score(data):
    try:
        response = requests.post(ML_MODEL_URL, json=data, timeout=3)
        if response.status_code == 200:
            return float(response.json().get("anomaly_score", 0.0))
        else:
            print(f"ML service failed with code {response.status_code}")
            return 0.0
    except Exception as e:
        print(f"Error contacting ML service: {e}")
        return 0.0

# Simulate traffic
def simulate_traffic(file_path):
    sheets = read_patient_data_from_excel(file_path)
    if not sheets:
        return

    sheet_names = list(sheets.keys())
    sheet_data = {name: sheets[name].to_dict(orient='records') for name in sheet_names}

    row_index = 0
    time_diff_minutes = 1

    while True:
        active = False

        for sheet_name in sheet_names:
            rows = sheet_data[sheet_name]
            if row_index < len(rows):
                active = True
                patient_meta = rows[row_index]

                data = generate_updated_patient_data(patient_meta, time_diff_minutes)

                anomaly_score = get_anomaly_score(data)
                data["anomaly_score"] = anomaly_score

                print("Sending Updated Data:", data)

                try:
                    response = requests.post(MAIN_HOST, json=data)
                    if response.status_code == 200:
                        print(f"✔ Sent | Patient: {data['patient']} | Score: {anomaly_score}")
                    else:
                        print(f"✘ Failed | Status: {response.status_code} | Patient: {data['patient']}")
                except requests.exceptions.RequestException as e:
                    print(f"Error while sending data: {e}")

                time.sleep(1)
                time_diff_minutes += 1

        if not active:
            print("All rows processed.")
            break

        row_index += 1

# Main
if __name__ == '__main__':
    file_path = "patients_data.xlsx"
    simulate_traffic(file_path)
