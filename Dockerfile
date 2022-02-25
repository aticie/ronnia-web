FROM node:14 AS frontend_public

WORKDIR /usr/src/app

COPY ./frontend/package*.json ./

RUN npm install

COPY ./frontend/vite.config.js ./
COPY ./frontend/src ./src
COPY ./frontend/public ./public

RUN npm run build

FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim

WORKDIR /src

RUN mkdir -p /src/frontend

COPY --from=frontend_public /usr/src/app/dist ./frontend/dist

RUN mkdir -p /src/backend

COPY backend/requirements.txt ./backend/requirements.txt
RUN pip install -r backend/requirements.txt

ADD backend ./backend
COPY ./main.py .

ENV PYTHONPATH=$PYTHONPATH:/src/backend

ENTRYPOINT ["python", "main.py"]