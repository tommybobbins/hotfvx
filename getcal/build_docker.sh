VERSION="0.01"

#go mod init learn
#go mod tidy

#go: finding module for package periph.io/x/devices/bmxx80
#go: finding module for package periph.io/x/conn/i2c/i2creg
#go: finding module for package periph.io/x/conn/physic
kubectl delete -f 32*.yml
#CGO_ENABLED=0 go build -o relay-decider *.go
docker build . -t docker-registry.docker-registry:32000/proc-cal:${VERSION}; docker push docker-registry.docker-registry:32000/proc-cal:${VERSION}; docker image prune -f
kubectl create -f 32*.yml
