#!/usr/bin/env bash
export GPG_TTY=$(tty)
ejwt=$1
logpath=/opt/jwt/jwt_access.log
touch $logpath || exit 1
# JWT issuer service has the public PGP key, encrypting the JWT before return to client
# client sends encrypted JWT to service, this wrapper decrypts it then validates in cache
# before use
jwt=$(echo -n $ejwt | base64 -d | gpg -d --passphrase=PASSPHRASEHERE)
b2=$(echo -n $jwt | b2sum | cut -c1-24 | tr -d '\n')
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
