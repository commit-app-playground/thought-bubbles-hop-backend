
FROM python:3.7
RUN  apt-get update \
  && apt-get install -y wget \
  && rm -rf /var/lib/apt/lists/*

RUN mkdir /app
WORKDIR /app
ADD . /app/
RUN pip install -r requirements.txt
#RUN mkdir instance
RUN scripts/download-model.sh

EXPOSE 80
CMD ["python", "/app/main.py"]
