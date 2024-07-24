FROM registry.cn-chengdu.aliyuncs.com/py-docker3/python:3-alpine

WORKDIR /app

COPY requirements.txt .

RUN set -eux && sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories

RUN apk add --update nodejs npm  && \
    rm -rf /var/cache/apk/*

RUN pip install --no-cache-dir -r requirements.txt -U -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY . .

ENV THREADS=4

EXPOSE 8080

CMD gunicorn -c config/gunicorn.conf.py -w $THREADS -b :8080 main:app