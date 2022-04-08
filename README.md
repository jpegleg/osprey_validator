# osprey_validator 🐟 🦅
<h3>a collection of prototype service wrappers for added client validations</h3>

<h2>JWT area:</h2>
Rather than having the JWT consumer exposed externally, expose a wrapper service that does additional policy validation and decryption, for hardening on top of JWT services.
Token creating systems can also have wrappers, encrypting/signing the JWT before handing it back to the client to make it tamper proof, so that the expiration value of the JWT cannot be edited on the client side.


<h4>For JWT generation and validation starting point (as used in the prototypes) see https://github.com/jpegleg/royal_blobs_jwt_service</h4>

<h4>For adding layers of protecting and doing data signing and verifying that also uses Redis cache controls, see https://github.com/jpegleg/signer-daemon</h4>
