FROM python:3.8
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN python3 elt.py
CMD ["uvicorn", "server:app", "--host", "0.0.0.0"]
