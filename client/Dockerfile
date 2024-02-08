FROM nginx:alpine AS extractor

COPY ./nginx.conf /etc/nginx/nginx.conf
COPY . /usr/share/nginx/html

HEALTHCHECK --interval=15s --timeout=10s --start-period=5s --retries=5 \
    CMD curl -f http://localhost:80 || exit  1