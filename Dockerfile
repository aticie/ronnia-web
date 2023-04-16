# Start from low size builder image
FROM node:18.16.0-alpine3.17 as builder

# Set the working directory
WORKDIR /app

# Copy the package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the files
COPY . .

# Build the app
RUN npm run build

# Path: Dockerfile
FROM nginx:1.24.0-alpine

# Copy the build files
COPY --from=builder /app/dist /usr/share/nginx/html

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
