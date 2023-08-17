# ./.github/actions/docker-action/Dockerfile
FROM python:3

COPY /requirements.txt /requirements.txt

RUN pip install -r requirements.txt

COPY ../../../locustfiles/test.py /locustfile.py
COPY ./run_locust.py /run_locust.py

CMD ["python", "/run_locust.py"]