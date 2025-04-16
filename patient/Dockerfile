FROM python:3.10-slim

WORKDIR /app

COPY send_data.py .
COPY patients_data.xlsx .  

RUN pip install requests pandas openpyxl 

CMD ["python", "send_data.py"]
