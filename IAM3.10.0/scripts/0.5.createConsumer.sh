echo '
_format_version: "3.0"
consumers:
  - username: luka
    keyauth_credentials:
    - key: top-secret-key
' | deck gateway apply -
