#!/usr/bin/env bash
uid="/var/tmp/100_$RANDOM$RANDOM"
echo -n $1 | xxd -r -p > $uid
openssl rsautl -verify -in /var/tmp/$uid -inkey /opt/jwt/sign.pub -pubin
rm -f $uid
