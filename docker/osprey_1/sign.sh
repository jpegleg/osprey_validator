#!/usr/bin/env bash
uid="/var/tmp/99_$RANDOM$RANDOM"
echo -n $1 > $uid
openssl rsautl -sign -in /var/tmp/$uid -inkey /opt/jwt/sign.key | xxd -p | tr -d '\n'
rm -rf $uid
