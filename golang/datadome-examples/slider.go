package main

import (
	"fmt"
	"log"

	"github.com/Salamoonder-LLC/salamoonder-go"
)

// Configuration
const (
	URL        = "https://example.com/"
	USER_AGENT = `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36`
	PROXY      = "http://user:pass@ip:port"
	API_KEY    = "sr-YOUR-KEY"
)

var HEADERS = map[string]string{
	"User-Agent":         USER_AGENT,
	"sec-ch-ua":          `"Google Chrome";v="146", "Not-A.Brand";v="8", "Chromium";v="146"`,
	"sec-ch-ua-mobile":   "?0",
	"sec-ch-ua-platform": `"Windows"`,
	"accept-language":    "en-US,en;q=0.9",
}

func main() {
	client := salamoonder.New(API_KEY)

	response, err := client.Get(URL, HEADERS, PROXY)
	if err != nil {
		log.Fatalf("Failed to get initial page: %v", err)
	}

	cookies := response.Cookies["datadome"]
	if cookies == "" {
		fmt.Println("No DataDome cookie found")
		return
	}

	challenge, err := client.Datadome.GetSliderChallenge(string(response.Body), cookies, URL, HEADERS, USER_AGENT)
	if err != nil {
		log.Fatalf("Failed to get slider challenge: %v", err)
	}

	taskID, err := client.Task.CreateTask("DataDomeSliderSolver", map[string]interface{}{
		"captcha_url":    challenge["captcha_url"],
		"challenge_page": challenge["challenge_page"],
		"user_agent":     USER_AGENT,
	})
	if err != nil {
		log.Fatalf("Failed to create task: %v", err)
	}

	result, err := client.Task.GetTaskResult(taskID, 1)
	if err != nil {
		log.Fatalf("Failed to get task result: %v", err)
	}

	solution, ok := result.(map[string]interface{})
	if !ok {
		log.Printf("ERROR: Unexpected result format: %+v", result)
		return
	}

	solvedURL, ok := solution["url"].(string)
	if !ok {
		log.Printf("ERROR: Failed to solve %+v", result)
		return
	}

	cookieResponse, err := client.Get(solvedURL, HEADERS, "")
	if err != nil {
		log.Fatalf("Failed to retrieve cookie: %v", err)
	}
	fmt.Println(string(cookieResponse.Body))
}