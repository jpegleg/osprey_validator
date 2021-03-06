# OSPREY 2 🦅

End to End protection abstraction prototype on top of JWT for zero-trust service modelling.

Unlike OSPREY 1, OSPREY 2 provides an example service approach with fixed program execution.
This allows service mappings to return the output of a non-daemon program. 

The example uses shell scripts called proc100 and flush-hydrate.

Demo proc100 returns a json file `cat data.json` from the working directory of the fixadm service.

The demo flush-hydrate deletes all keys in redis/0 and populates redis from a flatfile called initial.flat.

The demo service is here: https://github.com/jpegleg/fixadm

The demo fixadm also includes proc100 and flush-hydrate examples.

Compile it and place the resulting binary in pwd of the Dockerfile build :)

Another difference between osprey 2 and osprey 1 is that osprey 2 includes a key and certificate demo generator called generate_crypt.
The generate_crypt is for demo purposes.


Here is a way to display the Subjects from each auth.pem entry. Generally there would be one entry per client source, each client having a one-time unique auth CA.

```
while openssl x509 -noout -text; do :; done < auth.pem | grep "Subject:"
```


Osprey 2 also expands the default haproxy.cfg logging by two additional audit elements of TLS version and session duration. The HAProxy logging is easy enough to adjust. 

<b>WARNING:</b> Logging the URI (request) will expose a second layer authentication element! For this reasons, the request logging is not included by default. The URI may contain sensitive data, so best leave it out. Luckily it is a second layer, the mTLS still protects even if the request is logged, but we don't need to log that data so let's not.

<b>WARNING:</b> The flush-hydrate example isn't a safe program because it could be used to deny access to the service, if the drain is continuously ran it could prevent valid user auth! Likely time locks should be used to limit this function if actually desired, or more realistically the function might empty audit entries (the B64 BLAKE3 keys) as those have a 30 day TTL and are used for extra audit only.
