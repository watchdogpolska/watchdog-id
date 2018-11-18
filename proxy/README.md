# Watchdog-ID@Proxy

Proxy designed to enforce OAuth 2.0 authentication on legacy systems. The application allows you to relieve the implementation of OAuth 2.0 authentication in any application.

Proxy in no way controls operations performed in a secured application, in particular, it does not authorize operations.

## HTTP headers

After successful authentication, it redirects all requests to the target application without modification, excluding adding following HTTP headers:

| Name | Description
| -------- | -----------
| ```x-watchdog-authenticated-user-id``` | unique identifier of user. A value that is not digitally signed in a special way.
| ```x-watchdog-authenticated-user-email``` | e-mail address of user. A value that is not digitally signed in a special way.
| ```REMOTE_USER``` | e-mail address of authenticated user. A value that is not digitally signed in a special way.
| ```x-watchdog-jwt-assertion``` | JWT signed payload to authenticate proxied request

## JWT payload

The request in the ```x-watchdog-jwt-assertion``` header contains a JWT payload that allows successful request authentication by verification of JWT claim. The application should check the parameter in detail and reject incorrect requests, in particular by verifying:
- the presence of the header,
- correctness of value as JWT payload
- signing the request with the key published at the address "/auth_keys"
- all claim values, and at least ```exp```,```iat```, ```email```, ```aud```, ```iss```

### Claim values

Below are presented the values available in the JWT token, as well as the method of their verification:

| key 	    | value 	            | verification |
|-----------|-----------------	|-----------------------------------------------------------------------------------------
| ```exp``` | Expiration time 	| Must be in the future. The time is measured in seconds since the UNIX epoch.
| ```iat``` | Issued-at time 	| Must be in the past. The time is measured in seconds since the UNIX epoch.
| ```aud``` | Audience 	| Must be a string with value match to target service hostname.
| ```iss ```| Issuer 	| Must be a string with value match to proxy service name defined in configuration files.
| ```sub ```| Subject – the unique, stable identifier for the user.	| Use this value instead of the ```x-watchdog-authenticated-user-id``` header. 
| ```email ```| User e-mail address	| It should match the user ID created in a separate system. Use this value instead of the ```x-watchdog-authenticated-user-email``` header.

## Communication security

The following steps should be taken on app side to ensure the safety of communication:
- the source IP address of the request should be only the proxy server address
- IP filtering should be done on the highest layer that is possible
- ```x-watchdog-jwt-assertion``` header values should be verified and correct
- any information that has not been digitally signed should not be considered safe
- all digital signatures should be verified and correct
