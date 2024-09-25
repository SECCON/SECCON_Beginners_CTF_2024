FROM nginx:latest

COPY nginx.conf /etc/nginx/nginx.conf

COPY ./html/ /usr/share/nginx/html/

CMD ["nginx", "-g", "daemon off;", "-c", "/etc/nginx/nginx.conf"]