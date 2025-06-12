FROM python:3.11

WORKDIR /music_library

COPY . .

RUN pip install -r requirements.txt --no-cache-dir

EXPOSE 5002

CMD ["python", "main.py"]
