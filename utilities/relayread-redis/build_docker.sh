#!/bin/bash
kubectl create -f ./30-namespace.yaml
cd Docker
CGO_ENABLED=0 go build -o readrelay-redis *.go
docker build . -t docker-registry.docker-registry:32000/relayread-redis:${VERSION}; docker push docker-registry.docker-registry:32000/relayread-redis:${VERSION}; docker image prune -f
cd ../
helm upgrade --install relayread-redis ./relayread-redis --debug -n sensorredis
VERSION="0.05"

#go mod init learn
#go mod tidy

#go: finding module for package periph.io/x/devices/bmxx80
#go: finding module for package periph.io/x/conn/i2c/i2creg
#go: finding module for package periph.io/x/conn/physic
