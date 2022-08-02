FROM node:18 AS frontend_public

WORKDIR /usr/src

ADD ./frontend ./app

WORKDIR /usr/src/app

RUN npm install
RUN npm run build

FROM python:3.10-slim

WORKDIR /src

RUN mkdir -p /src/frontend

COPY --from=frontend_public /usr/src/app/dist ./frontend/dist

RUN mkdir -p /src/backend

RUN apt-get update && apt-get install -y build-essential libssl-dev uuid-dev cmake libcurl4-openssl-dev pkg-config -y
COPY backend/requirements.txt ./backend/requirements.txt
RUN pip install -r backend/requirements.txt

ADD backend ./backend
COPY ./main.py .

ENV PYTHONPATH=$PYTHONPATH:/src/backend

ENTRYPOINT ["python", "main.py"]