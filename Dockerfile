# our base image
FROM python:3-onbuild
WORKDIR /app
COPY app.py .
ENTRYPOINT ["python", "app.py"]
