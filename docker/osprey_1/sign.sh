#!/usr/bin/env bash
uid=99_"$RANDOM$RANDOM"
echo -n $1 > /var/tmp/$uid
openssl rsautl -sign -in /var/tmp/$uid -inkey /opt/jwt/sign.key | xxd -p | tr -d '\n'
rm -rf /var/tmp/$uid
