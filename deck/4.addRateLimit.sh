echo '_format_version: "3.0"
plugins:
 - name: rate-limiting
   service: example-service
   config:
     minute: 5
     limit_by: consumer
     policy: local' | deck gateway apply