FROM python:3.10-slim

RUN apt-get update && \
    apt-get install -y tzdata && \
    apt-get install -y locales && \
    sed -i -e 's/# pt_BR.UTF-8 UTF-8/pt_BR.UTF-8 UTF-8/' /etc/locale.gen && \
    locale-gen

ENV LANG pt_BR.UTF-8
ENV LC_ALL pt_BR.UTF-8
ENV LANGUAGE pt_BR:en
ENV TZ=America/Sao_Paulo

RUN pip install --upgrade pip>=23.1.2
COPY ./api/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY ./api/app /app/app
COPY ./api/main.py /app/main.py

WORKDIR /app

EXPOSE 8989

CMD ["uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8989", "--reload", "--forwarded-allow-ips", "'*'"]
