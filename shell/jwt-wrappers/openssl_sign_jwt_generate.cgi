#!/usr/bin/env bash
echo "Content-Type: text/html";
echo

blobjwt=$(curl http://127.0.0.1:5599/login -d '{"identity": "root@localhost", "service_id": "3ec85f59dce67fc936d7f1e63466aea3b6c"}' -H 'Content-Type: application/json'  | cut -c14-616 | cut -d '|' -f2)

uid="99_$RANDOM$RANDOM"
echo -n $blobjwt > /var/tmp/$uid
jwt=$(openssl rsautl -sign -in /var/tmp/$uid -inkey /opt/jwt/sign.key | xxd -p | tr -d '\n')
rm -rf /var/tmp/$uid

b2=$(echo -n $blobjwt | b2sum -l 96 | cut -d' ' -f1 | tr -d '\n')
echo -n "$jwt" | redis-cli -x SET $b2  >/dev/null 2>&1
redis-cli EXPIRE $b2 60 >/dev/null 2>&1
echo "$jwt"
