package main

import (
	"log"
	"strings"

	"github.com/salamoonder/salamoonder-go"
)

// Configuration
const (
	URL        = "https://example.com/"
	USER_AGENT = `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36`
	PROXY      = "http://user:pass@ip:port"
	API_KEY    = "sr-YOUR-KEY"
)

var HEADERS = map[string]string{
	"User-Agent":             USER_AGENT,
	"sec-ch-ua":              `"Google Chrome";v="142", "Not-A.Brand";v="8", "Chromium";v="142"`,
	"sec-ch-ua-mobile":       "?0",
	"sec-ch-ua-platform":     `"Windows"`,
	"accept-language":        "en-US,en;q=0.9",
}

func main() {
	client := salamoonder.New(API_KEY)

	response, err := client.Get(URL, HEADERS, "")
	if err != nil {
		log.Fatalf("Failed to get initial page: %v", err)
	}

	respText := string(response.Body)
	if !strings.Contains(respText, "Pardon Our Interruption") && !strings.Contains(respText, "Incapsula incident ID") {
		log.Printf("INFO: No challenge detected")
		return
	}

	log.Printf("INFO: Incapsula challenge detected")

	// Solve the challenge
	taskID, err := client.Task.CreateTask("IncapsulaReese84Solver", map[string]interface{}{
		"website":        URL,
		"submit_payload": true,
		// Optional parameters
		// "reese_url": "..." <- https://apidocs.salamoonder.com/tasks/incapsula/reese84#what-if-your-response-doesn't-match-ours
		// "user_agent": USER_AGENT
	})
	if err != nil {
		log.Fatalf("Failed to create task: %v", err)
	}

	result, err := client.Task.GetTaskResult(taskID)
	if err != nil {
		log.Fatalf("Failed to get task result: %v", err)
	}

	token, ok := result["token"].(string)
	if !ok {
		log.Printf("ERROR: Failed to solve challenge: %+v", result)
		return
	}

	client.SessionCookies.Set("reese84", token, ".example.com")

	response, err = client.Get(URL, HEADERS, "")
	if err != nil {
		log.Fatalf("Failed to validate bypass: %v", err)
	}

	respText = string(response.Body)
	if !strings.Contains(respText, "Pardon Our Interruption") && !strings.Contains(respText, "Incapsula incident ID") {
		log.Printf("SUCCESS: Successfully bypassed Incapsula!")
	} else {
		log.Printf("ERROR: Bypass failed")
	}
}