echo '
_format_version: "3.0"
routes:
  - name: example_route
    service:
      name: example_service
    paths:
    - "/mock"
' | deck gateway apply -
