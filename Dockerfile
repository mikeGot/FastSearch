FROM python:3.8
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN python3 elt.py
CMD ["python3", "server.py"]
