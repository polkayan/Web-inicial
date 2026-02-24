FROM python:3.11-alpine

WORKDIR /app

COPY . /app

WORKDIR /app/backend
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

CMD ["python", "app.py"]
