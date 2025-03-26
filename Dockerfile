FROM python:3.9.21-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip # Update pip
RUN pip install --no-cache-dir -r requirements.txt # Clean install of requirements

COPY . .

EXPOSE 8000
EXPOSE 8501

CMD ["/bin/bash", "-c", "uvicorn mnist_server:app --host 0.0.0.0 --port 8000 & streamlit run mnist_fron.py --server.address 0.0.0.0 --server.port 8501"]
