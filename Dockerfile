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

RUN pip install aiohttp aiofiles python-jose[cryptography]

RUN mkdir -p /src/frontend

ADD backend ./app
COPY --from=frontend_public /usr/src/app ./frontend/

COPY ./main.py .

ENTRYPOINT ["python", "main.py"]