FROM nginx:latest

RUN apt update && apt install -y apache2-utils

COPY nginx.conf /etc/nginx/nginx.conf

COPY ./html/ /usr/share/nginx/html/

COPY --chmod=555 entrypoint.sh /usr/local/bin/entrypoint.sh

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["nginx", "-g", "daemon off;", "-c", "/etc/nginx/nginx.conf"]
