VERSION="0.02"
cd Docker
docker build . -t docker-registry.docker-registry:32000/calread-redis:${VERSION}; docker push docker-registry.docker-registry:32000/calread-redis:${VERSION}; docker image prune -f
cd ../
helm upgrade --install  calendarread-redis ./calendarread-redis --debug -n sensorredis
