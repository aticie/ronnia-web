# Start from low size builder image
FROM node:18.16.0-alpine3.17 as builder

# Set the working directory
WORKDIR /app

# Copy the package.json and package-lock.json
COPY package.json ./
COPY package-lock.json ./

# Install dependencies
RUN npm install --ignore-scripts true

# Copy the rest of the files
COPY ./src ./src
COPY ./public ./public
COPY ./.env.production ./.env
COPY ./tsconfig.json ./
COPY ./tsconfig.node.json ./
COPY ./vite.config.ts ./
COPY ./postcss.config.js ./
COPY ./tailwind.config.js ./
COPY ./index.html ./

# Build the app
RUN npm run build

# Path: Dockerfile
FROM nginx:1.27.0

# Copy the build files
COPY --from=builder /app/dist /usr/share/nginx/html

COPY default.conf /etc/nginx/conf.d/default.conf

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
