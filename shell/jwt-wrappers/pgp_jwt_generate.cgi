#!/usr/bin/env bash
# The service code is hard coded for the prototype, update to use some authorization data etc. Keep this call local unless TLS is added to the 5599 server.
# The cgi executes the creation of the JWT and encrypts it immediately with the recipient sent as the argument to the program.
# The recipient is going to be a "validator" server identity that will be decrypting the JWT before consumption, so that
# the JWT can be encrypted while in the actual header ;)

blobjwt=$(curl http://127.0.0.1:5599/login -d '{"identity": "root@localhost", "service_id": "3ec85f59dce67fc936d7f1e63466aea3b6c"}' -H 'Content-Type: application/json'  | cut -c14-616 | cut -d '|' -f2 )

jwt=$(echo -n $blobjwt | gpg -e -r $1 --armor | base64 | tr -d '\n')
b2=$(echo -n $blobjwt | b2sum | cut -c1-24 | tr -d '\n')
echo -n "$jwt" | redis-cli -x SET $b2
redis-cli EXPIRE $b2 60 >/dev/null 2>&1

echo "$jwt"
