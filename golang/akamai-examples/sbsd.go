package main

import (
	"log"

	"github.com/Salamoonder-LLC/salamoonder-go"
)

// Configuration
const (
	URL        = "https://example.com/"
	USER_AGENT = `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36`
	PROXY      = "http://user:pass@ip:port"
	API_KEY    = "sr-YOUR-KEY"
)

var HEADERS = map[string]string{
	"User-Agent":             USER_AGENT,
	"sec-ch-ua":              `"Google Chrome";v="141", "Not-A.Brand";v="8", "Chromium";v="141"`,
	"sec-ch-ua-mobile":       "?0",
	"sec-ch-ua-platform":     `"Windows"`,
	"accept-language":        "en-US,en;q=0.9",
}

func main() {
	client := salamoonder.New(API_KEY)

	akamaiData, err := client.AkamaiSBSD.FetchAndExtract(URL, USER_AGENT, PROXY)
	if err != nil {
		log.Printf("ERROR: Failed to retrieve Akamai SBSD data: %v", err)
		return
	}

	taskID, err := client.Task.CreateTask("AkamaiSBSDSolver", map[string]interface{}{
		"url":      akamaiData["base_url"],
		"cookie":   akamaiData["cookie_value"],
		"sbsd_url": akamaiData["sbsd_url"],
		"script":   akamaiData["script_data"],
	})
	if err != nil {
		log.Fatalf("Failed to create task: %v", err)
	}

	result, err := client.Task.GetTaskResult(taskID)
	if err != nil {
		log.Fatalf("Failed to get task result: %v", err)
	}

	cookie, err := client.AkamaiSBSD.PostSBSD(
		result["payload"].(string),
		akamaiData["sbsd_url"].(string),
		result["user-agent"].(string),
		URL,
		PROXY,
	)
	if err != nil {
		log.Fatalf("Failed to post SBSD: %v", err)
	}

	if cookie != nil {
		log.Printf("SUCCESS: Successfully solved Akamai SBSD on %s", URL)
		log.Printf("Cookie Dict: %+v", cookie)

		// Set the cookie in your jar
		// And then do your action.
	} else {
		log.Printf("ERROR: Failed to solve Akamai SBSD")
	}
}