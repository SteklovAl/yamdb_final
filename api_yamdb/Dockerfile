
FROM python:3.7-slim
COPY ./ /app
RUN pip install -r /app/api_yamdb/requirements.txt
WORKDIR /app/api_yamdb/
CMD python manage.py runserver 0:5000