FROM debian
LABEL maintainer="carefuldata@protonmail.com"
LABEL version="1.0"
LABEL description="osprey 2"

RUN apt-get update && apt-get install -y apt-transport-https aptitude && aptitude install -y openssl apache2 haproxy redis curl xxd

RUN mkdir -p /opt/jwt/workspace/files

COPY apache2.conf /etc/apache2/apache2.conf
COPY serve-cgi-bin.conf /etc/apache2/conf-enabled/
COPY other-vhosts-access-log.conf /etc/apache2/conf-enabled/other-vhosts-access-log.conf
COPY 000-default.conf /etc/apache2/sites-enabled/000-default.conf
COPY index.html /var/www/html/index.html
COPY cuser1.cgi /var/www/html/
COPY vuser1.cgi /var/www/html/
COPY cuser2.cgi /var/www/html/
COPY vuser2.cgi /var/www/html/
COPY haproxy.cfg /etc/haproxy/haproxy.cfg
COPY keycert.pem /etc/keycert.pem
COPY auth.pem /etc/auth.pem
COPY fixadm /usr/sbin/jwt-server
COPY sign.key /opt/jwt/
COPY sign.pub /opt/jwt/
COPY sign.sh /opt/jwt/
COPY verify.sh /opt/jwt/
COPY proc100 /opt/jwt/workspace/
COPY initial.flat /opt/jwt/workspace/
COPY data.json /opt/jwt/workspace/
COPY flush-hydrate /opt/jwt/workspace/

RUN chmod +x /opt/jwt/workspace/flush-hydrate && chmod +x /opt/jwt/workspace/proc100 && chmod +x /usr/sbin/jwt-server && chmod +x /var/www/html/cuser1.cgi && chmod +x /var/www/html/cuser2.cgi && chmod +x /var/www/html/vuser1.cgi && chmod +x /var/www/html/vuser2.cgi && chmod +x /opt/jwt/sign.sh && chmod +x /opt/jwt/verify.sh
RUN touch /opt/jwt/jwt_access_check.log && chown www-data:www-data /opt/jwt/jwt_access_check.log
RUN ln -sf /dev/stdout /opt/jwt/jwt.log
RUN a2enmod cgi

EXPOSE 443

CMD cd /opt/jwt/workspace && /usr/sbin/apachectl start && /usr/sbin/jwt-server > /opt/jwt/jwt.log 2>&1 & /usr/bin/redis-server > /opt/jwt/redis.log 2>&1 & /usr/sbin/haproxy -f /etc/haproxy/haproxy.cfg
