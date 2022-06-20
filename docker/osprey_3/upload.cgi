#!/usr/bin/env bash
echo "Content-Type: text/html";

# ensure the locking is enforced across the signcsr function too...
uploada () {
  mkdir /opt/jwt/webtmp/_active_lockdir_ || exit 1
  :>/opt/jwt/webtmp/CSR.b64 2>/dev/null
  while read line; do
    echo "$line" >> /opt/jwt/webtmp/CSR.b64
  done<&0
  cat /opt/jwt/webtmp/CSR.b64 | base64 -d > /opt/jwt/webtmp/CSR.csr
  rmdir /opt/jwt/webtmp/_active_lockdir_
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
