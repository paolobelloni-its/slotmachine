FROM python:3.11-slim

WORKDIR /app
COPY app/slot_server.py /app/slot_server.py

EXPOSE 7777
CMD ["python", "-u", "/app/slot_server.py"]