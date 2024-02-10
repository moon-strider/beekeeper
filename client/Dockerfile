FROM node:14 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build -- --prod


FROM nginx:1.19.0-alpine
COPY --from=builder /app/dist/your-app-name /usr/share/nginx/html

COPY ./nginx.conf /etc/nginx/nginx.conf
COPY . /usr/share/nginx/html


HEALTHCHECK --interval=15s --timeout=10s --start-period=5s --retries=5 \
    CMD curl -f http://localhost:80 || exit  1