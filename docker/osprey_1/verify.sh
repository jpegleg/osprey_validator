#!/usr/bin/env bash
uid=100_$RANDOM$RANDOM
echo -n $1 | xxd -r -p > /var/tmp/$uid
openssl rsautl -verify -in /var/tmp/$uid -inkey /opt/jwt/sign.pub -pubin
