FROM python:3.11

COPY .. /mnt/locust
COPY ../requirements.txt /mnt/locust

WORKDIR /mnt/locust

RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt

ENV PYTHONPATH /mnt/locust

EXPOSE 8089 5557

RUN useradd --create-home locust
USER locust

ENTRYPOINT ["/bin/bash", "-c"]

# Turn off python output buffering
ENV PYTHONBUFFERED=1
