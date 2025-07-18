### enter username and password, then encode username:password in base64 format
#!/bin/bash

read -p "Nom d'utilisateur : " username
read -s -p "Mot de passe : " password
echo

# Concatène username:password puis encode en base64
credentials="${username}:${password}"
encoded=$(echo "$credentials" | base64)

echo "Base64 : $encoded"

echo $encoded | base64 --decode