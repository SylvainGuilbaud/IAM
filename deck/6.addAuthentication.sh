echo '_format_version: "3.0"
plugins:
 - name: key-auth
   service: example-service
consumers:
 - username: alice
   keyauth_credentials:
     - key: hello_world' | deck gateway apply