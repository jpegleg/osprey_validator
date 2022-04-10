FROM debian
LABEL maintainer="carefuldata@protonmail.com"
LABEL version="1.0"
LABEL description="osprey 1"

RUN apt-get update && apt-get install -y apt-transport-https aptitude && aptitude install -y openssl apache2 haproxy redis curl xxd

RUN mkdir -p /opt/jwt/workspace/files

COPY apache2.conf /etc/apache2/apache2.conf
COPY serve-cgi-bin.conf /etc/apache2/conf-enabled/
COPY other-vhosts-access-log.conf /etc/apache2/conf-enabled/other-vhosts-access-log.conf
COPY 000-default.conf /etc/apache2/sites-enabled/000-default.conf
COPY index.html /var/www/html/index.html
COPY create.cgi /var/www/html/
COPY validate.cgi /var/www/html/
COPY haproxy.cfg /etc/haproxy/haproxy.cfg
COPY keycert.pem /etc/keycert.pem
COPY auth.pem /etc/auth.pem
COPY royal_blobs_jwt_service /usr/sbin/jwt-server
COPY sign.key /opt/jwt/
COPY sign.pub /opt/jwt/
COPY sign.sh /opt/jwt/
COPY verify.sh /opt/jwt/

RUN chmod +x /usr/sbin/jwt-server && chmod +x /var/www/html/create.cgi && chmod +x /var/www/html/validate.cgi && chmod +x /opt/jwt/sign.sh && chmod +x /opt/jwt/verify.sh
RUN ln -sf /dev/stdout /opt/jwt/jwt_access.log
RUN ln -sf /dev/stdout /opt/jwt/jwt.log
RUN a2enmod cgi

EXPOSE 443

CMD cd /opt/jwt/workspace && /usr/sbin/apachectl restart && /usr/sbin/jwt-server > /opt/jwt/jwt.log 2>&1 & /usr/bin/redis-server > /opt/jwt/redis.log 2>&1 & /usr/sbin/haproxy -f /etc/haproxy/haproxy.cfg
