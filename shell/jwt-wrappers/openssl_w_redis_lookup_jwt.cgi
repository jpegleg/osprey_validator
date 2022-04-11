#!/usr/bin/env bash
echo "Content-Type: text/html";
echo
uid="100_$RANDOM$RANDOM"
echo -n $blobjwt > /var/tmp/$uid
echo -n $1 | xxd -r -p > /var/tmp/$uid
jwt="$(openssl rsautl -verify -in /var/tmp/$uid -inkey /opt/jwt/sign.pub -pubin)"
rm -rf /var/tmp/$uid
logpath=/opt/jwt/jwt_access.log
b2=$(echo -n $jwt | b2sum -l 96 | cut -d' ' -f1 | tr -d '\n')
bstatus=$(echo "get $b2" | redis-cli)
blen=$(expr length "$bstatus")
if [ "$blen" == "0" ]; then
  echo "Not found in cache..."
  exit 1
else
  dateform=$(date +%Y%m%d%H%M%S%N)
  echo "$dateform $b2" >> $logpath
  curl -X GET http://127.0.0.1:5599/admin -H 'Content-Type: application/json' -H "Authorization: Bearer $jwt"
fi
