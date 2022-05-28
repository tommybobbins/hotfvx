#!/bin/bash
VERSION="0.05"
#go mod init learn
#docker build . -t docker-registry.docker-registry:32000/sensor-redis:latest; docker push docker-registry.docker-registry:32000/sensor-redis; docker image prune -f
#go mod tidy

#go: finding module for package periph.io/x/devices/bmxx80
#go: finding module for package periph.io/x/conn/i2c/i2creg
#go: finding module for package periph.io/x/conn/physic
#redis_bm__80.go:7:5: module periph.io/x/conn@latest found (v0.0.2), but does not contain package periph.io/x/conn/i2c/i2creg
#redis_bm__80.go:8:5: module periph.io/x/conn@latest found (v0.0.2), but does not contain package periph.io/x/conn/physic
#redis_bm__80.go:9:5: module periph.io/x/devices@latest found (v0.0.1), but does not contain package periph.io/x/devices/bmxx80
#docker build -t golangbmp .
kubectl create -f ./30-namespace.yaml
cd Docker
CGO_ENABLED=0 go build -o bmx *.go
docker build . -t docker-registry.docker-registry:32000/bmx-redis:${VERSION}
docker push docker-registry.docker-registry:32000/bmx-redis:${VERSION}
docker image prune -f
cd ../
helm upgrade --install bmx-redis ./bmx-redis --debug -n sensorredis
