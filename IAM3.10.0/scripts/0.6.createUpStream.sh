echo '
_format_version: "3.0"
upstreams:
  - name: example_upstream
    targets:
    - target: httpbun.com:80
      weight: 100
    - target: httpbin.konghq.com:80
      weight: 100
' | deck gateway apply -
