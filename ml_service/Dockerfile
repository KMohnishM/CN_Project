FROM python:3.10

WORKDIR /app

COPY model.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5051

CMD ["python", "model.py"]

