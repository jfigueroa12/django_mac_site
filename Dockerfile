FROM python:3
RUN mkdir /django_mac_site
RUN apt-get -y update && apt-get -y install vim
WORKDIR /django_mac_site
ADD requirements.txt /django_mac_site
RUN pip install -r requirements.txt
ADD . /django_mac_site
