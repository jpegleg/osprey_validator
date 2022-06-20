#!/usr/bin/env bash
echo "Content-Type: text/html";

# Not a safe uploader, at least the client side uses mTLS.
# And at least this is limited size by URI context and it doesn't catalog...
# The idea is that each service would have their own instance, but
# if multiple people try to use upload.cgi on the same instance
# right after one another, the second person will likely overwrite
# the CSR with their own before the first user performs a sign.
# This is a TOCTOU situation, in fact, a great demo of TOCTOU problems :)
# The TOCTOU is solved by moving the sign function within upload so 
# that the operation is protected by the locking :)
uploada () {
  mkdir /opt/jwt/_active_lockdir_ || exit 1
  :>/opt/jwt/webtmp/CSR.b64 2>/dev/null
  while read line; do
    echo "$line" >> /opt/jwt/webtmp/CSR.b64
  done<&0
  cat /opt/jwt/webtmp/CSR.b64 | base64 -d > /opt/jwt/webtmp/CSR.csr
  rmdir /opt/jwt/_active_lockdir_
}

listener () {
  echo "$1" | uploada 
}

errout () {
  echo "CSR UPLOAD EXIT ERROR $?"
  exit 1
}
echo
echo "$(listener "$1" || errorout)"
echo
