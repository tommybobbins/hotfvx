## bme280 sensor report to populate redis
=========================================

The following environment variables need to be set to allow the sensor to report into Redis - default values are shown from the k8s configmap and below from the golang settings

```
  export HOTF_DEBUG="false"
  export HOTF_REDISHOST="redis.redis"
  export HOTF_REDISPORT="6379"
  export HOTF_REDISDB="0"
  export HOTF_REDISTIMEOUT="60"
  export HOTF_REDISTTL="60m"
  export HOTF_LOCATION="bobbins"
  export HOTF_ZONE="inside"
  export HOTF_MULTIPLIER="1"
```

Specification from envconfig (overrides the above if not discovered from the environment variables)

```
    Debug           bool `default:"false"`   
    Redisport       string `default:"6379"`
    Redisdb         int `default:"0"` 
    Redishost       string `default:"redis.redis"`
    Redisttl        time.Duration `default:"60m"`
    Redispassword   string 
    Zone            string `default:"inside"`
    Multiplier      float32 `default:"1.0"`
    Location        string `default:"bobbins"`
```
## Building into Docker and a local repo
========================================

```
docker build . -t docker-registry.docker-registry:32000/bmx-redis:latest; 
docker push docker-registry.docker-registry:32000/bmx-redis; 
docker image prune -f
```

## Deploy to k3s 
================
