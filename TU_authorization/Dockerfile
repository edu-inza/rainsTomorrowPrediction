FROM ubuntu:latest
ADD requirements.txt TU_api_authorization.py ./
RUN apt-get update && apt-get install python3-pip -y && pip install -r requirements.txt
RUN mkdir logs
ENV API_ADDRESS='127.0.0.1'
ENV API_PORT=8000
CMD python3 TU_api_authorization.py