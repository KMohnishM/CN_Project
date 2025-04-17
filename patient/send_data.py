import requests
import time
import pandas as pd
from datetime import datetime, timedelta
import os
import random
import numpy as np
import json

# The URL for the main host where the data will be sent
MAIN_HOST = 'http://main_host:8000/track'

# Function to read patient data from Excel file (supports multiple sheets)
def read_patient_data_from_excel(file_path):
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"Error: The file '{file_path}' does not exist.")
        return []
    
    # Read the Excel file with multiple sheets
    try:
        # Load the Excel file
        df_sheets = pd.read_excel(file_path, sheet_name=None)  # This will load all sheets
    except Exception as e:
        print(f"Error reading the Excel file: {e}")
        return []
    
    return df_sheets

# Function to generate updated patient data with new values
def generate_updated_patient_data(meta, time_diff_minutes=1):
    # Simulate incremental changes in the patient's data
    heart_rate = meta['heart_rate'] + random.randint(-5, 5)  # slight change
    bp_systolic = meta['bp_systolic'] + random.randint(-2, 2)
    bp_diastolic = meta['bp_diastolic'] + random.randint(-2, 2)
    respiratory_rate = meta['respiratory_rate'] + random.randint(-1, 1)
    spo2 = meta['spo2'] + random.randint(-1, 1)
    etco2 = meta['etco2'] + random.randint(-1, 1)
    temperature = round(meta['temperature'] + random.uniform(-0.1, 0.1), 1)
    wbc_count = round(meta['wbc_count'] + random.uniform(-0.2, 0.2), 1)
    lactate = round(meta['lactate'] + random.uniform(-0.1, 0.1), 1)
    blood_glucose = meta['blood_glucose'] + random.randint(-5, 5)

    # Update timestamp
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

# Function to simulate sending patient data one by one
def simulate_traffic(file_path):
    sheets = read_patient_data_from_excel(file_path)
    if not sheets:
        return

    sheet_names = list(sheets.keys())
    sheet_data = {name: sheets[name].to_dict(orient='records') for name in sheet_names}

    row_index = 0  # Start from the first row
    time_diff_minutes = 1

    while True:
        active = False  # Check if there's any data left

        for sheet_name in sheet_names:
            rows = sheet_data[sheet_name]
            if row_index < len(rows):
                active = True  # At least one sheet has data at this index
                patient_meta = rows[row_index]

                # Generate updated data
                data = generate_updated_patient_data(patient_meta, time_diff_minutes)
                print("Sending Updated Data for Patient", patient_meta['patient'], ":", data)

                try:
                    response = requests.post(MAIN_HOST, json=data)
                    if response.status_code == 200:
                        print(f"Sent | Status: {response.status_code} | Patient: {data['patient']}")
                    else:
                        print(f"Failed to send | Status: {response.status_code} | Patient: {data['patient']}")
                except requests.exceptions.RequestException as e:
                    print(f"Error while sending data: {e}")

                time.sleep(1)
                time_diff_minutes += 1

        if not active:
            print("All rows processed from all sheets.")
            break  # Exit if no more data left in any sheet

        row_index += 1  # Move to next row in next cycle


# Main loop to keep sending updated data indefinitely
if __name__ == '__main__':
    file_path = "patients_data.xlsx"  # Ensure this is the correct path to your Excel file
    simulate_traffic(file_path)  # Continuously send data for all patients sheet by sheet
