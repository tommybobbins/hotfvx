package main

import (
    "fmt"
    "log"
    "github.com/kelseyhightower/envconfig"
    "periph.io/x/conn/v3/i2c/i2creg"
    "periph.io/x/conn/v3/physic"
    "periph.io/x/devices/v3/bmxx80"
    "periph.io/x/host/v3"
)

type Specification struct {
    Debug           bool `default:"false"`   
}

func readsensor() (float64, int64){

    var s Specification
    err := envconfig.Process("hotf", &s)
    if err != nil {
        log.Fatal(err.Error())
    }
    if s.Debug == true {
        format := " Debug: %v\n"
        _, err = fmt.Printf(format, s.Debug)
        if err != nil {
            log.Fatal(err.Error())
        }
    }

    // Load all the drivers:
    if _, err := host.Init(); err != nil {
        log.Fatal(err)
    }

    // Open a handle to the first available I²C bus:
    bus, err := i2creg.Open("")
   if err != nil {
       log.Fatal(err)
    }
    defer bus.Close()

    // Open a handle to a bme280/bmp280 connected on the I²C bus using default
    // settings:
    dev, err := bmxx80.NewI2C(bus, 0x76, &bmxx80.DefaultOpts)
    if err != nil {
        log.Fatal(err)
    }
    defer dev.Halt()

    // Read temperature from the sensor:
    var env physic.Env
    if err = dev.Sense(&env); err != nil {
        log.Fatal(err)
    }
    if s.Debug == true {
        fmt.Printf("%8f %8s\n", env.Temperature.Celsius(), env.Pressure)
    }
    return env.Temperature.Celsius(), int64(env.Pressure)
}
