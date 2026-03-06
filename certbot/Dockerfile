FROM certbot/certbot:latest

RUN pip install certbot-nginx

ARG DOMAIN
ARG EMAIL

RUN certbot \
    --nginx \
    -d ${DOMAIN} \
    --email ${EMAIL} \
    --agree-tos \
    --no-eff-email \
    --non-interactive || true
