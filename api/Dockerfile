FROM ubuntu:latest
ADD requirements.txt api.py model.py rains.csv ./
RUN apt-get update && apt-get install python3-pip -y && pip install -r requirements.txt
EXPOSE 8000
CMD uvicorn api:app --host 0.0.0.0