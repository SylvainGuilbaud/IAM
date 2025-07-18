echo '
_format_version: "3.0"
plugins:
  - name: rate-limiting
    config:
      minute: 5
      policy: local
' | deck gateway apply -
