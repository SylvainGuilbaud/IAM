### activate Prometheus plugin in Kong
curl -s -X POST http://localhost:8001/plugins \
     --data "name=prometheus"
