FROM python:3.7-slim
WORKDIR /app
COPY ./api_yamdb/requirements.txt .
RUN pip3 install -r /requirements.txt --no-cache-dir
COPY . ./
CMD ["python3", "./api_yamdb/manage.py", "runserver", "0:8000"] 