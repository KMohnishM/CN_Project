import pandas as pd
import random
from datetime import datetime, timedelta

def generate_patient_records(num_records=500):
    records = []
    for i in range(1, num_records + 1):
        # Normal values
        heart_rate = random.randint(60, 100)
        bp_systolic = random.randint(100, 130)
        bp_diastolic = random.randint(60, 90)
        respiratory_rate = random.randint(12, 20)
        spo2 = random.randint(85, 98)
        etco2 = random.randint(30, 45)

        if random.random() < 0.2:  # 20% chance of anomalies
            anomaly_fields = random.sample(
                ["heart_rate", "bp_systolic", "bp_diastolic", "respiratory_rate", "spo2", "etco2"],
                k=random.randint(1, 3)
            )
            for field in anomaly_fields:
                if field == "heart_rate":
                    heart_rate = random.choice([random.randint(30, 50), random.randint(120, 160)])
                elif field == "bp_systolic":
                    bp_systolic = random.choice([random.randint(70, 90), random.randint(140, 170)])
                elif field == "bp_diastolic":
                    bp_diastolic = random.choice([random.randint(40, 55), random.randint(95, 110)])
                elif field == "respiratory_rate":
                    respiratory_rate = random.choice([random.randint(5, 10), random.randint(25, 35)])
                elif field == "spo2":
                    spo2 = random.randint(70, 84)
                elif field == "etco2":
                    etco2 = random.choice([random.randint(10, 25), random.randint(46, 60)])

        record = {
            "hospital": random.choice(["1", "2"]),
            "dept": random.choice(["A", "B"]),
            "ward": str(random.randint(1, 4)),
            "patient": str(i),
            "timestamp": (datetime.utcnow() - timedelta(minutes=i)).isoformat(),
            "heart_rate": heart_rate,
            "bp_systolic": bp_systolic,
            "bp_diastolic": bp_diastolic,
            "respiratory_rate": respiratory_rate,
            "spo2": spo2,
            "etco2": etco2,
            "fio2": 21,
            "temperature": round(random.uniform(36.5, 38.0), 1),
            "wbc_count": round(random.uniform(4.0, 12.0), 1),
            "lactate": round(random.uniform(1.0, 3.0), 1),
            "blood_glucose": random.randint(70, 180),
            "ecg_signal": "dummy_waveform_data"
        }
        records.append(record)
    return records

# Save the dataset to Excel
df = pd.DataFrame(generate_patient_records())
df.to_excel(r"d:\cn proj\CN_Project\patient\patients_data.xlsx", index=False)

print("patients_data.xlsx created successfully ")
