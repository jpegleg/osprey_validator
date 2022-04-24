# OSPREY 2 🦅

End to End protection abstraction prototype on top of JWT for zero-trust service modelling.

Unlike OSPREY 1, OSPREY 2 provides an example service approach with fixed program execution.
This allows service mappings to return the output of a non-daemon program. 

The example uses shell scripts called proc100 and flush-hydrate.

Demo proc100 returns a json file `cat data.json` from the working directory of the fixadm service.

The demo flus-hydrate deletes all keys in redis/0 and populates redis from a flatfile called initial.flat.

The demo service is here: https://github.com/jpegleg/fixadm

The demo fixadm also includes proc100 and flush-hydrate examples.

Compile it and place the resulting binary in pwd of the Dockerfile build :)
