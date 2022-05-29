package main

// Reads the relay/heat/state and compares to relay/heat/requestedstate
// Reads the relay/water/state and compares to relay/water/requestedstate
// If relay is 1 and requestedstate is true do nothing
// If relay is 0 and requestedstate is false do nothing
// Otherwise switch the relay
// http://192.168.1.203/relay/0?turn=off
// http://192.168.1.203/relay/0?turn=on


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
    var ton = "?turn=on"
    var toff = "?turn=off"
    var water_relay_on_or_off = false
    var werr = "OK"
    err := envconfig.Process("hotf", &s)
    if err != nil { log.Fatal(err.Error()) }
    if s.Debug == true {
        format := " Debug: %v\n redishost: %s\n redisport: %s\n redisttl: %d\n relayheat: %s\n relaywater: %s\n"
        _, err = fmt.Printf(format, s.Debug, s.Redishost, s.Redisport, s.Redisttl, s.Relayheat, s.Relaywater)
        if err != nil { log.Fatal(err.Error()) }
    }

    ctx := context.Background()

    rdb := redis.NewClient(&redis.Options{
        Addr:	  ""+ s.Redishost +":"+  s.Redisport + "",
        Password: "", // no password set
        DB:		  s.Redisdb ,  // use default DB
    })

    //var water_relay_on_or_off (bool)
    water_rrequested_val, err_wrredis := rdb.Get(ctx, "relay/water/requestedstate").Result()
    if err_wrredis != nil {
        if s.Debug == true { fmt.Printf("relay/water/requestedstate not found %s", err_wrredis) }
        //panic(err_uredis)
    } else {
        if s.Debug == true { print("relay/water/requestedstate = %t", water_rrequested_val) }
        if water_rrequested_val == "true" { 
            water_relay_on_or_off,werr = getrelay(s.Relaywater+ton)
            //water_relay_on_or_off,werr := getrelay(s.Relaywater)
            if werr != "OK" { fmt.Printf("error %v", werr) }
        } else if water_rrequested_val == "false" {
            water_relay_on_or_off,werr = getrelay(s.Relaywater+toff)
            //water_relay_on_or_off,werr := getrelay(s.Relaywater)
            if werr != "OK" { fmt.Printf("error %v", werr) }
        } else { 
            if s.Debug == true { fmt.Printf("Unable to set Relaywater = %s+%s|%s", s.Relaywater, ton, toff) }
            water_relay_on_or_off = false
        }
        if s.Debug == true { fmt.Printf("water_relay_on_or_off %s", water_relay_on_or_off) }
    }
    
}
