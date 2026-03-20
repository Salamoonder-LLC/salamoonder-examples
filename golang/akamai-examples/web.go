package main

import (
	"fmt"
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

	akamaiData, err := client.Akamai.FetchAndExtract(URL, USER_AGENT, PROXY)
	if err != nil {
		log.Printf("ERROR: Failed to retrieve Akamai data: %v", err)
		return
	}

	// Solve 3 sensors (requires 3 API calls, you pay per sensor)
	// For better pricing, use the private endpoint: support@salamoonder.com
	data := ""
	var cookie map[string]string

	for i := 0; i < 3; i++ {
		taskID, err := client.Task.CreateTask("AkamaiWebSensorSolver", map[string]interface{}{
			"url":        akamaiData["base_url"],
			"abck":       akamaiData["abck"],
			"bmsz":       akamaiData["bm_sz"],
			"script":     akamaiData["script_data"],
			"sensor_url": akamaiData["akamai_url"],
			"user_agent": USER_AGENT,
			"count":      i,
			"data":       data,
		})
		if err != nil {
			log.Fatalf("Failed to create task: %v", err)
		}

		result, err := client.Task.GetTaskResult(taskID)
		if err != nil {
			log.Fatalf("Failed to get task result: %v", err)
		}

		payload := result["payload"].(string)
		data = result["data"].(string)

		cookieResp, err := client.Akamai.PostSensor(
			akamaiData["akamai_url"].(string),
			payload,
			USER_AGENT,
			URL,
			PROXY,
		)
		if err != nil {
			log.Fatalf("Failed to post sensor: %v", err)
		}

		cookie = cookieResp.Cookies
	}

	log.Printf("SUCCESS: Successfully solved Akamai on %s", URL)

	for k, v := range cookie {
		client.SessionCookies.Set(k, v, ".example.com")
	}
}