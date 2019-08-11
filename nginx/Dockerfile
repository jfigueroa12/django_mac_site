FROM nginx:latest
RUN apt-get -y update && apt-get -y install vim
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/
