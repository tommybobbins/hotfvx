package main

import (
    "fmt"
    "log"
    "time"
    //"math"
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
}

func main() {
    var s RSpecification
    err := envconfig.Process("hotf", &s)
    if err != nil {
        log.Fatal(err.Error())
    }
    if s.Debug == true {
        format := " Debug: %v\n redishost: %s\n redisport: %s\n redisDb: %v\n redisttl: %d\n"
        _, err = fmt.Printf(format, s.Debug, s.Redishost, s.Redisport, s.Redisdb, s.Redisttl)
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

    water_cal_val, err_credis := rdb.Get(ctx, "calendar/water/requestedstate").Result()
    if err_credis != nil {
        if s.Debug == true { fmt.Printf("calendar/water/requestedstate not found", err_credis) }
        water_cal_val = "false" 
    } else {
        if s.Debug == true { print("Water_cal_val = %t", water_cal_val) }
    }
    if water_cal_val != "" {
        fmt.Println("Water Cal Value: %v\n", water_cal_val)
    } else {
        if s.Debug == true { print("calendar/water/requestedstate not found") }
    }
    water_user_val, err_uredis := rdb.Get(ctx, "user/water/requestedstate").Result()
    if err_uredis != nil {
        if s.Debug == true { fmt.Printf("user/water/requestedstate not found", err_uredis) }
        water_user_val = "false" 
        //panic(err_uredis)
    } else {
        if s.Debug == true { print("Water_user_val = %t", water_user_val) }
    }
    if water_user_val != "" {
        if s.Debug == true { fmt.Println("User Calendar Value: %v\n", water_user_val) }
    } else {
        if s.Debug == true { print("User Override not found") }
    }
    var requested_state = "error"
    if water_user_val == "true" || water_cal_val == "true" {
       requested_state = "true"
    // So both water_cal_val and water_user_val must both be false
    } else {
       requested_state = "false"
    }
    if requested_state != "error" {
       if s.Debug == true {fmt.Println("Requested Water State: %t\n", requested_state)}
    }  else { 
       if s.Debug == true {fmt.Println("Requested State is in error: %s\n", requested_state)}
    }
    redis_requested_state := rdb.Set(ctx, "relay/water/requestedstate", requested_state, 0 ).Err()
    if redis_requested_state != nil {
       panic(redis_requested_state)
    }


}
//Job3 - water
//Read redis for water
//Read user override for water user/water/requestedstate
//Determine if boiler should be on
//Write requested state to relay/water/requestedstate
