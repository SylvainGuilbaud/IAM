for _ in {1..6}; do
  curl  -i $KONNECT_PROXY_URL/mock/anything \
       -H "apikey:top-secret-key" 
  echo
done
