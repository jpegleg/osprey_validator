FROM debian
LABEL maintainer="carefuldata@protonmail.com"
LABEL version="1.0"
LABEL description="osprey 1"

RUN apt-get update && apt-get install -y apt-transport-https aptitude && aptitude install -y openssl apache2 haproxy redis
RUN mkdir /opt/jwt/

COPY apache2.conf /etc/apache2/apache2.conf
COPY cgi-sec.conf /etc/
COPY serve-cgi-bin.conf /etc/apache2/conf-enabled/
COPY create.cgi /var/www/html/
COPY validate.cgi /var/www/html/
COPY haproxy.cfg /etc/haproxy/haproxy.cfg
COPY keycert.pem /etc/keycert.pem

RUN /usr/bin/redis-server &
RUN ln -sf /dev/stdout /opt/jwt/jwt_access.log
RUN a2enmod cgi
RUN apachectl -D FOREGROUND &

EXPOSE 443

CMD /usr/sbin/haproxy -f /etc/haproxy/haproxy.cfg 
