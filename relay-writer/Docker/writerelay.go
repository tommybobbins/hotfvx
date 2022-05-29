package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"time"
        "github.com/kelseyhightower/envconfig"
)

type relayread struct {
	Ison bool `json:"ison"`
}

type Specification struct {
        Debug           bool `default:"false"` 
}

//func getrelay(url string) (error bool) {
func getrelay(url string) (bool, string) {
    var s Specification
    err := envconfig.Process("hotf", &s)
    if err != nil {
        log.Print(err.Error())
    }
    if s.Debug == true {
        format := " Debug: %v\n"
        _, err = fmt.Printf(format, s.Debug)
        if err != nil {
            log.Print(err.Error())
        }
    }

	spaceClient := http.Client{
            Timeout: time.Second * 2, // Timeout after 2 seconds
	}

	req, err := http.NewRequest(http.MethodGet, url, nil)
	if err != nil {
            log.Print(err)
            return false, "HTTP Method invalid"
	}

	req.Header.Set("User-Agent", "spacecount-tutorial")

	res, getErr := spaceClient.Do(req)
	if getErr != nil {
            log.Print(getErr)
            return false, "GET HTTP Error"
	}

	if res.Body != nil {
            defer res.Body.Close()
            //return false, "Body is invalid Error"
	}

	body, readErr := ioutil.ReadAll(res.Body)
	if readErr != nil {
            log.Print(readErr)
            return false, "Reading HTTP Body Error"
	}
        if s.Debug == true {
            fmt.Printf("%s \n",body)
        }
	relayread1 := relayread{}
	jsonErr := json.Unmarshal(body, &relayread1)
	if jsonErr != nil {
            log.Print(jsonErr)
            return false, "Parsing JSON Error"
	}

	fmt.Println(relayread1.Ison)
        return relayread1.Ison, "OK"
}

//func main() {
//    relay0 := "http://192.168.1.56/relay/0"
//    relay1 := "http://192.168.1.56/relay/0"
//    relay0_returned_state := getrelay(relay0)
//    relay1_returned_state := getrelay(relay1)
//    //if relay0_returned_state {
//	fmt.Println("Returned relay: %v\n", relay0_returned_state)
//    //}
//    //if relay1_returned_state {
//	fmt.Println("Returned relay: %v\n", relay1_returned_state)
//    //}
//}
