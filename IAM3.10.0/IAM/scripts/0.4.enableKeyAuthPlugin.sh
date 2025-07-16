echo '
_format_version: "3.0"
plugins:
  - name: key-auth
    config:
      key_names:
      - apikey
' | deck gateway apply -
