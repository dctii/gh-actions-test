# ./.github/actions/docker-action/Dockerfile
FROM python:3

# Install GitHub CLI
RUN apt-get update && apt-get install -y software-properties-common && \
    apt-key adv --keyserver keyserver.ubuntu.com --recv-key C99B11DEB97541F0 && \
    apt-add-repository https://cli.github.com/packages && \
    apt-get update && apt-get install -y gh

COPY requirements.txt /requirements.txt

RUN pip install -r requirements.txt

COPY locustfile.py /locustfile.py
COPY run_locust.py /run_locust.py

CMD ["python", "/run_locust.py"]