import pandas as pd
import random
from datetime import datetime, timedelta

# Generate data for 20 patients
def generate_patient_records(num_records=20):
    records = []
    for i in range(1, num_records + 1):
        record = {
            "hospital": random.choice(["1", "2"]),
            "dept": random.choice(["A", "B"]),
            "ward": str(random.randint(1, 4)),
            "patient": str(i),
            "timestamp": (datetime.utcnow() - timedelta(minutes=i)).isoformat(),
            "heart_rate": random.randint(60, 100),
            "bp_systolic": random.randint(100, 130),
            "bp_diastolic": random.randint(60, 90),
            "respiratory_rate": random.randint(12, 20),
            "spo2": random.randint(85, 98),
            "etco2": random.randint(30, 45),
            "fio2": 21,
            "temperature": round(random.uniform(36.5, 38.0), 1),
            "wbc_count": round(random.uniform(4.0, 12.0), 1),
            "lactate": round(random.uniform(1.0, 3.0), 1),
            "blood_glucose": random.randint(70, 180),
            "ecg_signal": "dummy_waveform_data"
        }
        records.append(record)
    return records

# Create DataFrame and save to Excel
df = pd.DataFrame(generate_patient_records())
df.to_excel("patients_data.xlsx", index=False)

print("✅ patients_data.xlsx created successfully.")

