# OSPREY 1 🦅

End to End protection abstraction prototype on top of JWT for zero-trust service modelling.

This is a service wrapper, not a separate service. The microservice goes within or otherwise replaces the royal_blobs_jwt_service.

This means that each client has TLS auth to the individual container, using a token for access specific to that container.

If used with Kubernetes Deployments, the Replicas will need to be 1 per instance as each container does cache based authorization. If you want to scale it horizontal with replicas, then the cache needs to be moved out and into a shared cache or cache consolidation handled so that each replica knows which JWTs are active, and wrap more security around that interaction. Alternatively, the cache could be removed and the wrapper rearranged to not use it. The JWTs will still expire normally without the Redis cache ;)

Each token is valid for 60 seconds before it expires in both JWT form and in Redis cache.

The client never sees or uses a regular JWT, but instead passes a signed blob that contains the JWT back to the service for access.

Getting a signed token via authenticated TLS:

```
curl -E myclientkeycert.pem https://microservice_a/create.cgi
935d01c96d86a8ffe76b55e1c29259f887b7e787ff8e412077852a9f130f7f277a497c3a8cc3f0e4fbb2f1f600cf17372f3d33a1ab05f8c0764ee3d394884721e91cca3a0b690bff8cbde233aaba8eac1cf9aa6e234e04ee9d2da08d864d99e15792faa07bc80bdccefc49012b108b71886eba00a058a6963bb28bdc9c42b508fdff2266160e316ecc5360ed452ea273971af8e1aadf288cd2cc0423ed7c7fc68e7e8b3f59166b0ac8cc8fad83cff55f66c6945eb711a4df53e0bc88c4fd78fa5b65ab12fca8922e32853b40b85aeeb093ae5b657ddd1679c6930a29ea4b725c37506bef1dc7a948d3d800dfa5952e4bab44011ca42b2eb66863c0093fceebda
```

Using the signed token to get access to the demo royal blobs service:

```
curl -E myclientkeycert.pem -k https://microservice_a/validate.cgi?935d01c96d86a8ffe76b55e1c29259f887b7e787ff8e412077852a9f130f7f277a497c3a8cc3f0e4fbb2f1f600cf17372f3d33a1ab05f8c0764ee3d394884721e91cca3a0b690bff8cbde233aaba8eac1cf9aa6e234e04ee9d2da08d864d99e15792faa07bc80bdccefc49012b108b71886eba00a058a6963bb28bdc9c42b508fdff2266160e316ecc5360ed452ea273971af8e1aadf288cd2cc0423ed7c7fc68e7e8b3f59166b0ac8cc8fad83cff55f66c6945eb711a4df53e0bc88c4fd78fa5b65ab12fca8922e32853b40b85aeeb093ae5b657ddd1679c6930a29ea4b725c37506bef1dc7a948d3d800dfa5952e4bab44011ca42b2eb66863c0093fceebda
royal_blobs_jwt_service ADMIN 2
```

Where "royal_blobs_jwt_service ADMIN 2" is returned would be the microservice or data being requested, the text is a placeholder to represent the microservice response.

You may be thinking, this is crazy, this breaks all our wonderful APIs! Yes, that is the point.

All the API functions are trapped behind authenticated wrappers. In order to regain API functionality and still use this technique without breaking the benefits gained, additional functionality to pass in the API request would be included in the .cgi files and client instructions.

Examples with some extra context API mappings:

