FROM python:3.9

WORKDIR /python

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY /src/main/python/app.py .

CMD ["python", "app.py"]
