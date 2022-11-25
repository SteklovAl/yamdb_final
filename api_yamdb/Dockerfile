
FROM python:3.7-slim
COPY ./ /app
RUN pip install -r /app/api_yamdb/requirements.txt
WORKDIR /app/api_yamdb/
CMD ["gunicorn", "api_yamdb.wsgi:application", "--bind", "0:8000" ]