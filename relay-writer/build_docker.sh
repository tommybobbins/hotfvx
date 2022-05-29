VERSION="0.01"

#go mod init learn
#go mod tidy

#go: finding module for package periph.io/x/devices/bmxx80
#go: finding module for package periph.io/x/conn/i2c/i2creg
#go: finding module for package periph.io/x/conn/physic
cd Docker
CGO_ENABLED=0 go build -o relay-writer *.go
docker build . -t docker-registry.docker-registry:32000/relay-writer:${VERSION}; docker push docker-registry.docker-registry:32000/relay-writer:${VERSION}; docker image prune -f
cd ../
helm upgrade --install relay-writer ./relay-writer --debug -n sensorredis
