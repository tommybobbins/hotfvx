package main

import (
    "fmt"
    "log"
    "time"
    "github.com/go-redis/redis/v8"
    "github.com/kelseyhightower/envconfig"
    "context"
)

type RSpecification struct {
    Debug           bool `default:"false"`   
    Redisport       string `default:"6379"`
    Redisdb         int `default:"0"` 
    Redishost       string `default:"redis.redis"`
    Redisttl        time.Duration `default:"60m"`
    Redispassword   string 
    Relayheat       string `default:"http://192.168.1.213/relay/0"`
    Relaywater      string `default:"http://192.168.1.56/relay/0"`
}

func main() {
    var s RSpecification
    err := envconfig.Process("hotf", &s)
    if err != nil {
        log.Fatal(err.Error())
    }
    if s.Debug == true {
        format := " Debug: %v\n redishost: %s\n redisport: %s\n redisttl: %d\n relayheat: %s\n relaywater: %s\n"
        _, err = fmt.Printf(format, s.Debug, s.Redishost, s.Redisport, s.Redisttl, s.Relayheat, s.Relaywater)
        if err != nil {
            log.Fatal(err.Error())
        }
    }
    //var heat_relay_on_or_off = "error"
    //var water_relay_on_or_off = "error"

    heat_relay_on_or_off,herr := getrelay(s.Relayheat)
    water_relay_on_or_off,werr := getrelay(s.Relaywater)
    if s.Debug == true {fmt.Printf("heat_relay_on_or_off: %t\n heat_error: %s\n water_relay_on_or_off: %t\n water_error: %s\n ", heat_relay_on_or_off, herr, water_relay_on_or_off, werr)}

    ctx := context.Background()

    rdb := redis.NewClient(&redis.Options{
        Addr:	  ""+ s.Redishost +":"+  s.Redisport + "",
        Password: "", // no password set
        DB:		  s.Redisdb ,  // use default DB
    })
    
    if herr != "OK" {
        if s.Debug == true {print("Heat Relay not found")}
    } else {
        if s.Debug == true {fmt.Printf("Heat Relay: %v \n",heat_relay_on_or_off)}
        err_heatrelay := rdb.Set(ctx, "relay/heat/state", heat_relay_on_or_off, 0).Err()
        if err_heatrelay != nil {
           panic(err_heatrelay)
        } else {
            if s.Debug == true {print("Heat relay state sent to redis\n")}
        } 
    }
    if werr != "OK" {
        if s.Debug == true {print("Water Relay not found")}
    } else {
        if s.Debug == true {fmt.Printf("Water Relay: %v \n",water_relay_on_or_off)}
        err_waterrelay := rdb.Set(ctx, "relay/water/state", water_relay_on_or_off, 0).Err()
        if err_waterrelay != nil {
           panic(err_waterrelay)
        } else {
            if s.Debug == true {print("Water relay state sent to redis\n")}
        } 
    }

}
