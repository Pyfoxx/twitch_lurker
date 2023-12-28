FROM python:3.8-slim-buster
LABEL authors="Pyfox"

WORKDIR /app
COPY . /app
RUN pip install -r requirement.txt
CMD ["python", "main.py"]