package main

import (
	"log"

	"github.com/salamoonder/salamoonder-go"
)

// Configuration
const (
	URL        = "https://example.com/"
	USER_AGENT = `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36`
	API_KEY    = "sr-YOUR-KEY"
)

var HEADERS = map[string]string{
	"User-Agent":             USER_AGENT,
	"sec-ch-ua":              `"Google Chrome";v="139", "Not-A.Brand";v="8", "Chromium";v="139"`,
	"sec-ch-ua-mobile":       "?0",
	"sec-ch-ua-platform":     `"Windows"`,
	"accept-language":        "en-US,en;q=0.9",
}

func main() {
	client := salamoonder.New(API_KEY)

	taskID, err := client.Task.CreateTask("IncapsulaUTMVCSolver", map[string]interface{}{
		"website":    URL,
		"user_agent": USER_AGENT,
	})
	if err != nil {
		log.Fatalf("Failed to create task: %v", err)
	}

	result, err := client.Task.GetTaskResult(taskID)
	if err != nil {
		log.Fatalf("Failed to get task result: %v", err)
	}

	utmvc, ok := result["utmvc"].(string)
	if !ok {
		log.Printf("ERROR: Failed to solve challenge: %+v", result)
		return
	}

	client.SessionCookies.Set("___utmvc", utmvc, ".example.com")

	log.Printf("SUCCESS: Successfully solved UTMVC challenge: %s", utmvc[:150])
	log.Printf("SUCCESS: User-Agent: %s", result["user-agent"])
}