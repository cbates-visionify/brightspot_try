FROM python:3.9-slim

ADD app/ /app
ADD source/ /source


RUN apt update
RUN pip install -r /source/requirements.txt

# Start app
EXPOSE 5000
ENTRYPOINT ["python /app/app.py"]