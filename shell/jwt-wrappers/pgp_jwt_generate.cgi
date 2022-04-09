#!/usr/bin/env bash
# The service code is hard coded for the prototype, update to use some authorization data etc. Keep this call local unless TLS is added to the 5599 server.
blobjwt=$(curl http://127.0.0.1:5599/login -d '{"identity": "root@localhost", "service_id": "3ec85f59dce67fc936d7f1e63466aea3b6c"}' -H 'Content-Type: application/json' | cut -d':' -f2 | cut -d'"' -f2 | tr -d '\n')
# The cgi executes the creation of the JWT and encrypts it immediately with the recipient sent as the argument to the program.
# The recipient is going to be a "validator" server identity that will be decrypting the JWT before consumption, so that
# the JWT can be encrypted while in the actual header ;)
jwt=$(echo $blobjwt | cut -d'|' -f2 | gpg -e -r $1 --armor | base64 | tr -d '\n')

blob=$(echo $blobjwt | cut -d'|' -f1)
b2=$(echo $blobjwt | cut -d'|' -f2 | b2sum | xxd -r -p | base64)

echo "$jwt|$blob" | redis-cli -x SET $b2 >/dev/null 2>&1
redis-cli EXPIRE $b2 60 >/dev/null 2>&1

echo "$jwt|$blob"
