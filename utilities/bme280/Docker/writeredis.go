package main

import (
    "fmt"
    "log"
    "time"
    "math"
    "github.com/kelseyhightower/envconfig"
    "context"
    "github.com/go-redis/redis/v8"
)

type RSpecification struct {
    Debug           bool `default:"false"`   
    Redisport       string `default:"6379"`
    Redisdb         int `default:"0"` 
    Redishost       string `default:"redis.redis"`
    Redisttl        time.Duration `default:"60m"`
    Redispassword   string 
    Zone            string `default:"inside"`
    Multiplier      float32 `default:"1.0"`
    Location        string `default:"bobbins"`
}

func main() {
    var s RSpecification
    err := envconfig.Process("hotf", &s)
    if err != nil {
        log.Fatal(err.Error())
    }
    if s.Debug == true {
        format := " Debug: %v\n redishost: %s\n redisport: %s\n multiplier: %f\n redisttl: %d\n"
        _, err = fmt.Printf(format, s.Debug, s.Redishost, s.Redisport, s.Multiplier, s.Redisttl)
        if err != nil {
            log.Fatal(err.Error())
        }
    }

    ctx := context.Background()

    rdb := redis.NewClient(&redis.Options{
        Addr:	  ""+ s.Redishost +":"+  s.Redisport + "",
        Password: "", // no password set
        DB:		  s.Redisdb ,  // use default DB
    })


    temperature,pressure := readsensor()
    if math.Mod(temperature,1.0) == 0.0 {
        fmt.Printf("\nThere was a problem calling the producer :-(\n%8f\n", temperature)
    }

    if s.Debug == true {
        fmt.Printf("%8f %8d \n",temperature, pressure)
    }

        err_temperature := rdb.Set(ctx, "sensor/" + s.Location + "/temperature", temperature, 0).Err()
        err_temperature_expire := rdb.Expire(ctx, "sensor/" + s.Location + "/temperature", s.Redisttl).Err()
        if err_temperature != nil {
           panic(err_temperature)
        }
        if err_temperature_expire != nil {
           panic(err_temperature_expire)
        }
        err_pressure := rdb.Set(ctx, "sensor/" + s.Location + "/pressure", (pressure/1E+11), 0).Err()
        err_pressure_expire := rdb.Expire(ctx, "sensor/" + s.Location + "/pressure", s.Redisttl).Err()
        if err_pressure != nil {
           panic(err_pressure)
        }
        if err_pressure_expire != nil {
           panic(err_pressure_expire)
        }

    //val, err_sensor := rdb.Get(ctx, "sensor/" + s.Location + "/temperature").Result()
    //    if err_sensor != nil {
    //        panic(err_sensor)
    //}

}
