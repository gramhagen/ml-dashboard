FROM python:2.7

MAINTAINER gramhagen

# install nginx
# modified version from https://github.com/dockerfile/nginx
RUN \
    apt-get update && \
    apt-get install -y nginx && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /etc/nginx/sites-enabled/default && \
    echo "\ndaemon off;" >> /etc/nginx/nginx.conf && \
    chown -R www-data:www-data /var/lib/nginx

# install supervisor
RUN apt-get update && \
    apt-get install -y supervisor

# install node.js
RUN \
    curl -sL https://deb.nodesource.com/setup_5.x | bash - && \
    apt-get install -y nodejs

# install python requirements
# only pulling in the requirements file lets docker reuse intermediate containers for python packages
ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

# pull in code
ADD ./ /usr/local/app

# setup the application
WORKDIR /usr/local/app
RUN \
    python manage.py init && \
    python manage.py publish_docs && \
    cd src && \
    npm install && \
    gulp

# make soft links for config files
RUN \
    ln -s /usr/local/app/config/nginx.conf /etc/nginx/sites-enabled/ && \
    ln -s /usr/local/app/config/supervisor.conf /etc/supervisor/conf.d/

# setup directory permissions
RUN \
    mkdir /var/run/uwsgi && \
    mkdir /var/log/app && \
    chown www-data /var/run/uwsgi && \
    chgrp www-data /var/run/uwsgi && \
    chown www-data /var/log/app && \
    chgrp www-data /var/log/app

EXPOSE 80
EXPOSE 9001

CMD ["/usr/bin/supervisord", "-n"]
