export KONG_ADMIN_HOST=localhost
export KONG_ADMIN_PORT=8000
docker run -i \
-v $(pwd):/deck \
kong/deck --kong-addr http://$KONG_ADMIN_HOST:$KONG_ADMIN_PORT --headers kong-admin-token:KONG_ADMIN_TOKEN -o /deck/kong.yaml dump
