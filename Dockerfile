FROM python:3.10-slim-buster
WORKDIR /app
COPY app/requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY app/ /app
EXPOSE 8503
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8503"]