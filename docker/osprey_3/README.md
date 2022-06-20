# OSPREY 3 🦅

End to End protection abstraction prototype on top of JWT for zero-trust service modelling.

Osprey 3 builds on top of osprey 2, adding in an ephemeral CA for mTLS client certificate signing, a PKI component that also requires mTLS to access.

The binary used in Osprey 3 is very similar to the ones we have used in Osprey 2 and 1, see https://github.com/jpegleg/three_pki


There are two other programs not included in this osprey validator repo that are required for the docker build:

signcsr (to provide client identity, as executed by vuser2.cgi)
collect_auth_pem (to provide all identities, as executed by vuser1.cgi)

The "three_pki" prototype has example/demos of signcsr and colelct_auth_pem.