```
$ curl -E myclientkeycert.pem -k https://microservice_a/validate.cgi?935d01c96d86a8ffe76b55e1c29259f887b7e787ff8e412077852a9f130f7f277a497c3a8cc3f0e4fbb2f1f600cf17372f3d33a1ab05f8c0764ee3d394884721e91cca3a0b690bff8cbde233aaba8eac1cf9aa6e234e04ee9d2da08d864d99e15792faa07bc80bdccefc49012b108b71886eba00a058a6963bb28bdc9c42b508fdff2266160e316ecc5360ed452ea273971af8e1aadf288cd2cc0423ed7c7fc68e7e8b3f59166b0ac8cc8fad83cff55f66c6945eb711a4df53e0bc88c4fd78fa5b65ab12fca8922e32853b40b85aeeb093ae5b657ddd1679c6930a29ea4b725c37506bef1dc7a948d3d800dfa5952e4bab44011ca42b2eb66863c0093fceebda/things/can/go/down/here/
royal_blobs_jwt_service ADMIN 2
$ curl -E myclientkeycert.pem -k https://microservice_a/validate.cgi?935d01c96d86a8ffe76b55e1c29259f887b7e787ff8e412077852a9f130f7f277a497c3a8cc3f0e4fbb2f1f600cf17372f3d33a1ab05f8c0764ee3d394884721e91cca3a0b690bff8cbde233aaba8eac1cf9aa6e234e04ee9d2da08d864d99e15792faa07bc80bdccefc49012b108b71886eba00a058a6963bb28bdc9c42b508fdff2266160e316ecc5360ed452ea273971af8e1aadf288cd2cc0423ed7c7fc68e7e8b3f59166b0ac8cc8fad83cff55f66c6945eb711a4df53e0bc88c4fd78fa5b65ab12fca8922e32853b40b85aeeb093ae5b657ddd1679c6930a29ea4b725c37506bef1dc7a948d3d800dfa5952e4bab44011ca42b2eb66863c0093fceebda?things?can?go?here?too
royal_blobs_jwt_service ADMIN 2
```

In addition to the forced expiration and tamper-proofing, individual clients can be removed by removing the corresponding private ca cert in auth.pem.

<h4>Each client gets its own secret CA sign during set up, not included here</h4>

Client generates private key and CSR.

The PKI signs the CSR with a unique key, returning the certificate to be paired with the key on the client (myclientkeycert.pem in the example).

The CA key can be disposable as only the CA cert is needed appended to auth.pem which gets put within Osprey in /etc/auth.pem during image build.


While the royal_blobs_jwt_service log goes to STDOUT and thus to the docker/kubernetes logs, there is also useful data inside the container. 

The log file /opt/jwt/jwt_access_check.log containers a record of `time b2truncatedhex b64b2` whenever a JWT is used.
This jwt_access_check.log can be used for event auditing etc.

The b64 encoded BLAKE2 has a TTL of 9 days for audit purposes, but the shorter truncated hex version is the "live" version that is expired along with the token at 60 seconds.

```
root@fd29cf75d923:/opt/jwt# cat jwt_access_check.log
20220410060157453253643 17beff83340fb909e2876ec0 F77/gzQPuQnih27AJg40pdt/KjqpWQcWKnPHSMDPEqgRzH6hwjChUbrNkovyFiIYETmqhickmh6EXDaWIYsuGw==
root@fd29cf75d923:/opt/jwt# redis-cli
127.0.0.1:6379> keys *
1) "F77/gzQPuQnih27AJg40pdt/KjqpWQcWKnPHSMDPEqgRzH6hwjChUbrNkovyFiIYETmqhickmh6EXDaWIYsuGw=="
2) "17beff83340fb909e2876ec0"
127.0.0.1:6379>
```

Here is an example of the main log data in STDOUT:

```
AH00558: apache2: Could not reliably determine the server's fully qualified domain name, using 172.17.0.2. Set the 'ServerName' directive globally to suppress this message
httpd not running, trying to start
============================
| royal_blobs_jwt_service  |
============================
-> Symmetric HS512 JWT
-> base64 encoded BLAKE2
-> UUID version 4 tracking
ADDED~RSA~signed~blob~format
Starting Warp listener on the loopback device, port 5599...
2022-04-10 06:01:46.163864109 UTC - royal_blobs_jwt_service INFO - START JWT usage UID a2e8eda7-2f59-465f-9a36-7b7559d0698c
2022-04-10 06:01:46.164358651 UTC - royal_blobs_jwt_service INFO - a2e8eda7-2f59-465f-9a36-7b7559d0698c - base64 BLAKE2: "F77/gzQPuQnih27AJg40pdt/KjqpWQcWKnPHSMDPEqgRzH6hwjChUbrNkovyFiIYETmqhickmh6EXDaWIYsuGw=="
2022-04-10 06:01:57.474179728 UTC - royal_blobs_jwt_service INFO - admin resource provided
```
