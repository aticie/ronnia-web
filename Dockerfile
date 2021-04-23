FROM node:14 AS frontend_public

WORKDIR /usr/src/app

COPY ./frontend/package*.json ./

RUN npm install

COPY ./frontend/rollup.config.js ./
COPY ./frontend/src ./src
COPY ./frontend/public ./public

RUN npm run build

FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim

WORKDIR /src

RUN pip install aiohttp

RUN mkdir -p /src/frontend/public

ADD ./app ./app
COPY --from=frontend_public /usr/src/app ./frontend/public

COPY ./main.py .

ENTRYPOINT ["python", "main.py"]