FROM python:3.8

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.2.1/wait /wait
RUN chmod +x /wait

CMD /wait && python main.py

# CMD ["python", "main.py"]