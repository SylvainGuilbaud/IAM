# for _ in {1..6}; do 
#   curl http://localhost:8000/anything
# done

# for _ in {1..6}; do 
#   curl http://localhost:8000/anything -H 'apikey: hello_world'
# done

for _ in {1..6}; do 
  curl http://localhost:8000/anything -H 'apikey: test'
done