FROM python:3
LABEL authors="danatolman"

COPY requirements.txt /requirements.txt

RUN pip install -r requirements.txt

COPY test.py /test.py

CMD ["python", "/test.py"]