FROM node:24-alpine AS build
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --ignore-scripts
COPY . .
RUN npm run build

FROM nginx:1.28-alpine
ENV NGINX_ENTRYPOINT_LOCAL_RESOLVERS=1
COPY --chmod=755 19-api-upstream.envsh /docker-entrypoint.d/19-api-upstream.envsh
COPY --chmod=755 20-sentry-config.envsh /docker-entrypoint.d/20-sentry-config.envsh
COPY --chmod=755 25-error-log-level.envsh /docker-entrypoint.d/25-error-log-level.envsh
COPY --from=build /app/dist /usr/share/nginx/html
COPY default.conf.template /etc/nginx/templates/default.conf.template
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
