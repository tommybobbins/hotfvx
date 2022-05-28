docker build . -t docker-registry.docker-registry:32000/sensor-redis:latest; docker push docker-registry.docker-registry:32000/sensor-redis; docker image prune -f
