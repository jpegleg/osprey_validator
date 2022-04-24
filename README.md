# osprey_validator 🐟 🦅
<h3>a collection of prototype service wrappers for added client validations</h3>

<h2>JWT area:</h2>
Rather than having the JWT consumer exposed externally, expose a wrapper service that does additional policy validation and decryption, for hardening on top of JWT services.
Token creating systems can also have wrappers, encrypting/signing the JWT before handing it back to the client to make it tamper proof, so that the expiration value of the JWT cannot be edited on the client side.

The approach uses mTLS (client auth) in HAProxy, letting valid client certificates fetch the signed tokens, which then can be used with the (demo service) for 60 seconds. The token is tamper proof, unlike plain JWT.

<h3>
With this approach, the JWT is no longer treated directly as a JWT, but instead is treated as a signed blob with custom processing, then treated as a JWT under the hood.
</h3>

<h4>For JWT generation and validation starting point (as used in the prototype osprey 1) see https://github.com/jpegleg/royal_blobs_jwt_service</h4>

<h4>For JWT generation and validation starting point + program execution template (as used in the prototype osprey 2) see https://github.com/jpegleg/fixadm</h4>

<h3>Osprey 1</h3>

Compile the royal_blobs_jwt_service with cargo, put the binary in the Docker build dir with this is a working demonstration:

https://github.com/jpegleg/osprey_validator/tree/main/docker/osprey_1

<h4>The demo includes demo private keys, don't use those for real stuff, only demo.</h4>


<h3>Osprey 2</h3>

Compile the fixadm_service with cargo, put the binary in the Docker build dir along with the demo files and generated files:

https://github.com/jpegleg/osprey_validator/tree/main/docker/osprey_2

<h4>The example execututions and HMAC need to be adjusted as needed per use case</h4>
