echo '
_format_version: "3.0"
plugins:
  - name: proxy-cache
    config:
      request_method:
      - GET
      response_code:
      - 200
      content_type:
      - application/json
      cache_ttl: 30
      strategy: memory
' | deck gateway apply -
