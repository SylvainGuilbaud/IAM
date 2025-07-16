#!/bin/bash
# This script is used to validate caching in Kong Gateway.  
for i in {1..10}; do
  echo "Request #$i"
  RESPONSE=$(curl -s -i $KONNECT_PROXY_URL/mock/anything --header "apikey:top-secret-key" | grep -E 'X-Cache')
  echo $RESPONSE 
  sleep 0.1
done    

