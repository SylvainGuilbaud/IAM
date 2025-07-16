## send 10 times the same request to the mock server

## collect the target response to check the load balancing
## if the response contains bun.com add 1 to BUN 
## if the response contains httpbin.konghq.com add 1 to HTTPBIN
echo "Testing load balancing with apikey header"

BUN=0
HTTPBIN=0   
for i in {1..10}; do
  echo "Request #$i"
  RESPONSE=$(curl -s $KONNECT_PROXY_URL/mock/anything --header "apikey:top-secret-key")
  echo $RESPONSE | grep -i -A1 '"host"'
  if echo $RESPONSE | grep -q "httpbun.com"; then
    BUN=$((BUN + 1))
  elif echo $RESPONSE | grep -q "httpbin.konghq.com"; then
    HTTPBIN=$((HTTPBIN + 1))
  fi
done    
echo "BUN responses: $BUN"
echo "HTTPBIN responses: $HTTPBIN"


