FROM python:3.9-slim

WORKDIR /app

COPY ./ ./

RUN python3 -m pip install --upgrade pip

RUN pip3 install -r ./requirements.txt --no-cache-dir

RUN python3 manage.py collectstatic --no-input

CMD ["gunicorn", "backend.wsgi:application", "--bind", "0:8000"]
