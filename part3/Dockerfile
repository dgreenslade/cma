# syntax=docker/dockerfile:1.4
FROM python:3.10-alpine

# WORKDIR /Q3

COPY requirements.txt ./
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install -r requirements.txt
COPY . /.

#EXPOSE 8000

ENTRYPOINT ["python3"]
CMD ["app.py"]