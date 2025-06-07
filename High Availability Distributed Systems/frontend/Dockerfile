# Use an official Node.js runtime as the base image
FROM node:18-alpine AS build

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json to the working directory
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

ARG VITE_SCRAPER_TIMEOUT_MS

ENV VITE_SCRAPER_TIMEOUT_MS=$VITE_SCRAPER_TIMEOUT_MS

# Build the Vite app
RUN npm run build

# Copy the assets folder into the dist directory
RUN cp -r src/assets dist/assets

# Use an official Nginx image to serve the built app
FROM nginx:alpine

# Install gettext for envsubst
RUN apk add --no-cache gettext

# Default values for service URLs
ENV TRAIN_SCRAPER_URL=http://host.docker.internal:8080
ENV ACCOUNT_MANAGER_URL=http://host.docker.internal:5220
ENV TRANSACTION_MANAGER_URL=http://host.docker.internal:5221
ENV ANALYTICS_SERVICE_URL=http://host.docker.internal:5223

# Copy the built app from the previous stage to the Nginx web server directory
COPY --from=build /app/dist /usr/share/nginx/html

# Copy the Nginx config template
COPY nginx.conf.template /etc/nginx/templates/default.conf.template

# Expose port 80
EXPOSE 80

# Start Nginx with the entrypoint script
CMD /bin/sh -c "envsubst '\${TRAIN_SCRAPER_URL} \${ACCOUNT_MANAGER_URL} \${TRANSACTION_MANAGER_URL} \${ANALYTICS_SERVICE_URL}' < /etc/nginx/templates/default.conf.template > /etc/nginx/conf.d/default.conf && nginx -g 'daemon off;'"

