FROM python:3.7

RUN pip install gunicorn

WORKDIR /app
COPY requirements.txt /app

RUN pip install -r requirements.txt

COPY website /app/website
COPY ecb1.py /app/

EXPOSE 5000/tcp

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "ecb1:app"]