#!/usr/bin/env bash

jwt=$1
logpath=/opt/jwt/jwt_access.log
touch $logpath || exit 1
b2=$(echo -n $jwt | b2sum | xxd -r -p | base64 | tr -d '\n')

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
