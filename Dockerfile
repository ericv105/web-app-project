FROM python:3.8

WORKDIR /app
ENV PYTHONUNBUFFERED=1

COPY . .

RUN pip install -r requirements.txt

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.2.1/wait /wait
RUN chmod +x /wait

ENV PYTHONUNBUFFERED=1

CMD /wait && python -u main.py

# CMD ["python", "main.py"]