#!/usr/bin/env bash
echo "Content-Type: text/html";
echo

blobjwt=$(curl http://127.0.0.1:5600/login -d '{"identity": "ephemeral@fixadmin.auth.domain.99_map", "service_id": "5aae5619a4b33765800bc5f9bdd1be507fb"}' -H 'Content-Type: application/json'  | cut -c14-616 | cut -d '|' -f2)

uid="/var/tmp/99_$RANDOM$RANDOM"
echo -n $blobjwt > $uid
jwt=$(openssl rsautl -sign -in $uid -inkey /opt/jwt/sign.key | xxd -p | tr -d '\n')
rm -rf $uid

b2=$(echo -n $blobjwt | b2sum -l 96 | cut -d' ' -f1 | tr -d '\n')
echo -n "$jwt" | redis-cli -x SET $b2  >/dev/null 2>&1
redis-cli EXPIRE $b2 60 >/dev/null 2>&1
b64=$(echo -n $blobjwt | b2sum | cut -d' ' -f1 | tr -d '\n' | xxd -r -p | base64 | tr -d '\n')
echo -n "$jwt" | redis-cli -x SET $b64  >/dev/null 2>&1
redis-cli EXPIRE $b2 2592000 >/dev/null 2>&1
echo "$jwt"
