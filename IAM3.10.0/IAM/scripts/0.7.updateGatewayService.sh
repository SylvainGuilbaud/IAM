echo '
_format_version: "3.0"
services:
  - name: example_service
    host: example_upstream
' | deck gateway apply -
