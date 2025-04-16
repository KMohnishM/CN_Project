import requests
import time
import pandas as pd
from datetime import datetime
import os

# The URL for the main host where the data will be sent
MAIN_HOST = 'http://main_host:8000/track'

# Function to read patient data from Excel file
def read_patient_data_from_excel(file_path):
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"Error: The file '{file_path}' does not exist.")
        return []
    
    # Read the Excel file
    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        print(f"Error reading the Excel file: {e}")
        return []

    # Convert dataframe to list of dictionaries
    patient_data = df.to_dict(orient='records')
    return patient_data

# Example Excel file path (Ensure the file is present at this path)
file_path = "/app/patients_data.xlsx"

# Function to generate patient data in the desired format
def generate_patient_data(meta):
    return {
        "hospital": meta['hospital'],
        "dept": meta['dept'],
        "ward": meta['ward'],
        "patient": meta['patient'],
        "heart_rate": meta['heart_rate'],
        "bp_systolic": meta['bp_systolic'],
        "bp_diastolic": meta['bp_diastolic'],
        "respiratory_rate": meta['respiratory_rate'],
        "spo2": meta['spo2'],
        "etco2": meta['etco2'],
        "fio2": meta['fio2'],
        "temperature": meta['temperature'],
        "wbc_count": meta['wbc_count'],
        "lactate": meta['lactate'],
        "blood_glucose": meta['blood_glucose'],
        "timestamp": datetime.utcnow().isoformat(),
        "ecg_signal": "dummy_waveform_data"
    }

# Function to simulate sending patient data
def simulate_traffic():
    patients = read_patient_data_from_excel(file_path)
    
    if not patients:
        return  # If no data was loaded, exit early

    for patient_meta in patients:
        data = generate_patient_data(patient_meta)
        print("🚀 Sending Data:", data)  # 👈 See the actual payload
        
        try:
            # Send the data to the server
            response = requests.post(MAIN_HOST, json=data)
            # Check if the request was successful
            if response.status_code == 200:
                print(f"✅ Sent | Status: {response.status_code} | Patient: {data['patient']}")
            else:
                print(f"❌ Failed to send | Status: {response.status_code} | Patient: {data['patient']}")
        except requests.exceptions.RequestException as e:
            # Handle network issues, server down, etc.
            print(f"Error while sending data: {e}")
        
        time.sleep(1)  # Simulate a slight delay between sending data

# Main loop to keep sending data indefinitely
if __name__ == '__main__':
    while True:
        simulate_traffic()
