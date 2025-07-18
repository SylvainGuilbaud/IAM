echo '
_format_version: "3.0"
services:
  - name: example_service
    url: https://httpbin.konghq.com
' | deck gateway apply -
