echo '_format_version: "3.0"
routes:
 - name: example-route
   service: 
     name: example-service
   paths:
     - "/"' | deck gateway apply