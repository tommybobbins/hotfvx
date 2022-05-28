VERSION="0.02"
kubectl delete -f 32-calread-redis.yml 
docker build . -t docker-registry.docker-registry:32000/calread-redis:${VERSION}; docker push docker-registry.docker-registry:32000/calread-redis:${VERSION}; docker image prune -f
kubectl create -f 32-calread-redis.yml 
