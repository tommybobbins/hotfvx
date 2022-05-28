VERSION="0.08"
cd Docker
CGO_ENABLED=0 GO111MODULE=on go build -o decide-water decide-water.go
docker build . -t docker-registry.docker-registry:32000/decide-water:${VERSION}; docker push docker-registry.docker-registry:32000/decide-water:${VERSION}; docker image prune -f
cd ../
helm upgrade --install decide-water ./decide-water --debug -n sensorredis
